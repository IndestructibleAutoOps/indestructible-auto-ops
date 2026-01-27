# Agent Memory Research - Paper & Project References

> 學術論文和開源項目參考列表

---

## 📚 學術論文

### 核心論文

| 日期 | 標題 | 論文連結 | 說明 |
|------|------|----------|------|
| 2023-10 | **MemGPT: Towards LLMs as Operating Systems** | [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) | 將 LLM 作為操作系統的記憶管理方法，實現虛擬無限上下文 |
| 2025-04 | **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory** | [arXiv:2504.19413](https://arxiv.org/abs/2504.19413) | 生產就緒的可擴展長期記憶架構，在 LOCOMO 基準上優於 OpenAI 26% |
| 2025-01 | **Zep: A Temporal Knowledge Graph Architecture for Agent Memory** | [arXiv:2501.13956](https://arxiv.org/abs/2501.13956) | 時序知識圖譜記憶架構 |
| 2023-09 | **CoALA: Cognitive Architectures for Language Agents** | [arXiv:2309.02427](https://arxiv.org/abs/2309.02427) | 認知架構語言代理框架，定義情節/程序/語義記憶分類 |

### 個性化記憶

| 日期 | 標題 | 論文連結 |
|------|------|----------|
| 2026-01 | Membox: Weaving Topic Continuity into Long-Range Memory for LLM Agents | [arXiv:2601.03785](https://arxiv.org/abs/2601.03785) |
| 2026-01 | SwiftMem: Fast Agentic Memory via Query-aware Indexing | [arXiv:2601.08160](https://arxiv.org/abs/2601.08160) |
| 2026-01 | SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory | [arXiv:2601.02744](https://arxiv.org/abs/2601.02744) |
| 2026-01 | SimpleMem: Efficient Lifelong Memory for LLM Agents | [arXiv:2601.02553](https://arxiv.org/abs/2601.02553) |
| 2025-02 | A-MEM: Agentic Memory for LLM Agents | [arXiv:2502.12110](https://arxiv.org/abs/2502.12110) |

### 從經驗中學習

| 日期 | 標題 | 論文連結 |
|------|------|----------|
| 2023-03 | Reflexion: Language agents with verbal reinforcement learning | [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) |
| 2023-08 | ExpeL: LLM Agents Are Experiential Learners | [arXiv:2308.10144](https://arxiv.org/abs/2308.10144) |
| 2024-09 | Agent workflow memory | [arXiv:2409.07429](https://arxiv.org/abs/2409.07429) |
| 2025-04 | SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills | [arXiv:2504.07079](https://arxiv.org/abs/2504.07079) |

### 長期任務記憶

| 日期 | 標題 | 論文連結 |
|------|------|----------|
| 2025-10 | Memory as Action: Autonomous Context Curation for Long-Horizon Agentic Tasks | [arXiv:2510.12635](https://arxiv.org/abs/2510.12635) |
| 2025-06 | MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents | [arXiv:2506.15841](https://arxiv.org/abs/2506.15841) |
| 2025-12 | Context as a Tool: Context Management for Long-Horizon SWE-Agents | [arXiv:2512.22087](https://arxiv.org/abs/2512.22087) |

### 綜述論文

| 日期 | 標題 | 論文連結 | GitHub |
|------|------|----------|--------|
| 2024-04 | A Survey on the Memory Mechanism of Large Language Model-based Agents | [arXiv:2404.13501](https://arxiv.org/abs/2404.13501) | [GitHub](https://github.com/nuster1128/LLM_Agent_Memory_Survey) |
| 2025-05 | Rethinking Memory in AI: Taxonomy, Operations, Topics, and Future Directions | [arXiv:2505.00675](https://arxiv.org/abs/2505.00675) | [GitHub](https://github.com/Elvin-Yiming-Du/Survey_Memory_in_AI) |
| 2025-07 | A Survey of Context Engineering for Large Language Models | [arXiv:2507.13334](https://arxiv.org/abs/2507.13334) | [GitHub](https://github.com/Meirtz/Awesome-Context-Engineering) |

---

## 🛠️ 開源項目

### 記憶框架

| 項目 | 描述 | GitHub | 星數 |
|------|------|--------|------|
| **Letta (MemGPT)** | 具有持久記憶的有狀態代理框架 | [letta-ai/letta](https://github.com/letta-ai/letta) | 11K+ |
| **Mem0** | 生產就緒的 AI 代理記憶層 | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 20K+ |
| **Graphiti** | 時序知識圖譜記憶 | [getzep/graphiti](https://github.com/getzep/graphiti) | 2K+ |
| **Cognee** | 知識圖譜與 LLM 整合 | [topoteretes/cognee](https://github.com/topoteretes/cognee) | 1K+ |

### Redis 相關

| 項目 | 描述 | GitHub |
|------|------|--------|
| **Redis Agent Memory Server** | Redis 官方代理記憶服務器 | [redis-developer/agent-memory-server](https://github.com/redis-developer/agent-memory-server) |
| **Redis AI Resources** | Redis AI 應用代碼示例 | [redis-developer/redis-ai-resources](https://github.com/redis-developer/redis-ai-resources) |
| **LangGraph Redis** | LangGraph 的 Redis 檢查點 | [redis-developer/langgraph-redis](https://github.com/redis-developer/langgraph-redis) |

### Agent 框架

| 項目 | 描述 | GitHub |
|------|------|--------|
| **LangChain** | LLM 應用開發框架 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| **LlamaIndex** | 數據框架用於 LLM 應用 | [run-llama/llama_index](https://github.com/run-llama/llama_index) |
| **AutoGen** | 多代理對話框架 | [microsoft/autogen](https://github.com/microsoft/autogen) |

### 論文集合

| 項目 | 描述 | GitHub |
|------|------|--------|
| **Awesome Memory for Agents** | 代理記憶論文集合（清華大學） | [TsinghuaC3I/Awesome-Memory-for-Agents](https://github.com/TsinghuaC3I/Awesome-Memory-for-Agents) |
| **Awesome Self-Evolving Agents** | 自我進化代理論文集合 | [EvoAgentX/Awesome-Self-Evolving-Agents](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) |

---

## 📊 基準測試

| 基準 | 描述 | 論文 | GitHub |
|------|------|------|--------|
| **LOCOMO** | 長期對話記憶評估 | [arXiv:2402.17753](https://arxiv.org/abs/2402.17753) | [snap-research/locomo](https://github.com/snap-research/locomo) |
| **LongMemEval** | 長期交互記憶基準 | [arXiv:2410.10813](https://arxiv.org/abs/2410.10813) | [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) |
| **MemBench** | 代理記憶綜合評估 | [arXiv:2506.21605](https://arxiv.org/abs/2506.21605) | [import-myself/Membench](https://github.com/import-myself/Membench) |
| **MemoryAgentBench** | 增量多輪交互評估 | [arXiv:2507.05257](https://arxiv.org/abs/2507.05257) | [HUST-AI-HYZ/MemoryAgentBench](https://github.com/HUST-AI-HYZ/MemoryAgentBench) |

---

## 📖 教程和課程

| 資源 | 描述 | 連結 |
|------|------|------|
| **Redis AI 文檔** | Redis 向量搜索和 AI 功能文檔 | [redis.io/docs/latest/develop/ai](https://redis.io/docs/latest/develop/ai/) |
| **LangGraph 記憶指南** | LangGraph 記憶管理教程 | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/how-tos/persistence_redis/) |
| **DeepLearning.AI 課程** | 語義快取 AI 代理課程 | [learn.deeplearning.ai](https://learn.deeplearning.ai/courses/semantic-caching-for-ai-agents/) |
| **Letta 文檔** | Letta 代理記憶文檔 | [docs.letta.com](https://docs.letta.com) |

---

## 🔗 相關博客文章

| 標題 | 來源 | 連結 |
|------|------|------|
| Build smarter AI agents: Manage short-term and long-term memory with Redis | Redis Blog | [redis.io/blog](https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/) |
| 10 techniques to optimize your semantic cache | Redis Blog | [redis.io/blog](https://redis.io/blog/10-techniques-for-semantic-cache-optimization/) |
| Agent Memory: How to Build Agents that Learn and Remember | Letta Blog | [letta.com/blog](https://www.letta.com/blog/agent-memory) |
| Context Engineering for AI Agents | Weaviate Blog | [weaviate.io/blog](https://weaviate.io/blog/context-engineering) |

---

*最後更新: 2025-01-27*