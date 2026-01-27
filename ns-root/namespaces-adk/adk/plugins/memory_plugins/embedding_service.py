"""
Embedding Service with multiple provider support.
Provides unified interface for generating embeddings from various providers.
"""

import asyncio
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class EmbeddingProvider(Enum):
    """Supported embedding providers."""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OLLAMA = "ollama"


@dataclass
class EmbeddingConfig:
    """Configuration for embedding service."""
    provider: EmbeddingProvider
    model: str
    dimension: int
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    api_version: Optional[str] = None
    batch_size: int = 100
    max_retries: int = 3
    timeout: float = 30.0


class BaseEmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    def __init__(self, config: EmbeddingConfig):
        self.config = config

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        pass

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        return self.config.dimension


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI embedding provider."""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self._client: Any = None

    async def _get_client(self) -> Any:
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.api_base,
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("openai package is required for OpenAI embeddings")
        return self._client

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        client = await self._get_client()
        response = await client.embeddings.create(
            model=self.config.model,
            input=text
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        client = await self._get_client()
        results: list[list[float]] = []
        
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            response = await client.embeddings.create(
                model=self.config.model,
                input=batch
            )
            results.extend([d.embedding for d in response.data])
        
        return results


class AzureOpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """Azure OpenAI embedding provider."""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self._client: Any = None

    async def _get_client(self) -> Any:
        """Lazy initialization of Azure OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncAzureOpenAI
                self._client = AsyncAzureOpenAI(
                    api_key=self.config.api_key,
                    azure_endpoint=self.config.api_base or "",
                    api_version=self.config.api_version or "2024-02-01",
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("openai package is required for Azure OpenAI embeddings")
        return self._client

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        client = await self._get_client()
        response = await client.embeddings.create(
            model=self.config.model,
            input=text
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        client = await self._get_client()
        results: list[list[float]] = []
        
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            response = await client.embeddings.create(
                model=self.config.model,
                input=batch
            )
            results.extend([d.embedding for d in response.data])
        
        return results


class CohereEmbeddingProvider(BaseEmbeddingProvider):
    """Cohere embedding provider."""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self._client: Any = None

    async def _get_client(self) -> Any:
        """Lazy initialization of Cohere client."""
        if self._client is None:
            try:
                import cohere
                self._client = cohere.AsyncClient(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("cohere package is required for Cohere embeddings")
        return self._client

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        client = await self._get_client()
        response = await client.embed(
            texts=[text],
            model=self.config.model,
            input_type="search_document"
        )
        return response.embeddings[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        client = await self._get_client()
        results: list[list[float]] = []
        
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            response = await client.embed(
                texts=batch,
                model=self.config.model,
                input_type="search_document"
            )
            results.extend(response.embeddings)
        
        return results


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    """Ollama embedding provider for local models."""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self._base_url = config.api_base or "http://localhost:11434"

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        try:
            import aiohttp
        except ImportError:
            raise ImportError("aiohttp package is required for Ollama embeddings")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base_url}/api/embeddings",
                json={"model": self.config.model, "prompt": text},
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as response:
                result = await response.json()
                return result["embedding"]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        tasks = [self.embed_text(text) for text in texts]
        return await asyncio.gather(*tasks)


class SentenceTransformersEmbeddingProvider(BaseEmbeddingProvider):
    """Sentence Transformers embedding provider for local models."""

    def __init__(self, config: EmbeddingConfig):
        super().__init__(config)
        self._model: Any = None

    def _get_model(self) -> Any:
        """Lazy initialization of Sentence Transformers model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.config.model)
            except ImportError:
                raise ImportError("sentence-transformers package is required")
        return self._model

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        model = self._get_model()
        embedding = await asyncio.to_thread(model.encode, text)
        return embedding.tolist()

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""
        model = self._get_model()
        embeddings = await asyncio.to_thread(
            model.encode, texts, batch_size=self.config.batch_size
        )
        return embeddings.tolist()


class EmbeddingService:
    """
    Unified embedding service with caching support.
    Provides a single interface for multiple embedding providers.
    """

    PROVIDER_MAP = {
        EmbeddingProvider.OPENAI: OpenAIEmbeddingProvider,
        EmbeddingProvider.AZURE_OPENAI: AzureOpenAIEmbeddingProvider,
        EmbeddingProvider.COHERE: CohereEmbeddingProvider,
        EmbeddingProvider.OLLAMA: OllamaEmbeddingProvider,
        EmbeddingProvider.SENTENCE_TRANSFORMERS: SentenceTransformersEmbeddingProvider,
    }

    def __init__(
        self,
        config: EmbeddingConfig,
        cache_client: Optional[Any] = None,
        cache_ttl: int = 86400
    ):
        """
        Initialize the embedding service.
        
        Args:
            config: Embedding configuration
            cache_client: Optional Redis client for caching embeddings
            cache_ttl: Cache TTL in seconds (default: 24 hours)
        """
        self.config = config
        self._cache_client = cache_client
        self._cache_ttl = cache_ttl
        
        provider_class = self.PROVIDER_MAP.get(config.provider)
        if not provider_class:
            raise ValueError(f"Unsupported embedding provider: {config.provider}")
        
        self._provider = provider_class(config)
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_tokens": 0
        }

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        return self._provider.dimension

    def _cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        return f"emb:{self.config.provider.value}:{self.config.model}:{text_hash}"

    async def _get_cached(self, text: str) -> Optional[list[float]]:
        """Get cached embedding if available."""
        if not self._cache_client:
            return None
        
        try:
            key = self._cache_key(text)
            cached = await self._cache_client.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        return None

    async def _set_cached(self, text: str, embedding: list[float]) -> None:
        """Cache an embedding."""
        if not self._cache_client:
            return
        
        try:
            key = self._cache_key(text)
            await self._cache_client.setex(
                key,
                self._cache_ttl,
                json.dumps(embedding)
            )
        except Exception:
            pass

    async def embed(self, text: str, use_cache: bool = True) -> list[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            use_cache: Whether to use caching
            
        Returns:
            Embedding vector
        """
        self._stats["total_requests"] += 1
        
        # Check cache
        if use_cache:
            cached = await self._get_cached(text)
            if cached:
                self._stats["cache_hits"] += 1
                return cached
        
        self._stats["cache_misses"] += 1
        
        # Generate embedding
        embedding = await self._provider.embed_text(text)
        
        # Cache result
        if use_cache:
            await self._set_cached(text, embedding)
        
        return embedding

    async def embed_many(
        self,
        texts: list[str],
        use_cache: bool = True
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            use_cache: Whether to use caching
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        results: list[Optional[list[float]]] = [None] * len(texts)
        texts_to_embed: list[tuple[int, str]] = []

        # Check cache for each text
        if use_cache:
            for i, text in enumerate(texts):
                cached = await self._get_cached(text)
                if cached:
                    results[i] = cached
                    self._stats["cache_hits"] += 1
                else:
                    texts_to_embed.append((i, text))
                    self._stats["cache_misses"] += 1
        else:
            texts_to_embed = list(enumerate(texts))
            self._stats["cache_misses"] += len(texts)

        self._stats["total_requests"] += len(texts)

        # Generate embeddings for uncached texts
        if texts_to_embed:
            indices, uncached_texts = zip(*texts_to_embed)
            embeddings = await self._provider.embed_batch(list(uncached_texts))
            
            for idx, embedding, text in zip(indices, embeddings, uncached_texts):
                results[idx] = embedding
                if use_cache:
                    await self._set_cached(text, embedding)

        return [r for r in results if r is not None]

    def get_stats(self) -> dict[str, int]:
        """Get embedding service statistics."""
        return self._stats.copy()

    def reset_stats(self) -> None:
        """Reset statistics."""
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_tokens": 0
        }


# Default configurations for common providers
OPENAI_ADA_002_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.OPENAI,
    model="text-embedding-ada-002",
    dimension=1536
)

OPENAI_3_SMALL_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.OPENAI,
    model="text-embedding-3-small",
    dimension=1536
)

OPENAI_3_LARGE_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.OPENAI,
    model="text-embedding-3-large",
    dimension=3072
)

COHERE_ENGLISH_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.COHERE,
    model="embed-english-v3.0",
    dimension=1024
)

COHERE_MULTILINGUAL_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.COHERE,
    model="embed-multilingual-v3.0",
    dimension=1024
)

OLLAMA_NOMIC_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.OLLAMA,
    model="nomic-embed-text",
    dimension=768
)

SENTENCE_TRANSFORMERS_MINILM_CONFIG = EmbeddingConfig(
    provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
    model="all-MiniLM-L6-v2",
    dimension=384
)