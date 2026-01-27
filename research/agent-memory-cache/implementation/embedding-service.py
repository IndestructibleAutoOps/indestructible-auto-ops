"""
Embedding Service: Multi-provider text embedding generation.

This module provides a unified interface for generating text embeddings
across multiple providers (OpenAI, Azure, Cohere, Ollama, local).

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache/implementation
@gl-semantic-anchor GL-00-IMPL_EMBEDDING_SVC
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import aiohttp


logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================


class EmbeddingProvider(Enum):
    """Supported embedding providers."""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    COHERE = "cohere"
    OLLAMA = "ollama"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    HUGGINGFACE = "huggingface"


class EmbeddingModel(Enum):
    """Predefined embedding models."""
    # OpenAI
    OPENAI_ADA_002 = "text-embedding-ada-002"
    OPENAI_SMALL_3 = "text-embedding-3-small"
    OPENAI_LARGE_3 = "text-embedding-3-large"
    
    # Cohere
    COHERE_EMBED_V3 = "embed-english-v3.0"
    COHERE_MULTILINGUAL_V3 = "embed-multilingual-v3.0"
    
    # Ollama
    OLLAMA_NOMIC = "nomic-embed-text"
    OLLAMA_LLAMA2 = "llama2"
    
    # Sentence Transformers
    SENTENCE_ALL_MINILM = "all-MiniLM-L6-v2"
    SENTENCE_MPNET = "all-mpnet-base-v2"


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""
    embedding: List[float]
    model: str
    dimension: int
    tokens_used: int = 0
    latency_ms: float = 0.0


@dataclass
class BatchEmbeddingResult:
    """Result of batch embedding generation."""
    embeddings: List[List[float]]
    model: str
    dimension: int
    total_tokens: int = 0
    latency_ms: float = 0.0
    errors: List[int] = None  # Indices of failed embeddings


@dataclass
class EmbeddingCacheEntry:
    """Cached embedding entry."""
    text_hash: str
    embedding: List[float]
    model: str
    timestamp: float
    hit_count: int = 0


# =============================================================================
# Abstract Embedding Provider
# =============================================================================


class BaseEmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""
    
    def __init__(self, model: str, api_key: Optional[str] = None, **kwargs):
        self.model = model
        self.api_key = api_key
        self.config = kwargs
        self._dimension: Optional[int] = None
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Get the embedding dimension."""
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding for a single text."""
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """Generate embeddings for multiple texts."""
        pass
    
    async def embed_with_cache(
        self,
        text: str,
        cache: Optional[Dict[str, List[float]]] = None
    ) -> EmbeddingResult:
        """Generate embedding with optional caching."""
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        if cache and text_hash in cache:
            logger.debug(f"Cache hit for embedding: {text_hash[:16]}...")
            return EmbeddingResult(
                embedding=cache[text_hash],
                model=self.model,
                dimension=len(cache[text_hash]),
                tokens_used=0,
                latency_ms=0.0
            )
        
        result = await self.embed(text)
        
        if cache is not None:
            cache[text_hash] = result.embedding
        
        return result


# =============================================================================
# OpenAI Embedding Provider
# =============================================================================


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI embedding provider."""
    
    # Model dimensions
    DIMENSIONS = {
        EmbeddingModel.OPENAI_ADA_002.value: 1536,
        EmbeddingModel.OPENAI_SMALL_3.value: 1536,
        EmbeddingModel.OPENAI_LARGE_3.value: 3072,
    }
    
    def __init__(
        self,
        model: str = EmbeddingModel.OPENAI_SMALL_3.value,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        super().__init__(model, api_key)
        self.base_url = base_url or "https://api.openai.com/v1"
        self.timeout = aiohttp.ClientTimeout(total=timeout)
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension for the model."""
        if self._dimension is None:
            self._dimension = self.DIMENSIONS.get(
                self.model,
                1536  # Default dimension
            )
        return self._dimension
    
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding using OpenAI API."""
        import time
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": text
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                
                data = await response.json()
                embedding = data["data"][0]["embedding"]
                tokens_used = data.get("usage", {}).get("prompt_tokens", 0)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return EmbeddingResult(
            embedding=embedding,
            model=self.model,
            dimension=len(embedding),
            tokens_used=tokens_used,
            latency_ms=latency_ms
        )
    
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """Generate embeddings for multiple texts."""
        import time
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": texts
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                
                data = await response.json()
                embeddings = [item["embedding"] for item in data["data"]]
                total_tokens = data.get("usage", {}).get("prompt_tokens", 0)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return BatchEmbeddingResult(
            embeddings=embeddings,
            model=self.model,
            dimension=len(embeddings[0]) if embeddings else 0,
            total_tokens=total_tokens,
            latency_ms=latency_ms
        )


# =============================================================================
# Cohere Embedding Provider
# =============================================================================


class CohereEmbeddingProvider(BaseEmbeddingProvider):
    """Cohere embedding provider."""
    
    DIMENSIONS = {
        EmbeddingModel.COHERE_EMBED_V3.value: 1024,
        EmbeddingModel.COHERE_MULTILINGUAL_V3.value: 1024,
    }
    
    def __init__(
        self,
        model: str = EmbeddingModel.COHERE_EMBED_V3.value,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        super().__init__(model, api_key)
        self.base_url = base_url or "https://api.cohere.ai/v1"
        self.timeout = aiohttp.ClientTimeout(total=timeout)
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension for the model."""
        if self._dimension is None:
            self._dimension = self.DIMENSIONS.get(self.model, 1024)
        return self._dimension
    
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding using Cohere API."""
        import time
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Client-Name": "agent-memory-cache"
        }
        
        payload = {
            "texts": [text],
            "model": self.model,
            "input_type": "search_document"
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/embed",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Cohere API error: {response.status} - {error_text}")
                
                data = await response.json()
                embedding = data["embeddings"][0]
                tokens_used = data.get("meta", {}).get("billed_units", {}).get("input_tokens", 0)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return EmbeddingResult(
            embedding=embedding,
            model=self.model,
            dimension=len(embedding),
            tokens_used=tokens_used,
            latency_ms=latency_ms
        )
    
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """Generate embeddings for multiple texts."""
        import time
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Client-Name": "agent-memory-cache"
        }
        
        payload = {
            "texts": texts,
            "model": self.model,
            "input_type": "search_document"
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/embed",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Cohere API error: {response.status} - {error_text}")
                
                data = await response.json()
                embeddings = data["embeddings"]
                total_tokens = data.get("meta", {}).get("billed_units", {}).get("input_tokens", 0)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return BatchEmbeddingResult(
            embeddings=embeddings,
            model=self.model,
            dimension=len(embeddings[0]) if embeddings else 0,
            total_tokens=total_tokens,
            latency_ms=latency_ms
        )


# =============================================================================
# Ollama Embedding Provider
# =============================================================================


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    """Ollama local embedding provider."""
    
    def __init__(
        self,
        model: str = EmbeddingModel.OLLAMA_NOMIC.value,
        base_url: Optional[str] = None,
        timeout: int = 60
    ):
        super().__init__(model, api_key=None)
        self.base_url = base_url or "http://localhost:11434"
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._dimension: Optional[int] = None
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension (determined on first use)."""
        if self._dimension is None:
            # Default to common dimensions for Ollama models
            self._dimension = 768
        return self._dimension
    
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding using Ollama API."""
        import time
        start_time = time.time()
        
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/api/embeddings",
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {response.status} - {error_text}")
                
                data = await response.json()
                embedding = data["embedding"]
        
        # Update dimension if different
        if self._dimension != len(embedding):
            self._dimension = len(embedding)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return EmbeddingResult(
            embedding=embedding,
            model=self.model,
            dimension=len(embedding),
            tokens_used=0,  # Ollama doesn't provide token counts
            latency_ms=latency_ms
        )
    
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """Generate embeddings for multiple texts (sequential)."""
        embeddings = []
        errors = []
        total_latency = 0.0
        
        for i, text in enumerate(texts):
            try:
                result = await self.embed(text)
                embeddings.append(result.embedding)
                total_latency += result.latency_ms
            except Exception as e:
                logger.error(f"Error embedding text {i}: {e}")
                errors.append(i)
                embeddings.append([])  # Placeholder for failed embedding
        
        return BatchEmbeddingResult(
            embeddings=embeddings,
            model=self.model,
            dimension=self.dimension,
            total_tokens=0,
            latency_ms=total_latency,
            errors=errors if errors else None
        )


# =============================================================================
# Sentence Transformers Provider
# =============================================================================


class SentenceTransformersProvider(BaseEmbeddingProvider):
    """Local Sentence Transformers embedding provider."""
    
    DIMENSIONS = {
        EmbeddingModel.SENTENCE_ALL_MINILM.value: 384,
        EmbeddingModel.SENTENCE_MPNET.value: 768,
    }
    
    def __init__(self, model: str = EmbeddingModel.SENTENCE_ALL_MINILM.value):
        super().__init__(model, api_key=None)
        self._model = None
    
    def _load_model(self):
        """Load the sentence-transformers model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model)
            except ImportError:
                raise ImportError(
                    "sentence-transformers package is required. "
                    "Install with: pip install sentence-transformers"
                )
        return self._model
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension for the model."""
        if self._dimension is None:
            self._dimension = self.DIMENSIONS.get(
                self.model,
                384  # Default for all-MiniLM-L6-v2
            )
        return self._dimension
    
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding using local model."""
        import time
        start_time = time.time()
        
        model = self._load_model()
        embedding = model.encode(text, convert_to_numpy=False).tolist()
        
        latency_ms = (time.time() - start_time) * 1000
        
        return EmbeddingResult(
            embedding=embedding,
            model=self.model,
            dimension=len(embedding),
            tokens_used=0,
            latency_ms=latency_ms
        )
    
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """Generate embeddings for multiple texts."""
        import time
        start_time = time.time()
        
        model = self._load_model()
        embeddings = model.encode(texts, convert_to_numpy=False).tolist()
        
        latency_ms = (time.time() - start_time) * 1000
        
        return BatchEmbeddingResult(
            embeddings=embeddings,
            model=self.model,
            dimension=len(embeddings[0]) if embeddings else 0,
            total_tokens=0,
            latency_ms=latency_ms
        )


# =============================================================================
# Unified Embedding Service
# =============================================================================


class EmbeddingService:
    """Unified embedding service supporting multiple providers."""
    
    PROVIDER_MAP = {
        EmbeddingProvider.OPENAI: OpenAIEmbeddingProvider,
        EmbeddingProvider.AZURE_OPENAI: OpenAIEmbeddingProvider,
        EmbeddingProvider.COHERE: CohereEmbeddingProvider,
        EmbeddingProvider.OLLAMA: OllamaEmbeddingProvider,
        EmbeddingProvider.SENTENCE_TRANSFORMERS: SentenceTransformersProvider,
    }
    
    def __init__(
        self,
        provider: Union[str, EmbeddingProvider] = EmbeddingProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        cache_embeddings: bool = True,
        **kwargs
    ):
        """
        Initialize embedding service.
        
        Args:
            provider: Embedding provider (enum or string)
            model: Model name (optional, uses default if not specified)
            api_key: API key for cloud providers
            cache_embeddings: Enable in-memory caching
            **kwargs: Additional provider-specific configuration
        """
        if isinstance(provider, str):
            provider = EmbeddingProvider(provider)
        
        self.provider = provider
        self.cache_embeddings = cache_embeddings
        self._embedding_cache: Dict[str, List[float]] = {}
        
        # Set default model if not specified
        if model is None:
            model = self._get_default_model(provider)
        
        # Initialize provider
        provider_class = self.PROVIDER_MAP.get(provider)
        if provider_class is None:
            raise ValueError(f"Unsupported provider: {provider}")
        
        self._provider = provider_class(
            model=model,
            api_key=api_key,
            **kwargs
        )
    
    def _get_default_model(self, provider: EmbeddingProvider) -> str:
        """Get default model for provider."""
        defaults = {
            EmbeddingProvider.OPENAI: EmbeddingModel.OPENAI_SMALL_3.value,
            EmbeddingProvider.COHERE: EmbeddingModel.COHERE_EMBED_V3.value,
            EmbeddingProvider.OLLAMA: EmbeddingModel.OLLAMA_NOMIC.value,
            EmbeddingProvider.SENTENCE_TRANSFORMERS: EmbeddingModel.SENTENCE_ALL_MINILM.value,
        }
        return defaults.get(provider, "")
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self._provider.dimension
    
    async def embed(self, text: str) -> EmbeddingResult:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            
        Returns:
            EmbeddingResult with embedding vector
        """
        if self.cache_embeddings:
            return await self._provider.embed_with_cache(
                text,
                cache=self._embedding_cache
            )
        return await self._provider.embed(text)
    
    async def embed_batch(self, texts: List[str]) -> BatchEmbeddingResult:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            BatchEmbeddingResult with embedding vectors
        """
        return await self._provider.embed_batch(texts)
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self._embedding_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "enabled": self.cache_embeddings,
            "size": len(self._embedding_cache),
            "provider": self.provider.value,
            "model": self._provider.model,
            "dimension": self.dimension
        }


# =============================================================================
# Factory Functions
# =============================================================================


def create_embedding_service(
    provider: Union[str, EmbeddingProvider] = "openai",
    **kwargs
) -> EmbeddingService:
    """
    Factory function to create embedding service.
    
    Args:
        provider: Embedding provider name or enum
        **kwargs: Additional configuration
        
    Returns:
        Configured EmbeddingService instance
    """
    return EmbeddingService(provider=provider, **kwargs)


# =============================================================================
# Example Usage
# =============================================================================


async def example_usage():
    """Example usage of embedding service."""
    
    # OpenAI embeddings
    openai_service = EmbeddingService(
        provider=EmbeddingProvider.OPENAI,
        api_key="your-api-key"
    )
    
    result = await openai_service.embed(
        "The user prefers Python over JavaScript"
    )
    print(f"OpenAI embedding dimension: {result.dimension}")
    print(f"Tokens used: {result.tokens_used}")
    
    # Cohere embeddings
    cohere_service = EmbeddingService(
        provider=EmbeddingProvider.COHERE,
        api_key="your-api-key"
    )
    
    batch_result = await cohere_service.embed_batch([
        "First document about AI",
        "Second document about ML",
        "Third document about DL"
    ])
    print(f"Batch embeddings: {len(batch_result.embeddings)}")
    
    # Local embeddings
    local_service = EmbeddingService(
        provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
        model="all-MiniLM-L6-v2"
    )
    
    result = await local_service.embed("Local embedding test")
    print(f"Local embedding dimension: {result.dimension}")


if __name__ == "__main__":
    asyncio.run(example_usage())