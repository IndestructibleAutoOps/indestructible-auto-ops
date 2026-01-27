# Agent 記憶與快取配置深度研究報告

> 針對 MachineNativeOps/machine-native-ops 專案的記憶系統架構分析與優化建議

---

## 目錄

1. [執行摘要](#1-執行摘要)
2. [Agent 記憶系統概述](#2-agent-記憶系統概述)
3. [記憶類型分類學](#3-記憶類型分類學)
4. [主流框架記憶架構分析](#4-主流框架記憶架構分析)
5. [快取策略與實現方案](#5-快取策略與實現方案)
6. [專案現狀分析](#6-專案現狀分析)
7. [優化建議方案](#7-優化建議方案)
8. [實施路線圖](#8-實施路線圖)
9. [參考資源](#9-參考資源)

---

## 1. 執行摘要

### 1.1 研究背景

AI Agent 的記憶系統是實現持續學習、個性化服務和長期任務執行的關鍵基礎設施。大型語言模型（LLM）本質上是無狀態的，每次交互都是獨立的，沒有從先前對話中攜帶的知識。記憶系統使 AI Agent 能夠從過去的交互中學習、保留信息並維持上下文，從而產生更連貫和個性化的響應。

### 1.2 核心發現

| 維度 | 發現 |
|------|------|
| **記憶分類** | 短期記憶（上下文窗口）+ 長期記憶（情節/程序/語義） |
| **存儲後端** | Redis 是首選方案，支持向量搜索、快取和持久化 |
| **快取策略** | 語義快取 + 自適應 TTL + LRU/LFU 驅逐策略 |
| **專案現狀** | 已有基礎 MemoryManager，但缺乏 Redis/Vector 後端實現 |

### 1.3 關鍵建議

1. **實現 Redis 記憶後端** - 支持短期和長期記憶的統一存儲
2. **整合向量數據庫** - 實現語義搜索和相似度匹配
3. **添加語義快取層** - 減少 LLM API 調用，降低成本和延遲
4. **實現記憶壓縮機制** - 自動摘要和記憶衰減策略

---

## 2. Agent 記憶系統概述

### 2.1 為什麼記憶很重要？

AI Agent 記憶對於提高效率和能力至關重要，因為大型語言模型（LLM）本身不會記住任何東西——它們是無狀態的。記憶允許 AI Agent：

- **從過去的交互中學習** - 積累經驗和知識
- **保留信息** - 跨會話維持用戶偏好和上下文
- **維持上下文** - 產生更連貫和個性化的響應

**實際案例**：想像一個設計用於規劃和預訂工作旅行的 AI Agent。沒有記憶，它將：
- 不記得個人偏好（例如，"你喜歡直飛還是轉機航班？"）
- 由於缺乏理解而犯程序性錯誤（例如，預訂不提供商務旅行所需設施的酒店）
- 無法回憶先前提供的詳細信息，如護照信息

### 2.2 記憶即上下文管理

Agent 的"記憶"從根本上取決於其上下文窗口中在任何給定時刻存在的內容。將上下文窗口視為 Agent 的工作記憶——用於回答問題、推理和採取行動的即時可用信息。

因此，設計 Agent 的記憶本質上是**上下文工程（Context Engineering）**：確定哪些 token 進入上下文窗口以及它們如何組織。記憶系統組合多種技術（如摘要、上下文重寫和檢索）來管理各種記憶組件（消息、記憶塊和外部數據庫）。

---

## 3. 記憶類型分類學

### 3.1 按持久性分類

根據清華大學 C3I 實驗室的研究框架，Agent 記憶可以按持久性分為：

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Memory Taxonomy                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │  Short-Term     │    │         Long-Term Memory         │ │
│  │    Memory       │    │                                   │ │
│  │                 │    │  ┌───────────┐  ┌─────────────┐  │ │
│  │  • Context      │    │  │ Experience│  │   Memory    │  │ │
│  │    Window       │    │  │           │  │             │  │ │
│  │  • Message      │    │  │ • Validated│  │ • No task   │  │ │
│  │    Buffer       │    │  │   by task │  │   outcome   │  │ │
│  │  • Working      │    │  │   outcomes│  │   reference │  │ │
│  │    Memory       │    │  │           │  │             │  │ │
│  │                 │    │  └───────────┘  └─────────────┘  │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 長期記憶的三種類型

基於著名的 CoALA 框架論文，長期記憶可進一步分為：

| 類型 | 描述 | 應用場景 |
|------|------|----------|
| **情節記憶 (Episodic)** | 存儲特定的過去事件和經歷，如 AI 交互的個人日記 | 用戶之前預訂了倫敦會議的旅行，偏好住在市中心 |
| **程序記憶 (Procedural)** | 存儲學習的技能、程序和"如何做"的知識 | AI 學習預訂航班的最佳流程，如確保轉機航班之間的適當間隔時間 |
| **語義記憶 (Semantic)** | 存儲一般知識、事實、概念和關係 | 存儲有關簽證要求、熱門旅遊目的地或平均酒店成本的信息 |

### 3.3 應用場景映射

| 應用場景 | 記憶內容 | 描述 |
|----------|----------|------|
| **個性化** | 用戶檔案、交互歷史、事實等 | 持續個性化交互，主要針對對話場景，使用帶有基於檢索的記憶交互的外部記憶池 |
| **從經驗中學習** | 軌跡、成功/失敗教訓、可重用技能等 | 跨任務經驗積累和轉移 |
| **長期任務** | 中間結果、推理軌跡、環境觀察等 | 通過摘要、反思或草稿本等方式在單個長期任務內進行上下文管理 |

---

## 4. 主流框架記憶架構分析

### 4.1 MemGPT / Letta - 操作系統方法

MemGPT（現為 Letta）是一個智能管理不同存儲層的系統，在 LLM 有限的上下文窗口內有效提供擴展上下文。

**核心架構**：

```
┌─────────────────────────────────────────────────────────────┐
│                    MemGPT Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    LLM Processor                         ││
│  │  ┌─────────────────────────────────────────────────────┐││
│  │  │              Context Window (RAM)                    │││
│  │  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐│││
│  │  │  │  System   │  │   Core    │  │     Message       ││││
│  │  │  │  Prompt   │  │  Memory   │  │      Buffer       ││││
│  │  │  │           │  │  Blocks   │  │                   ││││
│  │  │  └───────────┘  └───────────┘  └───────────────────┘│││
│  │  └─────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                           ↕ Function Calls                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              External Storage (Disk)                     ││
│  │  ┌─────────────────────┐  ┌─────────────────────────────┐││
│  │  │   Archival Memory   │  │      Recall Memory          │││
│  │  │   (Vector DB)       │  │   (Conversation History)    │││
│  │  └─────────────────────┘  └─────────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**關鍵特性**：
- 將上下文窗口視為受限的記憶資源
- 實現類似操作系統的記憶層次結構
- Agent 可以通過函數調用自主管理自己的記憶
- 在固定上下文限制內創建無限記憶的錯覺

### 4.2 Mem0 - 生產就緒的長期記憶

Mem0 是一個可擴展的以記憶為中心的架構，通過動態提取、整合和檢索對話中的顯著信息來解決 LLM 上下文窗口限制問題。

**核心優勢**：
- 在 LOCOMO 基準測試中，相對於 OpenAI 在 LLM-as-a-Judge 指標上提高了 **26%**
- 與全上下文方法相比，p95 延遲降低 **91%**
- 節省超過 **90%** 的 token 成本

**架構特點**：
```python
# Mem0 核心記憶操作
class Mem0Memory:
    def add(self, messages, user_id, metadata):
        """動態提取和存儲記憶"""
        # 1. 從消息中提取關鍵信息
        # 2. 生成嵌入向量
        # 3. 存儲到向量數據庫
        # 4. 更新圖結構（可選）
        
    def search(self, query, user_id, limit):
        """語義搜索相關記憶"""
        # 1. 生成查詢嵌入
        # 2. 向量相似度搜索
        # 3. 重排序和過濾
        # 4. 返回相關記憶
        
    def get_all(self, user_id):
        """獲取用戶所有記憶"""
```

### 4.3 Redis Agent Memory Server

Redis 提供了一個開源的 Agent Memory Server，專門用於管理 AI Agent 的記憶。

**為什麼選擇 Redis？**

| 特性 | 優勢 |
|------|------|
| **快速性能** | 內存架構確保微秒級讀寫操作 |
| **向量搜索** | 原生全功能向量數據庫，市場上最快的基準測試結果 |
| **AI 棧整合** | 與 LangGraph、LlamaIndex、Autogen 完全整合 |
| **可擴展性** | 支持多節點擴展、自動分層、高可用性 |
| **靈活性** | 多種數據結構選項（Hash、JSON、Vector） |

**記憶管理架構**：

```
┌─────────────────────────────────────────────────────────────┐
│              Redis Agent Memory Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Application Layer                      ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────────┐││
│  │  │ LangGraph │  │ LlamaIndex│  │      Custom Agent     │││
│  │  │ Checkpointer│ │ VectorStore│ │                       │││
│  │  └───────────┘  └───────────┘  └───────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Redis Agent Memory Server                   ││
│  │  ┌───────────────────┐  ┌───────────────────────────────┐││
│  │  │  Short-term Memory │  │     Long-term Memory         │││
│  │  │  (Checkpointer)    │  │  ┌─────────┐ ┌─────────────┐ │││
│  │  │                    │  │  │ Vector  │ │   Graph     │ │││
│  │  │  • Thread state    │  │  │ Search  │ │   Memory    │ │││
│  │  │  • Message buffer  │  │  │         │ │             │ │││
│  │  └───────────────────┘  │  └─────────┘ └─────────────┘ │││
│  │                         └───────────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Redis Stack                           ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐││
│  │  │ RedisJSON│ │ RediSearch│ │ RedisGraph│ │ Redis Streams │││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Graphiti / Zep - 時序知識圖譜

Graphiti 是一個時序知識圖譜架構，專門用於 Agent 記憶管理。

**核心特點**：
- 將記憶組織為圖結構
- 支持實體和關係的動態更新
- 時間感知的記憶檢索
- 支持複雜的多跳推理

---

## 5. 快取策略與實現方案

### 5.1 語義快取 (Semantic Caching)

語義快取的目的是重用先前計算的 LLM 工作——減少重複推理、改善延遲並穩定吞吐量。

**工作原理**：

```
┌─────────────────────────────────────────────────────────────┐
│                 Semantic Cache Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Query ──→ Embedding ──→ Vector Search                  │
│                                    │                         │
│                    ┌───────────────┴───────────────┐        │
│                    ↓                               ↓        │
│              Cache Hit                       Cache Miss      │
│                    │                               │        │
│                    ↓                               ↓        │
│           Return Cached                      LLM Call        │
│             Response                              │        │
│                                                   ↓        │
│                                          Store in Cache      │
│                                                   │        │
│                                                   ↓        │
│                                          Return Response     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 十大語義快取優化技術

| # | 技術 | 目的 | 應用示例 |
|---|------|------|----------|
| 1 | **移除語義噪音** | 聚焦嵌入於獨特含義，而非通用填充語言 | 從客服日誌中過濾"如有需要請告知"等重複短語 |
| 2 | **選擇和調優嵌入模型** | 確保嵌入準確捕獲領域特定的細微差別 | 醫療模型正確將"出院摘要"與臨床病歷關聯 |
| 3 | **摘要長上下文** | 提煉長文檔的語義核心以改善匹配 | 將10頁會議記錄摘要以匹配部署自動化決策查詢 |
| 4 | **調優相似度閾值** | 平衡精確度和召回率 | 調整閾值直到"如何重置登錄"和"忘記密碼"命中同一緩存條目 |
| 5 | **添加 LLM 重排序層** | 驗證和重新排序頂級語義候選項 | 為"如何升級欺詐索賠"查詢重排序多個接近匹配 |
| 6 | **使用元數據過濾** | 將搜索限制在正確的結構或上下文邊界 | 按 product=payments 和 region=EU 過濾"定價更新"搜索 |
| 7 | **實現自適應 TTL** | 根據波動性調整條目生命週期 | 實時股票數據設置短 TTL（15-30分鐘），穩定 FAQ 設置長 TTL |
| 8 | **監控命中/未命中模式** | 通過持續可觀測性檢測語義漂移 | 如果"計費問題"查詢經常未命中，表明該主題的嵌入分離較弱 |
| 9 | **預熱和預加載條目** | 確保可預測的啟動性能 | 為聊天機器人預加載前1000個常見問題 |
| 10 | **結合詞法和語義快取** | 精確匹配實現高精度，自然語言查詢保持靈活性 | 詞法快取用於"狀態碼403"，語義快取用於"訪問被禁止錯誤" |

### 5.3 記憶存儲策略

**四種主要存儲策略**：

```python
class MemoryStorageStrategies:
    """記憶存儲策略實現"""
    
    # 1. 摘要策略
    async def summarization(self, conversations: List[Message]) -> str:
        """使用 LLM 增量摘要對話"""
        summary = await self.llm.summarize(conversations)
        return summary
    
    # 2. 向量化策略
    async def vectorization(self, content: str) -> List[float]:
        """將內容轉換為向量嵌入"""
        # 語義分塊
        chunks = semantic_chunking(content)
        # 生成嵌入
        embeddings = await self.embedding_model.encode(chunks)
        return embeddings
    
    # 3. 提取策略
    async def extraction(self, conversation: List[Message]) -> List[Fact]:
        """從對話中提取關鍵事實"""
        facts = await self.llm.extract_facts(conversation)
        return facts
    
    # 4. 圖化策略
    async def graphication(self, content: str) -> Graph:
        """將信息映射為互連的實體和關係"""
        entities = await self.extract_entities(content)
        relations = await self.extract_relations(content)
        return Graph(entities, relations)
```

### 5.4 記憶衰減策略

記憶衰減對於防止記憶膨脹和維持效率至關重要：

| 策略 | 描述 | 適用場景 |
|------|------|----------|
| **TTL 過期** | 基於時間的自動過期 | 實時數據、會話上下文 |
| **LRU 驅逐** | 最近最少使用的條目被驅逐 | 一般用途快取 |
| **LFU 驅逐** | 最不頻繁使用的條目被驅逐 | 熱點數據快取 |
| **重要性衰減** | 基於訪問頻率和時間的重要性分數衰減 | 長期記憶管理 |
| **語義合併** | 相似記憶合併為更緊湊的表示 | 知識庫壓縮 |

---

## 6. 專案現狀分析

### 6.1 現有記憶管理架構

`machine-native-ops` 專案在 `ns-root/namespaces-adk/adk/core/memory_manager.py` 中已有基礎的記憶管理實現：

**現有架構**：

```
┌─────────────────────────────────────────────────────────────┐
│           Current Memory Manager Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    MemoryManager                         ││
│  │  ┌───────────────────────────────────────────────────┐  ││
│  │  │  • backend_type: str                              │  ││
│  │  │  • event_bus: EventBus                            │  ││
│  │  │  • _context_cache: Dict[str, List[MemoryEntry]]   │  ││
│  │  │  • _context_max_size: int                         │  ││
│  │  └───────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   MemoryBackend (ABC)                    ││
│  │  ┌───────────────────────────────────────────────────┐  ││
│  │  │  + add(entry) -> str                              │  ││
│  │  │  + get(entry_id) -> MemoryEntry                   │  ││
│  │  │  + update(entry_id, updates) -> bool              │  ││
│  │  │  + delete(entry_id) -> bool                       │  ││
│  │  │  + query(query) -> List[MemoryEntry]              │  ││
│  │  │  + summarize(session_id, max_tokens) -> str       │  ││
│  │  └───────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              InMemoryBackend (實現)                      ││
│  │  ┌───────────────────────────────────────────────────┐  ││
│  │  │  • _storage: Dict[str, MemoryEntry]               │  ││
│  │  │  • 簡單文本匹配查詢                                │  ││
│  │  │  • 基於重要性和時間的摘要                          │  ││
│  │  └───────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 現有數據結構

```python
# 記憶類型枚舉
class MemoryType(Enum):
    SHORT_TERM = "short_term"  # 上下文窗口
    LONG_TERM = "long_term"    # 持久存儲
    VECTOR = "vector"          # 向量數據庫（語義搜索）

# 記憶條目
@dataclass
class MemoryEntry:
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]]  # 預留向量嵌入
    memory_type: MemoryType
    session_id: Optional[str]
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    importance: float  # 0.0 到 1.0
    access_count: int

# 記憶查詢
@dataclass
class MemoryQuery:
    query_text: str
    session_id: Optional[str]
    user_id: Optional[str]
    memory_type: Optional[MemoryType]
    limit: int = 10
    threshold: float = 0.7  # 預留相似度閾值
    metadata_filter: Optional[Dict[str, Any]]
```

### 6.3 現有配置支持

在 `execution-engine.manifest.yaml` 中已定義了對 Redis 的支持：

```yaml
dependencies:
  required_services:
    - name: state_store
      options:
        - postgresql
        - redis
        - etcd
    - name: message_queue
      options:
        - rabbitmq
        - kafka
        - redis
    - name: lock_service
      options:
        - redis
        - zookeeper
        - etcd

configuration:
  performance:
    result_backend_cache_ttl: 3600
```

### 6.4 差距分析

| 維度 | 現狀 | 目標 | 差距 |
|------|------|------|------|
| **存儲後端** | 僅 InMemoryBackend | Redis + Vector DB | 缺少生產級後端 |
| **向量搜索** | 簡單文本匹配 | 語義相似度搜索 | 缺少嵌入生成和向量搜索 |
| **記憶壓縮** | 基於重要性的簡單摘要 | LLM 驅動的智能摘要 | 缺少 LLM 整合 |
| **快取層** | 簡單上下文快取 | 語義快取 + 自適應 TTL | 缺少語義快取實現 |
| **記憶衰減** | 無 | 自適應 TTL + LRU/LFU | 缺少驅逐策略 |
| **可觀測性** | 基本統計 | 完整監控儀表板 | 缺少詳細指標 |

---

## 7. 優化建議方案

### 7.1 架構升級方案

**目標架構**：

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Enhanced Memory Architecture                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                      Agent Runtime                               ││
│  │  ┌─────────────────────────────────────────────────────────────┐││
│  │  │                   Memory Manager                             │││
│  │  │  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐  │││
│  │  │  │ Context Cache │  │ Semantic Cache│  │ Memory Compactor│  │││
│  │  │  │ (Short-term)  │  │ (LLM Reuse)   │  │ (Summarization) │  │││
│  │  │  └───────────────┘  └───────────────┘  └─────────────────┘  │││
│  │  └─────────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────────┘│
│                                    ↕                                 │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Memory Backend Layer                          ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ││
│  │  │  Redis Backend  │  │  Vector Backend │  │  Graph Backend  │  ││
│  │  │                 │  │                 │  │                 │  ││
│  │  │  • Hash/JSON    │  │  • Embeddings   │  │  • Entities     │  ││
│  │  │  • Streams      │  │  • Similarity   │  │  • Relations    │  ││
│  │  │  • TTL/Eviction │  │  • Clustering   │  │  • Traversal    │  ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                    ↕                                 │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Infrastructure Layer                          ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ││
│  │  │   Redis Stack   │  │   Qdrant/Milvus │  │    Neo4j/       │  ││
│  │  │                 │  │   /Redis Vector │  │    RedisGraph   │  ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Redis 記憶後端實現

```python
# ns-root/namespaces-adk/adk/plugins/memory_plugins/redis_backend.py

"""
Redis Memory Backend: Production-ready memory storage with Redis.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_REDIS
@gl-evidence-required false
GL Unified Charter Activated
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import redis.asyncio as redis
from redis.commands.search.field import TextField, NumericField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from ...core.memory_manager import (
    MemoryBackend,
    MemoryEntry,
    MemoryQuery,
    MemoryType,
)


class RedisMemoryBackend(MemoryBackend):
    """
    Redis-based memory backend with vector search support.
    
    Features:
    - Fast in-memory storage with persistence
    - Vector similarity search for semantic retrieval
    - TTL-based automatic expiration
    - LRU/LFU eviction policies
    - Pub/Sub for real-time updates
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        prefix: str = "memory:",
        vector_dim: int = 1536,  # OpenAI embedding dimension
        default_ttl: int = 86400,  # 24 hours
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.prefix = prefix
        self.vector_dim = vector_dim
        self.default_ttl = default_ttl
        
        self._client: Optional[redis.Redis] = None
        self._logger = logging.getLogger(__name__)
        
    async def initialize(self) -> None:
        """Initialize Redis connection and create index."""
        self._client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
        )
        
        # Create vector search index
        await self._create_index()
        
    async def _create_index(self) -> None:
        """Create RediSearch index for memory entries."""
        index_name = f"{self.prefix}idx"
        
        try:
            # Check if index exists
            await self._client.ft(index_name).info()
        except redis.ResponseError:
            # Create index
            schema = (
                TextField("$.content", as_name="content"),
                TextField("$.session_id", as_name="session_id"),
                TextField("$.user_id", as_name="user_id"),
                TextField("$.memory_type", as_name="memory_type"),
                NumericField("$.importance", as_name="importance"),
                NumericField("$.created_at", as_name="created_at"),
                VectorField(
                    "$.embedding",
                    "FLAT",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.vector_dim,
                        "DISTANCE_METRIC": "COSINE",
                    },
                    as_name="embedding",
                ),
            )
            
            definition = IndexDefinition(
                prefix=[self.prefix],
                index_type=IndexType.JSON,
            )
            
            await self._client.ft(index_name).create_index(
                schema,
                definition=definition,
            )
            
    async def add(self, entry: MemoryEntry) -> str:
        """Add a memory entry to Redis."""
        key = f"{self.prefix}{entry.id}"
        
        # Serialize entry
        data = {
            "id": entry.id,
            "content": entry.content,
            "metadata": entry.metadata,
            "embedding": entry.embedding,
            "memory_type": entry.memory_type.value,
            "session_id": entry.session_id,
            "user_id": entry.user_id,
            "created_at": entry.created_at.timestamp(),
            "updated_at": entry.updated_at.timestamp(),
            "importance": entry.importance,
            "access_count": entry.access_count,
        }
        
        # Store as JSON
        await self._client.json().set(key, "$", data)
        
        # Set TTL based on memory type
        ttl = self._get_ttl(entry.memory_type, entry.importance)
        if ttl:
            await self._client.expire(key, ttl)
            
        return entry.id
        
    def _get_ttl(self, memory_type: MemoryType, importance: float) -> Optional[int]:
        """Calculate TTL based on memory type and importance."""
        if memory_type == MemoryType.SHORT_TERM:
            # Short-term: 1-4 hours based on importance
            return int(3600 * (1 + 3 * importance))
        elif memory_type == MemoryType.LONG_TERM:
            # Long-term: 1-30 days based on importance
            return int(86400 * (1 + 29 * importance))
        else:
            # Vector: use default TTL
            return self.default_ttl
            
    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID."""
        key = f"{self.prefix}{entry_id}"
        data = await self._client.json().get(key)
        
        if not data:
            return None
            
        return self._deserialize_entry(data)
        
    def _deserialize_entry(self, data: Dict[str, Any]) -> MemoryEntry:
        """Deserialize Redis data to MemoryEntry."""
        return MemoryEntry(
            id=data["id"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding"),
            memory_type=MemoryType(data["memory_type"]),
            session_id=data.get("session_id"),
            user_id=data.get("user_id"),
            created_at=datetime.fromtimestamp(data["created_at"]),
            updated_at=datetime.fromtimestamp(data["updated_at"]),
            importance=data.get("importance", 1.0),
            access_count=data.get("access_count", 0),
        )
        
    async def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory entry."""
        key = f"{self.prefix}{entry_id}"
        
        if not await self._client.exists(key):
            return False
            
        # Update fields
        updates["updated_at"] = datetime.now().timestamp()
        
        for field, value in updates.items():
            await self._client.json().set(key, f"$.{field}", value)
            
        return True
        
    async def delete(self, entry_id: str) -> bool:
        """Delete a memory entry."""
        key = f"{self.prefix}{entry_id}"
        result = await self._client.delete(key)
        return result > 0
        
    async def query(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        """Query memory entries with optional vector search."""
        index_name = f"{self.prefix}idx"
        
        # Build query
        query_parts = []
        
        if memory_query.session_id:
            query_parts.append(f"@session_id:{memory_query.session_id}")
        if memory_query.user_id:
            query_parts.append(f"@user_id:{memory_query.user_id}")
        if memory_query.memory_type:
            query_parts.append(f"@memory_type:{memory_query.memory_type.value}")
            
        # Text search
        if memory_query.query_text and not memory_query.embedding:
            query_parts.append(f"@content:{memory_query.query_text}")
            
        query_str = " ".join(query_parts) if query_parts else "*"
        
        # Vector search if embedding provided
        if hasattr(memory_query, 'embedding') and memory_query.embedding:
            query = (
                Query(f"({query_str})=>[KNN {memory_query.limit} @embedding $vec AS score]")
                .sort_by("score")
                .return_fields("id", "content", "session_id", "user_id", 
                              "memory_type", "importance", "created_at", "score")
                .dialect(2)
            )
            params = {"vec": self._encode_vector(memory_query.embedding)}
        else:
            query = (
                Query(query_str)
                .sort_by("created_at", asc=False)
                .paging(0, memory_query.limit)
            )
            params = {}
            
        # Execute query
        results = await self._client.ft(index_name).search(query, params)
        
        # Convert to MemoryEntry objects
        entries = []
        for doc in results.docs:
            data = await self._client.json().get(doc.id)
            if data:
                entry = self._deserialize_entry(data)
                entries.append(entry)
                
        return entries
        
    def _encode_vector(self, vector: List[float]) -> bytes:
        """Encode vector for Redis search."""
        import struct
        return struct.pack(f"{len(vector)}f", *vector)
        
    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        """Summarize memory for a session."""
        # Query all entries for session
        entries = await self.query(
            MemoryQuery(
                query_text="",
                session_id=session_id,
                limit=100,
            )
        )
        
        if not entries:
            return ""
            
        # Sort by importance and recency
        entries.sort(key=lambda e: (e.importance, e.created_at), reverse=True)
        
        # Build summary (in production, use LLM)
        summary_parts = []
        total_tokens = 0
        
        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens
            
        return " ".join(summary_parts)
        
    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
```

### 7.3 語義快取實現

```python
# ns-root/namespaces-adk/adk/plugins/memory_plugins/semantic_cache.py

"""
Semantic Cache: LLM response caching with semantic similarity.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_SEMCACHE
@gl-evidence-required false
GL Unified Charter Activated
"""

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import redis.asyncio as redis


@dataclass
class CacheEntry:
    """A semantic cache entry."""
    query: str
    response: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime
    access_count: int = 0
    ttl: int = 3600


class SemanticCache:
    """
    Semantic cache for LLM responses.
    
    Features:
    - Vector similarity-based cache lookup
    - Configurable similarity threshold
    - Adaptive TTL based on access patterns
    - LRU/LFU eviction policies
    - Cache warming and preloading
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        embedding_model: Any,  # Embedding model interface
        prefix: str = "semcache:",
        similarity_threshold: float = 0.85,
        default_ttl: int = 3600,
        max_entries: int = 10000,
        vector_dim: int = 1536,
    ):
        self._client = redis_client
        self._embedding_model = embedding_model
        self.prefix = prefix
        self.similarity_threshold = similarity_threshold
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self.vector_dim = vector_dim
        
        self._logger = logging.getLogger(__name__)
        
        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "stores": 0,
            "evictions": 0,
        }
        
    async def get(
        self,
        query: str,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Optional[Tuple[str, float]]:
        """
        Get cached response for a query.
        
        Args:
            query: The query string
            metadata_filter: Optional metadata filter
            
        Returns:
            Tuple of (response, similarity_score) if found, None otherwise
        """
        # Generate embedding for query
        query_embedding = await self._embedding_model.encode(query)
        
        # Search for similar queries
        results = await self._vector_search(
            query_embedding,
            limit=5,
            metadata_filter=metadata_filter,
        )
        
        if not results:
            self._stats["misses"] += 1
            return None
            
        # Check similarity threshold
        best_match = results[0]
        if best_match["score"] < self.similarity_threshold:
            self._stats["misses"] += 1
            return None
            
        # Update access count and TTL
        await self._update_access(best_match["id"])
        
        self._stats["hits"] += 1
        return (best_match["response"], best_match["score"])
        
    async def set(
        self,
        query: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
    ) -> str:
        """
        Store a query-response pair in cache.
        
        Args:
            query: The query string
            response: The LLM response
            metadata: Optional metadata
            ttl: Optional TTL in seconds
            
        Returns:
            Cache entry ID
        """
        # Generate embedding
        embedding = await self._embedding_model.encode(query)
        
        # Create entry
        entry_id = self._generate_id(query)
        entry = {
            "id": entry_id,
            "query": query,
            "response": response,
            "embedding": embedding,
            "metadata": metadata or {},
            "created_at": datetime.now().timestamp(),
            "access_count": 0,
        }
        
        # Store in Redis
        key = f"{self.prefix}{entry_id}"
        await self._client.json().set(key, "$", entry)
        
        # Set TTL
        actual_ttl = ttl or self.default_ttl
        await self._client.expire(key, actual_ttl)
        
        self._stats["stores"] += 1
        
        # Check if eviction needed
        await self._maybe_evict()
        
        return entry_id
        
    def _generate_id(self, query: str) -> str:
        """Generate unique ID for a query."""
        return hashlib.sha256(query.encode()).hexdigest()[:16]
        
    async def _vector_search(
        self,
        embedding: List[float],
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar entries using vector similarity."""
        index_name = f"{self.prefix}idx"
        
        # Build query
        query_parts = ["*"]
        if metadata_filter:
            for key, value in metadata_filter.items():
                query_parts.append(f"@metadata_{key}:{value}")
                
        query_str = " ".join(query_parts)
        
        # Vector search
        from redis.commands.search.query import Query
        
        query = (
            Query(f"({query_str})=>[KNN {limit} @embedding $vec AS score]")
            .sort_by("score")
            .return_fields("id", "query", "response", "score")
            .dialect(2)
        )
        
        import struct
        vec_bytes = struct.pack(f"{len(embedding)}f", *embedding)
        
        results = await self._client.ft(index_name).search(
            query,
            {"vec": vec_bytes},
        )
        
        return [
            {
                "id": doc.id,
                "query": doc.query,
                "response": doc.response,
                "score": 1 - float(doc.score),  # Convert distance to similarity
            }
            for doc in results.docs
        ]
        
    async def _update_access(self, entry_id: str) -> None:
        """Update access count and extend TTL."""
        key = f"{self.prefix}{entry_id}"
        
        # Increment access count
        await self._client.json().numincrby(key, "$.access_count", 1)
        
        # Extend TTL based on access frequency
        access_count = await self._client.json().get(key, "$.access_count")
        if access_count and access_count[0] > 10:
            # Popular entries get longer TTL
            current_ttl = await self._client.ttl(key)
            new_ttl = min(current_ttl * 1.5, self.default_ttl * 7)
            await self._client.expire(key, int(new_ttl))
            
    async def _maybe_evict(self) -> None:
        """Evict entries if cache is full."""
        # Count entries
        pattern = f"{self.prefix}*"
        count = 0
        async for _ in self._client.scan_iter(pattern):
            count += 1
            
        if count <= self.max_entries:
            return
            
        # Evict least recently used entries
        entries_to_evict = count - int(self.max_entries * 0.9)
        
        # Get all entries sorted by access count and created_at
        entries = []
        async for key in self._client.scan_iter(pattern):
            data = await self._client.json().get(key)
            if data:
                entries.append({
                    "key": key,
                    "access_count": data.get("access_count", 0),
                    "created_at": data.get("created_at", 0),
                })
                
        # Sort by access count (ascending) and created_at (ascending)
        entries.sort(key=lambda e: (e["access_count"], e["created_at"]))
        
        # Evict
        for entry in entries[:entries_to_evict]:
            await self._client.delete(entry["key"])
            self._stats["evictions"] += 1
            
    async def warm(self, entries: List[Dict[str, Any]]) -> int:
        """
        Pre-warm cache with entries.
        
        Args:
            entries: List of {"query": str, "response": str, "metadata": dict}
            
        Returns:
            Number of entries added
        """
        count = 0
        for entry in entries:
            await self.set(
                query=entry["query"],
                response=entry["response"],
                metadata=entry.get("metadata"),
            )
            count += 1
        return count
        
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0
        
        return {
            **self._stats,
            "hit_rate": hit_rate,
            "total_requests": total,
        }
        
    async def clear(self) -> int:
        """Clear all cache entries."""
        pattern = f"{self.prefix}*"
        count = 0
        async for key in self._client.scan_iter(pattern):
            await self._client.delete(key)
            count += 1
        return count
```

### 7.4 記憶壓縮器實現

```python
# ns-root/namespaces-adk/adk/plugins/memory_plugins/memory_compactor.py

"""
Memory Compactor: Intelligent memory summarization and compression.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_COMPACT
@gl-evidence-required false
GL Unified Charter Activated
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ...core.memory_manager import MemoryEntry, MemoryManager, MemoryType


@dataclass
class CompactionConfig:
    """Configuration for memory compaction."""
    max_context_tokens: int = 4000
    summarization_threshold: int = 3000
    eviction_ratio: float = 0.7  # Evict 70% of messages when compacting
    importance_decay_rate: float = 0.1  # Daily decay rate
    min_importance_threshold: float = 0.1


class MemoryCompactor:
    """
    Intelligent memory compaction and summarization.
    
    Features:
    - LLM-driven summarization of conversation history
    - Recursive summarization for long histories
    - Importance-based memory decay
    - Semantic deduplication
    - Memory consolidation during idle time
    """
    
    def __init__(
        self,
        memory_manager: MemoryManager,
        llm_client: Any,  # LLM client interface
        config: Optional[CompactionConfig] = None,
    ):
        self.memory_manager = memory_manager
        self.llm_client = llm_client
        self.config = config or CompactionConfig()
        
        self._logger = logging.getLogger(__name__)
        
    async def compact_session(
        self,
        session_id: str,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Compact memory for a session.
        
        Args:
            session_id: Session ID to compact
            force: Force compaction even if below threshold
            
        Returns:
            Compaction statistics
        """
        # Get current context
        context = await self.memory_manager.get_context(
            session_id,
            max_tokens=self.config.max_context_tokens * 2,
        )
        
        current_tokens = len(context.split())
        
        # Check if compaction needed
        if not force and current_tokens < self.config.summarization_threshold:
            return {
                "compacted": False,
                "reason": "below_threshold",
                "current_tokens": current_tokens,
            }
            
        # Get all short-term memories for session
        entries = await self.memory_manager.query(
            query_text="",
            session_id=session_id,
            memory_type=MemoryType.SHORT_TERM,
            limit=1000,
        )
        
        if not entries:
            return {
                "compacted": False,
                "reason": "no_entries",
            }
            
        # Sort by creation time
        entries.sort(key=lambda e: e.created_at)
        
        # Calculate eviction point
        eviction_count = int(len(entries) * self.config.eviction_ratio)
        entries_to_summarize = entries[:eviction_count]
        entries_to_keep = entries[eviction_count:]
        
        # Generate summary
        summary = await self._summarize_entries(entries_to_summarize)
        
        # Store summary as long-term memory
        summary_id = await self.memory_manager.add(
            content=summary,
            memory_type=MemoryType.LONG_TERM,
            session_id=session_id,
            metadata={
                "type": "session_summary",
                "summarized_count": len(entries_to_summarize),
                "summarized_at": datetime.now().isoformat(),
            },
            importance=0.8,
        )
        
        # Delete summarized entries
        deleted_count = 0
        for entry in entries_to_summarize:
            if await self.memory_manager.delete(entry.id):
                deleted_count += 1
                
        return {
            "compacted": True,
            "summary_id": summary_id,
            "entries_summarized": len(entries_to_summarize),
            "entries_deleted": deleted_count,
            "entries_kept": len(entries_to_keep),
            "original_tokens": current_tokens,
            "summary_tokens": len(summary.split()),
        }
        
    async def _summarize_entries(
        self,
        entries: List[MemoryEntry],
    ) -> str:
        """Summarize a list of memory entries using LLM."""
        # Build conversation text
        conversation = "\n\n".join([
            f"[{entry.created_at.strftime('%Y-%m-%d %H:%M')}] {entry.content}"
            for entry in entries
        ])
        
        # Generate summary using LLM
        prompt = f"""Summarize the following conversation history, preserving:
1. Key decisions and outcomes
2. Important facts and preferences mentioned
3. Action items and commitments
4. Any errors or issues encountered

Conversation:
{conversation}

Summary:"""

        response = await self.llm_client.generate(prompt, max_tokens=500)
        return response.strip()
        
    async def decay_importance(
        self,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Apply importance decay to memories.
        
        Args:
            session_id: Optional session ID to limit decay
            
        Returns:
            Decay statistics
        """
        # Query all long-term memories
        entries = await self.memory_manager.query(
            query_text="",
            session_id=session_id,
            memory_type=MemoryType.LONG_TERM,
            limit=10000,
        )
        
        updated_count = 0
        deleted_count = 0
        
        for entry in entries:
            # Calculate age in days
            age_days = (datetime.now() - entry.created_at).days
            
            # Apply decay
            new_importance = entry.importance * (
                1 - self.config.importance_decay_rate
            ) ** age_days
            
            # Boost importance based on access count
            access_boost = min(entry.access_count * 0.01, 0.3)
            new_importance = min(new_importance + access_boost, 1.0)
            
            if new_importance < self.config.min_importance_threshold:
                # Delete low-importance memories
                if await self.memory_manager.delete(entry.id):
                    deleted_count += 1
            else:
                # Update importance
                if await self.memory_manager.update(
                    entry.id,
                    metadata={"importance": new_importance},
                ):
                    updated_count += 1
                    
        return {
            "entries_processed": len(entries),
            "entries_updated": updated_count,
            "entries_deleted": deleted_count,
        }
        
    async def deduplicate(
        self,
        session_id: Optional[str] = None,
        similarity_threshold: float = 0.95,
    ) -> Dict[str, Any]:
        """
        Remove semantically duplicate memories.
        
        Args:
            session_id: Optional session ID to limit deduplication
            similarity_threshold: Similarity threshold for deduplication
            
        Returns:
            Deduplication statistics
        """
        # Query all memories with embeddings
        entries = await self.memory_manager.query(
            query_text="",
            session_id=session_id,
            memory_type=MemoryType.VECTOR,
            limit=10000,
        )
        
        # Filter entries with embeddings
        entries_with_embeddings = [e for e in entries if e.embedding]
        
        if len(entries_with_embeddings) < 2:
            return {
                "duplicates_found": 0,
                "duplicates_removed": 0,
            }
            
        # Find duplicates using cosine similarity
        duplicates = []
        processed = set()
        
        for i, entry1 in enumerate(entries_with_embeddings):
            if entry1.id in processed:
                continue
                
            for entry2 in entries_with_embeddings[i + 1:]:
                if entry2.id in processed:
                    continue
                    
                similarity = self._cosine_similarity(
                    entry1.embedding,
                    entry2.embedding,
                )
                
                if similarity >= similarity_threshold:
                    # Keep the one with higher importance or more recent
                    if entry1.importance > entry2.importance:
                        duplicates.append(entry2.id)
                        processed.add(entry2.id)
                    elif entry1.importance < entry2.importance:
                        duplicates.append(entry1.id)
                        processed.add(entry1.id)
                    elif entry1.created_at > entry2.created_at:
                        duplicates.append(entry2.id)
                        processed.add(entry2.id)
                    else:
                        duplicates.append(entry1.id)
                        processed.add(entry1.id)
                        
        # Remove duplicates
        removed_count = 0
        for entry_id in duplicates:
            if await self.memory_manager.delete(entry_id):
                removed_count += 1
                
        return {
            "duplicates_found": len(duplicates),
            "duplicates_removed": removed_count,
        }
        
    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
        
    async def consolidate(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """
        Consolidate memories during idle time (sleep-time compute).
        
        This method:
        1. Compacts short-term memory
        2. Applies importance decay
        3. Removes duplicates
        4. Extracts and stores key facts
        
        Args:
            session_id: Session ID to consolidate
            
        Returns:
            Consolidation statistics
        """
        results = {
            "session_id": session_id,
            "consolidated_at": datetime.now().isoformat(),
        }
        
        # Step 1: Compact short-term memory
        compaction_result = await self.compact_session(session_id)
        results["compaction"] = compaction_result
        
        # Step 2: Apply importance decay
        decay_result = await self.decay_importance(session_id)
        results["decay"] = decay_result
        
        # Step 3: Remove duplicates
        dedup_result = await self.deduplicate(session_id)
        results["deduplication"] = dedup_result
        
        return results
```

### 7.5 配置更新

更新 `AgentConfig` 以支持新的記憶配置：

```python
# 更新 ns-root/namespaces-adk/adk/core/agent_runtime.py

@dataclass
class MemoryConfig:
    """Memory system configuration."""
    # Backend settings
    backend: str = "redis"  # "in_memory", "redis", "vector"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Vector settings
    vector_dim: int = 1536
    embedding_model: str = "text-embedding-3-small"
    
    # Cache settings
    enable_semantic_cache: bool = True
    semantic_cache_threshold: float = 0.85
    semantic_cache_ttl: int = 3600
    semantic_cache_max_entries: int = 10000
    
    # Compaction settings
    enable_auto_compaction: bool = True
    compaction_threshold_tokens: int = 3000
    compaction_eviction_ratio: float = 0.7
    
    # Decay settings
    enable_importance_decay: bool = True
    importance_decay_rate: float = 0.1
    min_importance_threshold: float = 0.1
    
    # Context settings
    context_max_tokens: int = 4000
    context_cache_size: int = 50


@dataclass
class AgentConfig:
    """Configuration for the agent runtime."""
    name: str
    version: str = "1.0.0"
    environment: str = "development"
    config_path: Optional[str] = None
    enable_tracing: bool = True
    enable_metrics: bool = True
    enable_audit: bool = True
    max_concurrent_workflows: int = 10
    sandbox_enabled: bool = True
    plugin_directories: List[str] = field(default_factory=list)
    
    # Memory configuration
    memory: MemoryConfig = field(default_factory=MemoryConfig)
```

---

## 8. 實施路線圖

### 8.1 Phase 1: 基礎設施準備（1-2 週）

| 任務 | 優先級 | 預估時間 |
|------|--------|----------|
| 設置 Redis Stack 開發環境 | P0 | 2 天 |
| 創建 Redis 連接管理器 | P0 | 1 天 |
| 實現基礎 RedisMemoryBackend | P0 | 3 天 |
| 添加單元測試和整合測試 | P0 | 2 天 |
| 更新配置系統 | P1 | 1 天 |

### 8.2 Phase 2: 向量搜索整合（2-3 週）

| 任務 | 優先級 | 預估時間 |
|------|--------|----------|
| 整合嵌入模型（OpenAI/本地） | P0 | 2 天 |
| 實現向量索引創建和管理 | P0 | 3 天 |
| 實現語義搜索查詢 | P0 | 3 天 |
| 添加相似度閾值調優 | P1 | 2 天 |
| 實現混合搜索（詞法+語義） | P1 | 2 天 |
| 性能測試和優化 | P1 | 3 天 |

### 8.3 Phase 3: 語義快取（1-2 週）

| 任務 | 優先級 | 預估時間 |
|------|--------|----------|
| 實現 SemanticCache 類 | P0 | 3 天 |
| 添加自適應 TTL 策略 | P1 | 2 天 |
| 實現 LRU/LFU 驅逐策略 | P1 | 2 天 |
| 添加快取預熱功能 | P2 | 1 天 |
| 實現快取監控指標 | P1 | 2 天 |

### 8.4 Phase 4: 記憶壓縮（2 週）

| 任務 | 優先級 | 預估時間 |
|------|--------|----------|
| 實現 MemoryCompactor 類 | P0 | 3 天 |
| 整合 LLM 摘要功能 | P0 | 2 天 |
| 實現重要性衰減算法 | P1 | 2 天 |
| 實現語義去重 | P1 | 2 天 |
| 添加 Sleep-time 整合任務 | P2 | 2 天 |

### 8.5 Phase 5: 可觀測性和文檔（1 週）

| 任務 | 優先級 | 預估時間 |
|------|--------|----------|
| 添加 Prometheus 指標 | P1 | 2 天 |
| 創建 Grafana 儀表板 | P2 | 1 天 |
| 編寫 API 文檔 | P1 | 2 天 |
| 創建使用指南和示例 | P1 | 2 天 |

### 8.6 里程碑時間線

```
Week 1-2:   [████████████████████] Phase 1: 基礎設施準備
Week 3-5:   [████████████████████████████████] Phase 2: 向量搜索整合
Week 6-7:   [████████████████████] Phase 3: 語義快取
Week 8-9:   [████████████████████] Phase 4: 記憶壓縮
Week 10:    [██████████] Phase 5: 可觀測性和文檔
```

---

## 9. 參考資源

### 9.1 學術論文

| 論文 | 描述 | 鏈接 |
|------|------|------|
| **MemGPT** | 將 LLM 作為操作系統的記憶管理方法 | [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) |
| **Mem0** | 生產就緒的可擴展長期記憶架構 | [arXiv:2504.19413](https://arxiv.org/abs/2504.19413) |
| **CoALA** | 認知架構語言代理框架 | [arXiv:2309.02427](https://arxiv.org/abs/2309.02427) |
| **A-MEM** | 代理記憶的自主管理 | [arXiv:2502.12110](https://arxiv.org/abs/2502.12110) |
| **Zep/Graphiti** | 時序知識圖譜記憶架構 | [arXiv:2501.13956](https://arxiv.org/abs/2501.13956) |

### 9.2 開源項目

| 項目 | 描述 | GitHub |
|------|------|--------|
| **Letta (MemGPT)** | 具有持久記憶的有狀態代理框架 | [letta-ai/letta](https://github.com/letta-ai/letta) |
| **Mem0** | 生產就緒的 AI 代理記憶層 | [mem0ai/mem0](https://github.com/mem0ai/mem0) |
| **Redis Agent Memory Server** | Redis 官方代理記憶服務器 | [redis-developer/agent-memory-server](https://github.com/redis-developer/agent-memory-server) |
| **Graphiti** | 時序知識圖譜記憶 | [getzep/graphiti](https://github.com/getzep/graphiti) |
| **LangChain** | LLM 應用開發框架 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) |

### 9.3 文檔和教程

| 資源 | 描述 | 鏈接 |
|------|------|------|
| **Redis AI 文檔** | Redis 向量搜索和 AI 功能文檔 | [redis.io/docs/latest/develop/ai](https://redis.io/docs/latest/develop/ai/) |
| **LangGraph 記憶指南** | LangGraph 記憶管理教程 | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/how-tos/persistence_redis/) |
| **DeepLearning.AI 課程** | 語義快取 AI 代理課程 | [learn.deeplearning.ai](https://learn.deeplearning.ai/courses/semantic-caching-for-ai-agents/) |
| **Awesome Memory for Agents** | 代理記憶論文集合 | [TsinghuaC3I/Awesome-Memory-for-Agents](https://github.com/TsinghuaC3I/Awesome-Memory-for-Agents) |

### 9.4 基準測試

| 基準 | 描述 | 鏈接 |
|------|------|------|
| **LOCOMO** | 長期對話記憶評估 | [snap-research/locomo](https://github.com/snap-research/locomo) |
| **LongMemEval** | 長期交互記憶基準 | [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) |
| **MemBench** | 代理記憶綜合評估 | [import-myself/Membench](https://github.com/import-myself/Membench) |

---

## 附錄 A: 術語表

| 術語 | 定義 |
|------|------|
| **上下文窗口 (Context Window)** | LLM 在單次推理中可以處理的最大 token 數量 |
| **短期記憶 (Short-term Memory)** | 在單個任務或對話中管理的瞬態信息 |
| **長期記憶 (Long-term Memory)** | 跨任務持久存儲的外部信息 |
| **情節記憶 (Episodic Memory)** | 存儲特定過去事件和經歷的記憶類型 |
| **程序記憶 (Procedural Memory)** | 存儲學習的技能和程序的記憶類型 |
| **語義記憶 (Semantic Memory)** | 存儲一般知識和事實的記憶類型 |
| **語義快取 (Semantic Cache)** | 基於語義相似度重用先前 LLM 響應的快取機制 |
| **向量嵌入 (Vector Embedding)** | 文本的數值向量表示，捕獲語義含義 |
| **TTL (Time-to-Live)** | 快取條目的過期時間 |
| **LRU (Least Recently Used)** | 驅逐最近最少使用條目的快取策略 |
| **LFU (Least Frequently Used)** | 驅逐最不頻繁使用條目的快取策略 |

---

## 附錄 B: 配置示例

### B.1 Redis 記憶後端配置

```yaml
# config/memory.yaml
memory:
  backend: redis
  redis:
    host: localhost
    port: 6379
    db: 0
    password: ${REDIS_PASSWORD}
    prefix: "agent:memory:"
    
  vector:
    dim: 1536
    embedding_model: text-embedding-3-small
    distance_metric: cosine
    
  cache:
    enabled: true
    similarity_threshold: 0.85
    default_ttl: 3600
    max_entries: 10000
    eviction_policy: lru
    
  compaction:
    enabled: true
    threshold_tokens: 3000
    eviction_ratio: 0.7
    schedule: "0 */6 * * *"  # Every 6 hours
    
  decay:
    enabled: true
    rate: 0.1
    min_threshold: 0.1
    schedule: "0 0 * * *"  # Daily at midnight
```

### B.2 Docker Compose 配置

```yaml
# docker-compose.yaml
version: '3.8'

services:
  redis:
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"
      - "8001:8001"  # RedisInsight
    volumes:
      - redis_data:/data
    environment:
      - REDIS_ARGS=--appendonly yes
      
  agent:
    build: .
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./config:/app/config

volumes:
  redis_data:
```

---

*報告生成日期: 2025-01-27*
*版本: 1.0*
*作者: AI Research Assistant*