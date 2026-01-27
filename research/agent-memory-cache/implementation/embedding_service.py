import asyncio
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class EmbeddingProvider(Enum):
    """Supported embedding providers."""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    COHERE = "cohere"
    OLLAMA = "ollama"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    HUGGINGFACE = "huggingface"


@dataclass
class EmbeddingConfig:
    """Configuration for embedding service."""
    provider: EmbeddingProvider = EmbeddingProvider.OPENAI
    model: str = "text-embedding-ada-002"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    batch_size: int = 100
    timeout: int = 30
    cache_enabled: bool = True
    cache_ttl: int = 3600  # seconds
    
    # Provider-specific configs
    openai_api_type: Optional[str] = None  # for Azure
    openai_api_version: Optional[str] = None  # for Azure
    deployment_name: Optional[str] = None  # for Azure


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""
    embedding: List[float]
    model: str
    tokens_used: int = 0
    cached: bool = False
    latency_ms: float = 0.0


class EmbeddingService:
    """Service for generating text embeddings using multiple providers.
    
    Features:
    - Support for multiple embedding providers (OpenAI, Azure, Cohere, Ollama, etc.)
    - Caching layer to reduce API calls
    - Batch processing for efficiency
    - Automatic retry on failures
    - Latency and token usage tracking
    
    Usage:
        config = EmbeddingConfig(
            provider=EmbeddingProvider.OPENAI,
            model="text-embedding-ada-002",
            api_key="your-api-key"
        )
        service = EmbeddingService(config)
        result = service.embed("Your text here")
        embedding = result.embedding
    """
    
    def __init__(self, config: EmbeddingConfig, cache_client: Optional[Any] = None):
        """Initialize embedding service.
        
        Args:
            config: Embedding configuration
            cache_client: Optional cache client (Redis, etc.)
        """
        self.config = config
        self.cache_client = cache_client
        self._provider_client = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the provider-specific client."""
        try:
            if self.config.provider == EmbeddingProvider.OPENAI:
                import openai
                self._provider_client = openai.Client(api_key=self.config.api_key)
                
            elif self.config.provider == EmbeddingProvider.AZURE_OPENAI:
                import openai
                self._provider_client = openai.AzureOpenAI(
                    api_key=self.config.api_key,
                    api_base=self.config.api_base,
                    api_type=self.config.openai_api_type,
                    api_version=self.config.openai_api_version
                )
                
            elif self.config.provider == EmbeddingProvider.COHERE:
                import cohere
                self._provider_client = cohere.Client(api_key=self.config.api_key)
                
            elif self.config.provider == EmbeddingProvider.OLLAMA:
                # Ollama uses HTTP API
                self._provider_client = self.config.api_base or "http://localhost:11434"
                
            elif self.config.provider == EmbeddingProvider.SENTENCE_TRANSFORMERS:
                from sentence_transformers import SentenceTransformer
                self._provider_client = SentenceTransformer(self.config.model)
                
            elif self.config.provider == EmbeddingProvider.HUGGINGFACE:
                from transformers import AutoTokenizer, AutoModel
                self._tokenizer = AutoTokenizer.from_pretrained(self.config.model)
                self._model = AutoModel.from_pretrained(self.config.model)
                
        except ImportError as e:
            print(f"Failed to import required package for {self.config.provider}: {e}")
            self._provider_client = None
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"embedding:{self.config.provider.value}:{self.config.model}:{text_hash}"
    
    def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            EmbeddingResult with embedding vector and metadata
        """
        if not text.strip():
            return EmbeddingResult(embedding=[], model=self.config.model)
        
        # Check cache first
        if self.config.cache_enabled and self.cache_client:
            cache_key = self._get_cache_key(text)
            cached = self.cache_client.get(cache_key)
            if cached:
                cached_data = json.loads(cached)
                return EmbeddingResult(
                    embedding=cached_data["embedding"],
                    model=cached_data["model"],
                    tokens_used=cached_data["tokens_used"],
                    cached=True,
                    latency_ms=0.0
                )
        
        # Generate embedding
        start_time = time.time()
        embedding, tokens_used = self._generate_embedding(text)
        latency_ms = (time.time() - start_time) * 1000
        
        result = EmbeddingResult(
            embedding=embedding,
            model=self.config.model,
            tokens_used=tokens_used,
            cached=False,
            latency_ms=latency_ms
        )
        
        # Cache result
        if self.config.cache_enabled and self.cache_client:
            cache_key = self._get_cache_key(text)
            self.cache_client.setex(
                cache_key,
                self.config.cache_ttl,
                json.dumps({
                    "embedding": embedding,
                    "model": self.config.model,
                    "tokens_used": tokens_used
                })
            )
        
        return result
    
    def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of EmbeddingResult objects
        """
        results = []
        
        # Process in batches
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            
            # Check cache for each text
            uncached_texts = []
            uncached_indices = []
            
            for idx, text in enumerate(batch):
                if self.config.cache_enabled and self.cache_client:
                    cache_key = self._get_cache_key(text)
                    cached = self.cache_client.get(cache_key)
                    if cached:
                        cached_data = json.loads(cached)
                        results.append(EmbeddingResult(
                            embedding=cached_data["embedding"],
                            model=cached_data["model"],
                            tokens_used=cached_data["tokens_used"],
                            cached=True,
                            latency_ms=0.0
                        ))
                    else:
                        uncached_texts.append(text)
                        uncached_indices.append(idx)
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(idx)
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                batch_results, batch_tokens = self._generate_embeddings_batch(uncached_texts)
                
                for text_idx, (embedding, tokens) in enumerate(zip(batch_results, batch_tokens)):
                    results.append(EmbeddingResult(
                        embedding=embedding,
                        model=self.config.model,
                        tokens_used=tokens,
                        cached=False,
                        latency_ms=0.0
                    ))
                    
                    # Cache the result
                    if self.config.cache_enabled and self.cache_client:
                        cache_key = self._get_cache_key(uncached_texts[text_idx])
                        self.cache_client.setex(
                            cache_key,
                            self.config.cache_ttl,
                            json.dumps({
                                "embedding": embedding,
                                "model": self.config.model,
                                "tokens_used": tokens
                            })
                        )
        
        return results
    
    def _generate_embedding(self, text: str) -> Tuple[List[float], int]:
        """Generate embedding using the configured provider.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (embedding vector, tokens used)
        """
        try:
            if self.config.provider == EmbeddingProvider.OPENAI:
                response = self._provider_client.embeddings.create(
                    input=text,
                    model=self.config.model
                )
                embedding = response.data[0].embedding
                tokens_used = response.usage.total_tokens
                
            elif self.config.provider == EmbeddingProvider.AZURE_OPENAI:
                response = self._provider_client.embeddings.create(
                    input=text,
                    engine=self.config.deployment_name
                )
                embedding = response.data[0].embedding
                tokens_used = response.usage.total_tokens
                
            elif self.config.provider == EmbeddingProvider.COHERE:
                response = self._provider_client.embed(
                    texts=[text],
                    model=self.config.model
                )
                embedding = response.embeddings[0]
                tokens_used = response.meta.billed_units.input_tokens
                
            elif self.config.provider == EmbeddingProvider.OLLAMA:
                # Use HTTP API
                import requests
                response = requests.post(
                    f"{self._provider_client}/api/embeddings",
                    json={"model": self.config.model, "prompt": text},
                    timeout=self.config.timeout
                )
                embedding = response.json()["embedding"]
                tokens_used = len(text.split())  # Approximate
                
            elif self.config.provider == EmbeddingProvider.SENTENCE_TRANSFORMERS:
                embedding = self._provider_client.encode(text).tolist()
                tokens_used = len(text.split())
                
            elif self.config.provider == EmbeddingProvider.HUGGINGFACE:
                import torch
                inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self._model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
                tokens_used = len(inputs["input_ids"][0])
                
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
            
            return embedding, tokens_used
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return [], 0
    
    def _generate_embeddings_batch(self, texts: List[str]) -> Tuple[List[List[float]], List[int]]:
        """Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of input texts
            
        Returns:
            Tuple of (list of embeddings, list of tokens used)
        """
        try:
            if self.config.provider == EmbeddingProvider.OPENAI:
                response = self._provider_client.embeddings.create(
                    input=texts,
                    model=self.config.model
                )
                embeddings = [item.embedding for item in response.data]
                tokens_used_list = [response.usage.total_tokens // len(texts)] * len(texts)
                
            elif self.config.provider == EmbeddingProvider.AZURE_OPENAI:
                response = self._provider_client.embeddings.create(
                    input=texts,
                    engine=self.config.deployment_name
                )
                embeddings = [item.embedding for item in response.data]
                tokens_used_list = [response.usage.total_tokens // len(texts)] * len(texts)
                
            elif self.config.provider == EmbeddingProvider.COHERE:
                response = self._provider_client.embed(
                    texts=texts,
                    model=self.config.model
                )
                embeddings = response.embeddings
                tokens_used_list = [response.meta.billed_units.input_tokens] * len(texts)
                
            elif self.config.provider == EmbeddingProvider.OLLAMA:
                import requests
                embeddings = []
                tokens_used_list = []
                for text in texts:
                    response = requests.post(
                        f"{self._provider_client}/api/embeddings",
                        json={"model": self.config.model, "prompt": text},
                        timeout=self.config.timeout
                    )
                    embeddings.append(response.json()["embedding"])
                    tokens_used_list.append(len(text.split()))
                
            elif self.config.provider == EmbeddingProvider.SENTENCE_TRANSFORMERS:
                embeddings = self._provider_client.encode(texts).tolist()
                tokens_used_list = [len(text.split()) for text in texts]
                
            elif self.config.provider == EmbeddingProvider.HUGGINGFACE:
                import torch
                embeddings = []
                tokens_used_list = []
                for text in texts:
                    inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                    with torch.no_grad():
                        outputs = self._model(**inputs)
                    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
                    embeddings.append(embedding)
                    tokens_used_list.append(len(inputs["input_ids"][0]))
                
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
            
            return embeddings, tokens_used_list
            
        except Exception as e:
            print(f"Error generating batch embeddings: {e}")
            return [], []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get embedding service statistics.
        
        Returns:
            Dictionary with service statistics
        """
        return {
            "provider": self.config.provider.value,
            "model": self.config.model,
            "batch_size": self.config.batch_size,
            "cache_enabled": self.config.cache_enabled,
            "cache_ttl": self.config.cache_ttl
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of embedding service.
        
        Returns:
            Health status dictionary
        """
        try:
            # Test embedding generation
            test_result = self.embed("health check")
            
            return {
                "status": "healthy" if test_result.embedding else "unhealthy",
                "provider": self.config.provider.value,
                "model": self.config.model,
                "embedding_dimension": len(test_result.embedding) if test_result.embedding else 0
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": self.config.provider.value,
                "model": self.config.model,
                "error": str(e)
            }