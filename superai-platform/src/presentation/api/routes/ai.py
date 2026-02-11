"""AI & ML API routes - Expert Factory, Vector DB, Agents."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, UploadFile, File
from pydantic import BaseModel, Field

router = APIRouter()


# --- Schemas ---
class ExpertCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    domain: str = Field(..., description="Expert domain: quantum, ml, devops, security, data_engineering")
    specialization: str = Field(default="", max_length=500)
    knowledge_base: list[str] = Field(default_factory=list, description="List of document IDs or URLs")
    model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_prompt: str = Field(default="")


class ExpertQueryRequest(BaseModel):
    expert_id: str
    query: str = Field(..., min_length=1, max_length=10000)
    context: dict[str, Any] = Field(default_factory=dict)
    max_tokens: int = Field(default=4096, ge=1, le=32000)
    include_sources: bool = True


class VectorUpsertRequest(BaseModel):
    collection: str = Field(..., min_length=1, max_length=100)
    documents: list[str] = Field(..., min_items=1, description="Text documents to embed and store")
    metadata: list[dict[str, Any]] = Field(default_factory=list)
    ids: list[str] = Field(default_factory=list)


class VectorSearchRequest(BaseModel):
    collection: str = Field(..., min_length=1, max_length=100)
    query: str = Field(..., min_length=1, max_length=5000)
    top_k: int = Field(default=10, ge=1, le=100)
    filter: dict[str, Any] = Field(default_factory=dict)
    include_metadata: bool = True


class AgentTaskRequest(BaseModel):
    agent_type: str = Field(..., pattern=r"^(code_generator|code_reviewer|test_writer|doc_writer|devops_automator|security_auditor)$")
    task: str = Field(..., min_length=1, max_length=10000)
    context: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    output_format: str = Field(default="markdown", pattern=r"^(markdown|json|code|yaml)$")


class EmbeddingRequest(BaseModel):
    texts: list[str] = Field(..., min_items=1, max_items=100)
    model: str = Field(default="text-embedding-3-small")


# --- Endpoints ---
@router.post("/experts", status_code=201)
async def create_expert(request: ExpertCreateRequest) -> dict[str, Any]:
    """Create a new AI expert with domain knowledge."""
    from src.ai.factory.expert_factory import ExpertFactory
    factory = ExpertFactory()
    return await factory.create_expert(
        name=request.name,
        domain=request.domain,
        specialization=request.specialization,
        knowledge_base=request.knowledge_base,
        model=request.model,
        temperature=request.temperature,
        system_prompt=request.system_prompt,
    )


@router.post("/experts/query")
async def query_expert(request: ExpertQueryRequest) -> dict[str, Any]:
    """Query an AI expert with RAG-enhanced response."""
    from src.ai.factory.expert_factory import ExpertFactory
    factory = ExpertFactory()
    return await factory.query_expert(
        expert_id=request.expert_id,
        query=request.query,
        context=request.context,
        max_tokens=request.max_tokens,
        include_sources=request.include_sources,
    )


@router.get("/experts")
async def list_experts(domain: str | None = Query(None)) -> list[dict[str, Any]]:
    """List all registered AI experts."""
    from src.ai.factory.expert_factory import ExpertFactory
    factory = ExpertFactory()
    return await factory.list_experts(domain=domain)


@router.delete("/experts/{expert_id}", status_code=204)
async def delete_expert(expert_id: str) -> None:
    """Remove an AI expert."""
    from src.ai.factory.expert_factory import ExpertFactory
    factory = ExpertFactory()
    await factory.delete_expert(expert_id)


@router.post("/vectors/upsert")
async def vector_upsert(request: VectorUpsertRequest) -> dict[str, Any]:
    """Embed and store documents in vector database."""
    from src.ai.vectordb.manager import VectorDBManager
    manager = VectorDBManager()
    return await manager.upsert(
        collection=request.collection,
        documents=request.documents,
        metadata=request.metadata,
        ids=request.ids,
    )


@router.post("/vectors/search")
async def vector_search(request: VectorSearchRequest) -> dict[str, Any]:
    """Semantic search across vector collections."""
    from src.ai.vectordb.manager import VectorDBManager
    manager = VectorDBManager()
    return await manager.search(
        collection=request.collection,
        query=request.query,
        top_k=request.top_k,
        filter=request.filter,
        include_metadata=request.include_metadata,
    )


@router.get("/vectors/collections")
async def list_collections() -> list[dict[str, Any]]:
    """List all vector collections."""
    from src.ai.vectordb.manager import VectorDBManager
    manager = VectorDBManager()
    return await manager.list_collections()


@router.delete("/vectors/collections/{collection}", status_code=204)
async def delete_collection(collection: str) -> None:
    """Delete a vector collection."""
    from src.ai.vectordb.manager import VectorDBManager
    manager = VectorDBManager()
    await manager.delete_collection(collection)


@router.post("/agents/execute")
async def execute_agent_task(request: AgentTaskRequest) -> dict[str, Any]:
    """Execute an automated agent task."""
    from src.ai.agents.task_executor import AgentTaskExecutor
    executor = AgentTaskExecutor()
    return await executor.execute(
        agent_type=request.agent_type,
        task=request.task,
        context=request.context,
        constraints=request.constraints,
        output_format=request.output_format,
    )


@router.post("/embeddings")
async def generate_embeddings(request: EmbeddingRequest) -> dict[str, Any]:
    """Generate embeddings for text inputs."""
    from src.ai.embeddings.generator import EmbeddingGenerator
    generator = EmbeddingGenerator()
    return await generator.generate(texts=request.texts, model=request.model)