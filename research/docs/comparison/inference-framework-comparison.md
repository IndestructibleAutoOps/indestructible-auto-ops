# 主流大模型推理框架深度对比与选型指南(2025)
技术白皮书 / 性能评估与选型建议

面向读者:AI架构师、MLOps工程师、平台负责人、研发经理

## 0. 执行摘要(结论先行)

截至2025年,主流开源大模型推理框架在吞吐、延迟、内存效率与工程易用性上分化明显。综合权威基准、学术论文与一线工程实践,本报告给出三点总体结论:

第一,性能格局:在NVIDIA平台上,TensorRT-LLM凭借深度内核融合、连续批处理与Tensor Core的极致利用,通常取得最高峰值吞吐与更优的每瓦效率;但工程门槛与硬件锁定也更高。vLLM在跨硬件、迭代级调度与内存管理(PagedAttention)上表现稳健,是通用生产场景的“稳态优选”。SGLang在短对话/多轮缓存(RadixAttention)等场景具备强竞争力;LMDeploy在交互式推理与持久批处理、KV-cache优化方面表现出良好的工程性价比;Ollama聚焦本地化与极简易用,不适合高并发与极致吞吐;TGI在OpenAI兼容路由、生产级推理能力上成熟;FasterTransformer适合解码优先、低TTFT但吞吐敏感的特定场景;Triton Inference Server提供标准化可观测的Serving层能力,常与TRT-LLM组合用于生产级多模型管理。[^4][^5][^8][^9][^10][^12][^13][^16][^17][^21][^22][^26]

第二,延迟—吞吐的不可兼得:预填充(prefill)优先的迭代级批处理可显著提升吞吐,但在混合负载下会引入“生成停顿”(generation stalls),拉高TBT与尾延迟;解码优先策略能够稳住TBT,却牺牲吞吐。OSDI’24的Sarathi-Serve通过分块预填充与无停顿批处理,在严格SLO下相对vLLM实现最高3.5×容量提升(例如Mistral-7B、Yi-34B场景),同时显著降低尾延迟与流水线气泡,提供了一条可落地的折中路径。[^1]

第三,选型建议总览:在生产决策中,应以SLO(首令牌时间TTFT、令牌间延迟TBT、尾延迟P99)为主线,以吞吐/成本为约束条件。若核心目标是吞吐与能效且平台为NVIDIA,首选TensorRT-LLM(可配合Triton);若目标是跨硬件、可维护性与上线速度,首选vLLM;短对话高并发与多轮缓存优势场景可优先SGLang;工程易用与快速上线可选LMDeploy或TGI;本地化与极简部署场景选择Ollama;需要标准化可观测与多模型路由,建议Triton作为Serving底座。[^1][^3][^10][^12][^13][^16][^26]

为便于快速把握格局,以下表1给出场景—框架推荐矩阵;图1展示“性能—易用性—扩展性”的相对位置。

表1 场景—框架推荐矩阵(优势/注意事项)

| 场景 | 首选框架 | 备选 | 主要优势 | 注意事项 |
|---|---|---|---|---|
| NVIDIA平台、极致吞吐/能效 | TensorRT-LLM (+ Triton) | vLLM / SGLang | 峰值吞吐高、每瓦性能优、连续批处理与内核融合 | 硬件/软件栈锁定;构建与调优复杂度高[^4][^5][^16][^17] |
| 跨硬件、通用生产 | vLLM | TGI / LMDeploy | PagedAttention、OpenAI兼容API、分布式易用 | 在极端优化下峰值吞吐可能略逊TRT-LLM[^3][^10][^12][^26] |
| 短对话高并发/多轮缓存 | SGLang | vLLM | RadixAttention/对话缓存优势、上手友好 | 社区与生态仍在扩展[^21][^22] |
| 快速上线、工程易用 | LMDeploy / TGI | vLLM | 交互式推理、持久批处理、OpenAI兼容路由 | 高强度优化能力视场景而定[^12][^13][^20] |
| 本地化/极简易用 | Ollama | llama.cpp | 极简部署、桌面/轻量场景 | 不适合高并发与极致吞吐[^26] |
| 标准化Serving/多模型管理 | Triton (+ TRT-LLM/vLLM) | vLLM(自带Serving) | 生产级协议与可观测、模型仓管理 | 需掌握模型仓配置与性能工具[^16][^17][^19] |

![主流框架性能-易用性-扩展性象限图(示意)](/workspace/docs/comparison/ease_of_use_radar.png)

图1 象限图揭示:TRT-LLM在性能与能效维度占优;vLLM在易用性与跨硬件扩展性维度更均衡;SGLang与LMDeploy在特定场景(短对话、交互式)有突出平衡点;TGI与Triton偏工程与治理能力。选型应沿业务SLO与组织能力所构成的“可行边界”移动,而非追求单一指标的极值。

## 1. 研究方法与指标体系

本报告采用“指标—方法—证据”的三层结构,以统一的度量口径与可复现工具为基础,确保结论可信且可落地。

首先,明确核心指标:

- 吞吐(Throughput):以tokens/s与requests/s共同度量,关注不同批大小与输入/输出长度下的变化趋势。
- 首令牌时间(Time to First Token,TTFT):用户感知的首个可用响应时间。
- 令牌间延迟(Inter-Token Latency,ITL)/令牌间时间(Time Between Tokens,TBT):衡量生成流畅性,TBT在很多场景更敏感于尾延迟。
- 容量(Capacity):在既定SLO(如P99 TBT)约束下系统可持续承载的请求负载(QPS)。
- 能效:功耗与每瓦性能(tokens/s/W),反映单位能耗产出。[^2][^4]

其次,方法学与工具:

- 吞吐与延迟:统一以端到端延迟与批大小、输入/输出长度组合定义吞吐计算;结合实际请求到达过程(泊松分布)与SLO约束评估容量。[^2]
- 分布式推理:在TP/PP/EP/混合并行下评估扩展性与通信开销,结合跨节点互联(NVLink vs 以太网)对尾延迟与容量的影响。[^6][^25]
- 工具与协议:OpenAI兼容API用于快速对接;HTTP/gRPC与Perf Analyzer/GenAI-Perf用于标准化压测与对比。[^16][^19]

表2 性能指标定义与测量方法对照表

| 指标 | 定义 | 典型测量方法 | 关键影响因素 | 相关参考 |
|---|---|---|---|---|
| 吞吐(tok/s, req/s) | 单位时间处理token数/请求数 | 端到端延迟转化为吞吐;批大小×(输入+输出)/总时长 | 批大小、输入/输出长度、精度与量化 | [^2][^4] |
| TTFT | 请求到首token的时间 | 单token输出测量 | prefill策略、KV-cache、路由 | [^2] |
| ITL/TBT | 连续token间延迟/时间 | 平均与分位数(P50/P99) | 批调度、解码优先级、内存带宽 | [^2][^4] |
| 容量 | SLO约束下可持续QPS | 严格/宽松SLO下压测 | 停顿与气泡、并行配置 | [^1][^4] |
| 每瓦性能 | tok/s/W | 功耗计与吞吐比 | 框架与硬件优化度 | [^4] |

表3 基准工具与协议对比(简表)

| 工具/协议 | 作用 | 适配框架 | 备注 |
|---|---|---|---|
| OpenAI兼容API | 快速对接应用 | vLLM、TGI、SGLang、LMDeploy | 生态广、易集成[^10][^12][^20][^21] |
| HTTP/gRPC | 标准服务协议 | Triton、TGI | 统一接口与可观测[^16][^20] |
| Perf Analyzer | 端点压测 | Triton | 支持多轮对话模板[^19] |
| GenAI-Perf | LLM性能基准 | Triton + TRT-LLM | 统一场景与指标[^17][^18] |

证据分层:学术论文(OSDI、arXiv)、官方文档/博客(NVIDIA、vLLM、TGI)、第三方横评(BentoML、Clarifai、NLPCloud)。对存在冲突的数据,以“方法与配置透明度更高的来源”作为优先依据,并在文中明确不确定性边界。[^1][^2][^3][^4][^10][^12][^13][^15][^16][^17][^19][^21][^26]

## 2. 框架与优化技术概览

主流框架的内核技术与定位高度相关:优化路径与硬件支持共同决定其性能边界与工程成本。

- vLLM:以PagedAttention与连续批处理为核心,实现内存高效与高并发;跨硬件支持与OpenAI兼容API使其成为通用Serving的“默认选项”。最新版本在吞吐与TPOT上显著提升(如Llama 8B/70B的2.7×吞吐与5×TPOT改进)。[^3][^10]
- TensorRT-LLM:NVIDIA生态的深度优化引擎,强调内核融合、连续批处理、KV-cache优化与量化(FP8/INT8),在NVIDIA平台上的峰值吞吐与每瓦性能通常领先。适合对性能与能效极敏感的在线服务。[^5]
- SGLang:通过RadixAttention与对话缓存,在多轮对话与短上下文切换场景下具备显著延迟与吞吐优势;工程上易用,与OpenAI生态兼容度较高。[^21][^22]
- LMDeploy:聚焦工程易用与高效交互,支持持久批处理、交互式推理(长对话TTFT优化)、KV量化与张量并行;在短周期上线与多轮对话中具备良好性价比。[^12][^13][^14]
- TGI:面向生产的推理工具包,提供OpenAI兼容路由、并行与批量优化;与Eval Harness配合可进行标准化评测与上线验证。[^20]
- FasterTransformer:请求级批处理、解码优先,追求低TBT与稳定性,但吞吐受限于解码阶段的批量利用;适合对初始响应时间敏感、吞吐压力可管理的场景。[^1]
- Triton Inference Server:提供标准化模型服务(HTTP/gRPC/C++ API)、模型仓管理、动态批处理与丰富的性能分析工具;与TRT-LLM组合用于多模型、多实例的生产部署与观测。[^16][^17][^19]

表4 框架×关键优化特性矩阵(节选)

| 框架 | 连续批处理 | PagedAttention | KV-cache优化/量化 | 分布式并行 | OpenAI兼容 |
|---|---|---|---|---|---|
| vLLM | 是 | 是 | 支持(量化、KV优化) | TP/PP/混合 | 是[^10] |
| TensorRT-LLM | 是 | 部分(内存优化) | 深度支持(FP8/INT8等) | TP/PP/EP/混合 | 通过Serving层[^5][^16] |
| SGLang | 是 | 是(RadixAttention) | 支持 | TP/PP(社区实现) | 是(部分模型)[^21] |
| LMDeploy | 是(持久批处理) | 是(块化缓存) | 支持(KV量化) | TP | 通过路由[^12][^13] |
| TGI | 是 | 是 | 支持 | TP/PP | 是[^20] |
| FasterTransformer | 请求级(解码优先) | 否 | 支持 | TP/PP | 否(通常自集成)[^1] |
| Triton | 动态批处理 | 依backend | 依backend | 依backend | 可封装[^16] |

## 3. 性能对比(吞吐与延迟)

我们从7B/70B/MoE模型与单/多GPU场景展开,结合输入/输出长度与批大小,分析吞吐与延迟在不同框架上的行为。需要强调的是,基准数据对工作负载分布(长/短提示、输出长度)、上下文窗口、并发度与SLO设定高度敏感;不同研究的实验配置可能不完全一致,横向比较应在相同配置下解读。[^4]

图2展示不同框架在典型配置下的吞吐对比,表5给出跨GPU与批大小的吞吐示例。

![不同框架在典型配置下的吞吐对比(示意)](/workspace/docs/comparison/throughput_comparison.png)

图2 吞吐对比示意:TRT-LLM在H100/GH200上对7B与70B/MoE场景均展现高扩展性;vLLM在跨硬件平台上的曲线更平稳;MoE(如Mixtral-8×7B)因每次仅激活部分专家,通常优于同代70B密集模型的吞吐。[^4][^5]

表5 吞吐对比(示例:输入/输出=1024/1024,fp16;不同GPU与批大小)

| 模型 | 框架 | GPU | 批大小 | 吞吐(tok/s,近似) | 备注 |
|---|---|---|---|---|---|
| 7B(Mistral/LLaMA-3-8B) | TRT-LLM | H100 | 64 | ~8k–10k | GQA优势明显[^4][^5] |
| 7B(Mistral/LLaMA-3-8B) | vLLM | H100 | 64 | ~6k–8k | 跨硬件稳定[^4] |
| 7B(Mistral/LLaMA-3-8B) | vLLM | A100 | 64 | ~3k–5k | 相对H100较低[^4] |
| 70B(LLaMA-2/3-70B) | TRT-LLM | 4×H100 | 64 | ~3k–5k | H100相对A100约7.8×提升(特定配置)[^4] |
| 70B(LLaMA-2/3-70B) | vLLM | 4×H100 | 64 | ~2k–4k | 内存与并行管理影响较大[^4] |
| MoE(Mixtral-8×7B) | TRT-LLM/vLLM | 4×H100 | 64 | ~4k–6k | 稀疏专家激活优势[^4] |

在延迟维度(图3与表6),TTFT与TBT受调度策略与SLO约束显著影响。预填充优先的迭代级批处理(如vLLM的历史策略)在重负载长提示下可能产生“生成停顿”,导致TBT尾延迟抬升;Sarathi-Serve通过分块预填充与无停顿批处理在严格SLO下提升容量同时压低TBT与P99延迟。[^1]

![TTFT/TBT对比与SLO影响(示意)](/workspace/docs/comparison/latency_comparison.png)

图3 延迟对比示意:在严格SLO下,Sarathi-Serve的“stall-free”批处理显著降低尾延迟并提升容量;解码优先策略(例如FasterTransformer)能够稳住TBT,但吞吐受限。[^1]

表6 延迟对比(示例:在严格/宽松SLO下的TTFT/TBT)

| 场景 | 框架/策略 | TTFT(P50) | TBT(P99) | 备注 |
|---|---|---|---|---|
| Yi-34B,严格SLO | vLLM(预填充优先) | ~0.7s | ~0.7s+ | 可能出现秒级停顿[^1] |
| Yi-34B,严格SLO | Sarathi-Serve(分块+无停顿) | ~0.76s | ~0.14s | 容量提升至3.5×(严格SLO)[^1] |
| Mistral-7B,宽松SLO | vLLM | ~0.5s | ~0.3s | 负载增加时尾延迟上升[^1] |
| Mistral-7B,宽松SLO | Sarathi-Serve | ~0.5s | ~0.2s | 容量提升至2.6×(单A100)[^1] |

量化与KV-cache块大小也会显著影响吞吐:在H100上FP8、A100上INT8常优于FP16;KV-cache块大小≥16在A100上可提升吞吐(例如批64时,块16比块8高约1.27×)。[^4]

## 4. 内存效率与能效

内存效率的关键在于KV-cache管理与批处理调度。vLLM的PagedAttention以固定大小块管理KV-cache,减少内存碎片并提升并发;LMDeploy通过交互式推理缓存与持久批处理降低长对话的TTFT,提升批量效率。在多GPU/多节点部署中,TP的all-reduce通信开销显著,PP在跨节点以太网环境下更具通信性价比,但需通过微批与均匀批次减少流水线气泡。[^4][^12][^13][^25]

能效方面,TRT-LLM通常具有更高的每瓦性能(在相同吞吐下功耗更高,但单位功耗产出更优);vLLM在跨平台上取得更均衡的吞吐—功耗曲线。图4与图5示意能效对比与吞吐—功耗关系。

![框架能效(每瓦吞吐)对比(示意)](/workspace/docs/comparison/cost_effectiveness_matrix.png)

图4 每瓦性能对比示意:TRT-LLM在H100/GH200上取得更高的tokens/s/W;vLLM在跨平台上表现稳健。量化(FP8/INT8)与KV块大小优化是提升每瓦性能的实用手段。[^4]

表7 KV-cache块大小与吞吐影响(A100示例)

| 批大小 | 块大小=8 | 块大小=16 | 提升 |
|---|---|---|---|
| 64 | 基准 | +27% | 约1.27×[^4] |

表8 量化与吞吐/每瓦影响(示例)

| 框架 | GPU | 精度 | 吞吐变化 | 每瓦变化 | 备注 |
|---|---|---|---|---|---|
| vLLM/TRT-LLM | H100 | FP8 | ↑ | ↑ | FP8优势显著[^4] |
| vLLM/TRT-LLM | A100 | INT8 | ↑ | ↑ | A100无FP8时优选[^4] |

## 5. 易用性与开发者体验

在易用性维度,安装/部署复杂度、API友好度与文档完善度决定团队的上线速度与维护成本。第三方横评普遍认为:vLLM与TGI在安装与OpenAI兼容API方面友好;LMDeploy在交互式推理与持久批处理上有良好的工程体验;TensorRT-LLM需要更多的构建与调优工作,尤其在非NVIDIA生态中成本更高;Ollama在本地化与快速试用场景最具优势。[^10][^12][^13][^20][^26]

表9 易用性评分(定性)

| 框架 | 安装/部署 | API与生态 | 文档/示例 | 总体易用性 |
|---|---|---|---|---|
| vLLM | 简单 | OpenAI兼容 | 丰富 | 高[^10] |
| TensorRT-LLM | 复杂(需构建引擎) | 强(NVIDIA生态) | 完整 | 中(依赖团队经验)[^5] |
| SGLang | 简单 | OpenAI兼容(部分) | 增长中 | 高(应用层)[^21][^22] |
| LMDeploy | 简单 | REST/CLI | 完整 | 高(交互式场景)[^12][^13] |
| TGI | 中等 | OpenAI兼容/路由 | 完整 | 高(生产)[^20] |
| FasterTransformer | 中等 | 自定义 | 完整 | 中(工程集成) |
| Triton | 中等(容器化便捷) | HTTP/gRPC/C++ | 完整 | 高(标准化Serving)[^16] |
| Ollama | 极简 | CLI | 完整 | 高(本地/试用)[^26] |

## 6. 扩展性与分布式推理

扩展性包括张量并行(TP)、流水线并行(PP)、专家并行(EP)与混合策略。在跨节点以太网下,TP的all-reduce通信开销会成为瓶颈,PP的点对点通信更友好但易产生流水线气泡。Sarathi-Serve通过均匀批次与分块预填充显著减少气泡,在严格SLO与混合并行下取得更高容量。vLLM官方提供分布式推理与扩展指南;Triton + TRT-LLM在EKS上有多节点生产实践;K8s原生的llm-d探索 disaggregated prefill/decode 的分布式形态。[^1][^6][^7][^8][^25]

![框架扩展性与分布式能力对比(示意)](/workspace/docs/comparison/scalability_comparison.png)

图5 扩展性示意:TP在高带宽NVLink下效果最佳;跨节点应优先PP或混合并行;disaggregated架构可消除prefill/decode干扰但对KV迁移与带宽提出更高要求。[^1][^6][^7][^8][^25]

表10 分布式能力对比(简表)

| 框架 | TP | PP | EP | 跨节点 | 路由/调度 |
|---|---|---|---|---|---|
| vLLM | 是 | 是 | 部分 | 是 | 连续批处理[^6][^10] |
| TensorRT-LLM | 是 | 是 | 是 | 是 | 连续批处理 + 引擎优化[^5] |
| SGLang | 是(社区) | 是(社区) | 否 | 有限 | Radix缓存[^21] |
| LMDeploy | 是 | 是 | 否 | 是 | 持久批处理[^12][^13] |
| TGI | 是 | 是 | 否 | 是 | OpenAI兼容路由[^20] |
| FasterTransformer | 是 | 是 | 否 | 是 | 解码优先[^1] |
| Triton | 依backend | 依backend | 依backend | 是 | 动态批处理[^16] |
| llm-d(K8s) | 是 | 是 | 是 | 是 | disaggregated[^7][^8] |

## 7. 成本效益与硬件选型

硬件与框架的组合决定TCO(总拥有成本)。在NVIDIA H100/GH200上,TRT-LLM通常取得更高吞吐与每瓦;在A100上,INT8与KV块大小优化可显著提升性能;在AMD(MI250/MI300X)与Intel Habana(Gaudi2)上,vLLM与其他框架的适配度较好,但批量与内存饱和更快,需谨慎调参。组织成本方面,TRT-LLM的工程复杂度与硬件锁定可能增加前期投入;vLLM/TGI/LMDeploy在开发/运维效率与上线速度上更友好。[^4][^12][^15][^26]

表11 框架×硬件支持与峰值吞吐/每瓦(示例,定性/半定量)

| 框架 | H100/GH200 | A100 | AMD MI250/MI300X | Gaudi2 | 每瓦(相对) |
|---|---|---|---|---|---|
| TRT-LLM | 高 | 中 | 不支持 | 不支持 | 高[^4][^5] |
| vLLM | 高 | 高 | 中 | 中 | 中[^4] |
| SGLang | 高 | 中 | 限 | 限 | 中[^21] |
| LMDeploy | 中 | 中 | 限 | 限 | 中[^12][^13] |
| TGI | 中 | 中 | 限 | 中 | 中[^20] |
| FasterTransformer | 中 | 中 | 限 | 限 | 中[^1] |
| Triton(Serving) | 依backend | 依backend | 依backend | 依backend | 依backend[^16][^17] |

表12 TCO构成与场景化建议

| 维度 | 高吞吐在线服务 | 批处理/离线 | 研究/试验 | 建议 |
|---|---|---|---|---|
| 硬件 | H100/GH200 | A100/H100 | A100/MI系列 | 面向SLO与预算平衡[^4] |
| 框架 | TRT-LLM/Triton | vLLM/Dataset流水线 | vLLM/SGLang/LMDeploy | 依据工程能力与生态 |
| 能耗 | 高 | 中 | 低 | 优先每瓦优化(FP8/INT8)[^4] |
| 工程复杂度 | 高 | 中 | 低 | 团队培训与CI/CD |
| 上线速度 | 中 | 高 | 高 | 选择OpenAI兼容与标准Serving |

## 8. 选型建议(场景化)

将SLO目标与负载特征映射到框架与硬件组合,是生产选型的核心。

- 场景A:极致吞吐/能效(NVIDIA)与严格SLO。优先TRT-LLM(配合Triton Serving),在批大小与上下文窗口上通过FP8/INT8、KV块优化与连续批处理取得峰值;若混合负载导致停顿与尾延迟升高,考虑引入分块预填充与无停顿调度理念(S)或arathi-Serve采用更优的混合批次构建策略。[^1][^5][^16][^17]
- 场景B:跨硬件与通用生产。优先vLLM,以PagedAttention与OpenAI兼容API保障易用性与稳定性;需要更强路由与生产治理时引入TGI或Triton作为网关与可观测层。[^10][^20][^16]
- 场景C:短对话高并发/多轮缓存。优先SGLang(RadixAttention与对话缓存),兼顾易用性与性能;在极高并发下可叠加vLLM进行混合调度以吸收突发流量。[^21][^22]
- 场景D:快速上线与工程易用。优先LMDeploy或TGI,利用持久批处理、交互式推理与OpenAI兼容路由在较短时间内达成“可用且稳定”的服务级别。[^12][^13][^20]
- 场景E:本地化/极简易用。优先Ollama(或llama.cpp),满足个人与小团队的低门槛需求;注意其在高并发与极致吞吐上的局限。[^26]
- 场景F:标准化Serving/多模型管理。优先Triton(作为Serving底座),backend按需选择TRT-LLM或vLLM,利用模型仓、动态批处理与Perf Analyzer/GenAI-Perf进行持续调优。[^16][^17][^19]

表13 选型决策矩阵(示例)

| 目标SLO/负载 | 首选 | 备选 | 关键参数 |
|---|---|---|---|
| TTFT严格、P99 TBT严格 | TRT-LLM + Triton | vLLM + Sarathi策略 | 批大小、token预算、FP8/INT8[^1][^5][^16] |
| 高并发短对话 | SGLang | vLLM | 缓存命中、批处理策略[^21] |
| 快速上线 | LMDeploy/TGI | vLLM | 持久批处理、OpenAI路由[^12][^20] |
| 本地试用 | Ollama | llama.cpp | 极简部署[^26] |
| 多模型治理 | Triton | vLLM Serving | 模型仓、动态批处理[^16] |

## 9. 最佳实践与调优清单

- 批处理与调度:在预填充与解码之间取得平衡;对长提示使用分块预填充与均匀批次,避免生成停顿;依据SLO选择token预算与块大小。[^1]
- KV-cache与内存:使用PagedAttention或块化KV;依据GPU选择合适的块大小(例如A100上≥16);在H100上启用FP8、A100上启用INT8以提升吞吐与每瓦。[^4][^10]
- 分布式策略:优先TP于NVLink域内;跨节点采用PP或混合并行并减少流水线气泡;在高负载下评估disaggregated prefill/decode的可行性与带宽需求。[^1][^6][^7][^8]
- 性能验证:采用OpenAI兼容API与统一压测工具(Perf Analyzer/GenAI-Perf),以相同请求分布与SLO定义进行端到端验证。[^16][^17][^19]

表14 调优清单(按框架/硬件)

| 框架/硬件 | 参数 | 默认值 | 建议 | 影响 |
|---|---|---|---|---|
| vLLM(A100) | KV块大小 | 8 | 16+ | 吞吐↑(约+27%@bs=64)[^4] |
| vLLM(H100) | 量化 | FP16 | FP8 | 吞吐/每瓦↑[^4] |
| TRT-LLM(H100/GH200) | 批大小 | 1 | 32–64 | 吞吐↑(扩展性优)[^4][^5] |
| Triton + backend | 动态批处理 | 关 | 开 | 吞吐↑、尾延迟可控[^16] |
| 跨节点(PP) | 微批大小 | 任意 | 均匀/按SLO调 | 气泡↓、TBT↓[^1] |

## 10. 风险与信息缺口

- 工作负载差异:长/短提示、上下文窗口、并发与SLO设定不同,会显著影响框架排名;横向比较应在相同配置下进行。[^4]
- 框架版本与硬件差异:Tensor Core、互联带宽、驱动与CUDA版本、内核优化与框架版本差异可能带来显著性能差异,需要在报告中明确条件。[^4][^5]
- 成本数据:不同云厂商与本地部署的租赁/折旧与能耗成本存在区域与时间差异,需以企业自身账单校准。 
- MoE与新架构:SGLang、LMDeploy、MoE(如Mixtral)在更多模型与更大规模下的系统性对比数据仍有限,建议开展针对性PoC。[^4][^21]
- 信息缺口说明:第三方横评与官方博客的部分性能数据以图示为主,缺少可复现实验的完整数值表;内存带宽利用率(MBU)、模型FLOPs利用率(MFU)与算力-带宽耦合的框架级实测数据不足;TGI与Ollama在严格SLO/P99约束下的容量与尾延迟系统性对比有限;跨节点PP与混合并行在通用以太网下的最佳配置与气泡开销需要更多场景化验证;不同量化方案(FP8/INT8/GPTQ/AWQ)对吞吐与质量的框架间对比仍需补充;部分来源为博客或社区帖,需二次核验与交叉比对。[^4][^15][^26]

## 11. 附录:复现实验与参考配置

为保证复现性,建议遵循以下通用配置与度量方法:

- 环境:CUDA/cuDNN/驱动版本一致;精度(FP16/FP8/INT8)与量化策略统一;批大小、输入/输出长度与上下文窗口明确;并发与请求到达过程(泊松)一致。[^2][^4]
- 度量:TTFT(单token输出)、ITL/TBT(平均与分位数P50/P99)、吞吐(端到端延迟转化);每瓦性能(功耗计与吞吐比)。[^2][^4]
- 工具:OpenAI兼容API压测;Perf Analyzer与GenAI-Perf用于标准化测试;vLLM官方并行与扩展指南提供分布式配置参考;Triton提供模型仓、动态批处理与协议配置。[^16][^17][^19][^6]

表15 复现实验清单(示例)

| 模型 | 框架 | GPU | 输入/输出长度 | 批大小 | 精度/量化 | 度量工具 | 预期指标 |
|---|---|---|---|---|---|---|---|
| LLaMA-3-8B | vLLM | H100 | 1024/1024 | 32 | FP8 | GenAI-Perf | tok/s、TTFT、TBT、每瓦[^17] |
| LLaMA-2-70B | TRT-LLM + Triton | 4×H100 | 1024/1024 | 64 | FP8/INT8 | Perf Analyzer | tok/s、P99 TBT[^16][^19] |
| Mixtral-8×7B | vLLM | 4×H100 | 2048/512 | 64 | FP16 | OpenAI API压测 | tok/s、容量[^4][^10] |
| Mistral-7B | vLLM vs Sarathi-Serve策略 | A100 | 1730/415 | 32 | FP16 | 自定义压测 | 容量、停顿时长[^1] |

---

## 参考文献

[^1]: Agrawal, K. et al. Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve. OSDI 2024. https://www.usenix.org/system/files/osdi24-agrawal.pdf  
[^2]: Chitty-Venkata, K. et al. LLM-Inference-Bench: Inference Benchmarking of Large Language Models on AI Accelerators. arXiv:2411.00136. https://arxiv.org/pdf/2411.00136  
[^3]: vLLM Team. vLLM v0.6.0: 2.7x Throughput Improvement and 5x Latency Reduction. https://blog.vllm.ai/2024/09/05/perf-update.html  
[^4]: NVIDIA. LLM Benchmarking: Fundamental Concepts. https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/  
[^5]: NVIDIA. TensorRT-LLM — GitHub. https://github.com/NVIDIA/TensorRT-LLM  
[^6]: vLLM Docs. Parallelism and Scaling. https://docs.vllm.ai/en/stable/serving/parallelism_scaling/  
[^7]: Red Hat Developer. llm-d: Kubernetes-native distributed inferencing. https://developers.redhat.com/articles/2025/05/20/llm-d-kubernetes-native-distributed-inferencing  
[^8]: AWS. Scaling your LLM inference workloads: multi-node deployment with TensorRT-LLM and Triton on Amazon EKS. https://aws.amazon.com/blogs/hpc/scaling-your-llm-inference-workloads-multi-node-deployment-with-tensorrt-llm-and-triton-on-amazon-eks/  
[^9]: NVIDIA. NVIDIA Triton Inference Server Achieves Outstanding Performance in MLPerf Inference 4.1. https://developer.nvidia.com/blog/nvidia-triton-inference-server-achieves-outstanding-performance-in-mlperf-inference-4-1-benchmarks/  
[^10]: vLLM Project — GitHub. https://github.com/vllm-project/vllm  
[^11]: Hugging Face. Benchmarking Text Generation Inference (TGI). https://huggingface.co/blog/tgi-benchmarking  
[^12]: LMDeploy — GitHub. https://github.com/InternLM/lmdeploy  
[^13]: LMDeploy Docs. Installation. https://lmdeploy.readthedocs.io/en/latest/get_started/installation.html  
[^14]: OpenMMLab. Deploy Llama-2 models easily with LMDeploy. https://openmmlab.medium.com/deploy-llama-2-models-easily-with-lmdeploy-1cb001d70290  
[^15]: BentoML. Benchmarking LLM Inference Backends. https://www.bentoml.com/blog/benchmarking-llm-inference-backends  
[^16]: NVIDIA. Inference Protocols and APIs — Triton. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/inference_protocols.html  
[^17]: NVIDIA. GenAI-Perf — NVIDIA Triton. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_benchmark/genai_perf.html  
[^18]: Triton Inference Server — GitHub. https://github.com/triton-inference-server/server  
[^19]: NVIDIA. Benchmarking Triton via HTTP or gRPC endpoint — Perf Analyzer. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/docs/benchmarking.html  
[^20]: Hugging Face. Text Generation Inference (TGI) — GitHub. https://github.com/huggingface/text-generation-inference  
[^21]: LMSYS. SGLang: Efficient Serving of Large Language Models — Blog. https://lmsys.org/blog/2024-01-17-sglang/  
[^22]: LMSYS. SGLang: Llama 3 Instruction Following — Blog. https://lmsys.org/blog/2024-07-25-sglang-llama3/  
[^23]: E2E Cloud. Inference Benchmarking. https://docs.e2enetworks.com/docs/tir/benchmarks/inference_benchmarks/  
[^24]: Wallaroo.AI. LLM Inference Autoscaling Benchmarks (2025.1). https://docs.wallaroo.ai/wallaroo-llm/wallaroo-llm-optimizations/wallaroo-llm-optimizations-benchmarks/wallaroo-llm-optimizations-benchmarks-automatic-triggers/  
[^25]: Niradler. GPU Inference Servers Comparison: Triton vs TGI vs vLLM vs Ollama. https://blog.niradler.com/gpu-inference-servers-comparison-triton-vs-tgi-vs-vllm-vs-ollama  
[^26]: Ordina Data. Choosing your LLM framework: a comparison of Ollama, vLLM, SGLang and TensorRT-LLM. https://medium.com/ordina-data/choosing-your-llm-framework-a-comparison-of-ollama-vllm-sglang-and-tensorrt-llm-e0cb4a0d1cb8