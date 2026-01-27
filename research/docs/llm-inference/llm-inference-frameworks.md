# 2025主流开源大语言模型推理框架深度研究与选型指南(vLLM、TensorRT‑LLM、Ollama、TGI、LMDeploy、FastChat、ExLlama)

## 执行摘要与结论预览

本研究面向生产级大语言模型(LLM)服务,系统梳理了七个主流开源推理框架——vLLM、TensorRT‑LLM、Hugging Face Text Generation Inference(TGI)、Ollama、LMDeploy、FastChat、ExLlama——在架构设计、性能取舍、部署复杂度与生态适配上的关键差异,并给出按硬件与业务形态的选型建议。核心结论如下。

第一,内存与KV缓存管理是吞吐与并发的根基。vLLM以PagedAttention为核心,通过分页式KV缓存与虚拟到物理映射、近零碎片与前缀共享,在高并发与长上下文场景下显著提升吞吐并降低内存浪费,从根本上改善“批不大、尾延迟高”的问题[^6][^7][^8]。在公开技术讲解与案例中,传统系统KV缓存浪费可高达60–80%,而PagedAttention通过块级管理将浪费压至极低水平;在部分基准中,vLLM相对传统批处理实现约2倍请求吞吐提升[^7][^8]。

第二,混合精度与量化是NVIDIA平台的性能杠杆。TensorRT‑LLM围绕Hopper/Blackwell架构提供从FP16/BF16到FP8、NVFP4及INT4/INT8权重仅量化、INT8 KV缓存等完整配方,辅以Q/DQ算子融合与图优化,可在相同延迟下将吞吐推向峰值,或以极低TTFT(首个令牌时间)服务低延迟交互;例如H100上FP8在64并发可达>10,000 tok/s,批大小为1时TTFT可低至<10 ms(以牺牲吞吐为代价)[^1][^2][^14]。

第三,路由器+后端的多后端编排是生产可用性的现实路径。TGI v3在服务层提供HTTP/gRPC、持续批处理、可观测与扩缩容钩子,并通过分块与前缀缓存优化长提示;其可将请求路由至不同后端(如vLLM或TensorRT‑LLM),在多租户与多模型生产中实现SLA与成本的平衡[^4][^5][^10][^9]。

第四,易用与极致的二分在2025年更加清晰。Ollama聚焦本地化一键模型管理与OpenAI API兼容,几乎零工程门槛;但生产高并发与极致吞吐场景下,vLLM/TensorRT‑LMDeploy往往更具优势[^12][^13]。在H100离线批处理的公开对比中,LMDeploy与SGLang的tok/s相近且领先vLLM约29%,但vLLM在生态兼容、跨硬件与部署便利性上的综合均衡性更强[^11]。

选型总览(按场景):
- 单机本地开发与试用:Ollama首选;需要OpenAI兼容API与轻量管控也可用FastChat作为外层服务。
- 多租户在线服务:以TGI为外层路由器+后端(vLLM/TensorRT‑LLM/LMDeploy);按租户与优先级在多后端间调度。
- NVIDIA集群性能调优:TensorRT‑LLM(FP8/FP4/W4A16/SmoothQuant)+工程化Benchmark与图优化;视负载选择低TTFT或高吞吐模式。
- 跨硬件与生态优先:vLLM(OpenAI兼容API、Ray/Python生态);LMDeploy在H100上以TurboMind+C++路径亦具备强竞争力。

关键数据亮点:
- vLLM社区2024年快速增长:GitHub Stars 14k→32.6k(2.3x),贡献者190→740(3.8x),月下载6k→27k(4.5x),量化部署占比>20%[^9]。
- H100离线批处理:LMDeploy≈16,132 tok/s,SGLang≈16,215 tok/s,领先优化后的vLLM(≈12,553 tok/s)约29%[^11]。
- TensorRT‑LLM FP8:H100上>10,000 tok/s(64并发),TTFT≈100 ms;批1低TTFT模式<10 ms(吞吐代价)[^1][^14]。

需特别指出的信息缺口:ExLlama缺少权威、可复现的公开基准与社区活跃度数据;TGI v3在标准化长提示场景下的系统化基准亦有待补充;Ollama在生产高并发下的可复现吞吐/延迟数据较少;各框架在AMD/Intel GPU上的定量对比不充分;多租户公平调度与跨后端SLA实证案例仍需更多公开材料支撑(详见“研究范围、方法与证据来源”与“风险、限制与未来趋势”章节中的说明)。


## 研究范围、方法与证据来源

本研究以截至2025-12-14的公开信息为时间基准,覆盖以下框架:vLLM、TensorRT‑LLM、Ollama、Text Generation Inference(TGI)、LMDeploy、FastChat、ExLlama。信息来源包括官方文档与代码库、学术论文、技术博客/基准文章、生产实践报道与社区讨论。评价维度聚焦五项:性能(吞吐/延迟/TTFT)、部署复杂度、社区活跃度、适用场景与技术创新。

证据分级遵循“学术论文/官方文档 > 大型厂商技术博客/基准 > 社区文章/讨论”的原则。对于第三方基准,本文在引用时明确其适用范围与潜在偏差。例如,H100上的离线批处理tok/s对比(LMDeploy/SGLang/vLLM)来自AIMultiple的公开基准[^11];vLLM相对传统系统在请求吞吐上的提升数据引用自技术讲解与PagedAttention原始论文[^7][^6];TensorRT‑LLM的FP8/FP4等精度配方与性能模式引用自官方文档与基准总览[^1][^2][^14]。需要强调的是,不同基准在数据集、提示分布、并发设定与精度配置上差异显著,本文在呈现数字时尽可能给出上下文并在“性能对比与基准解读”章节进行解释。

信息缺口(摘录):
- ExLlama:缺少与同代框架的系统化、可复现公开基准与社区活跃度数据;
- TGI v3:在“20万+长提示”之外、更贴近实务的标准化基准仍不足;
- Ollama:高并发生产负载下的可复现吞吐/延迟数据相对稀缺;
- 跨硬件(AMD/Intel GPU):统一工作负载下的定量对比不充分;
- 多租户SLA与跨后端路由策略:大规模生产SLA与公平调度的实证仍需补充。


## 推理引擎核心技术原理

在LLM服务中,生成阶段的计算图由大量解码步组成。每一步都需要读取此前所有令牌的键值(KV),使得KV缓存的访存与存储成为系统瓶颈。随着并发上升与上下文增长,KV缓存容易产生外部碎片、冗余复制与低效共享,导致批处理规模受限与尾延迟抬升。解决路径分为两条:一是以分页式内存管理降低碎片与提升共享(如PagedAttention);二是以持续批处理与优先级调度平衡吞吐与延迟;三是在NVIDIA平台上以混合精度与量化释放算力与带宽潜力(FP8/FP4、INT8/INT4等);四是在服务层以分块与前缀缓存处理长提示;五是以C++内核与零拷贝路径减少Python层开销与调度成本[^6][^7][^1][^4][^11]。

为便于概览,以下矩阵总结了各框架在关键优化维度的覆盖情况。为避免误读,需结合后文各框架小节的上下文理解其实现细节与适用边界。

表1 技术优化覆盖矩阵(框架 × 优化维度)
| 框架 | 分页KV/块式KV | 前缀缓存 | 持续批处理 | 量化(权重/激活/KV) | 多后端/可插拔 | OpenAI兼容API |
|---|---|---|---|---|---|---|
| vLLM | 是(PagedAttention) | 支持前缀共享 | 是 | 以生态集成与外部工具为主 | 可通过外部路由/编排集成 | 是(HTTP服务器) |
| TensorRT‑LLM | 是(可配置布局与分页) | 取决于构建 | 是 | FP8/FP4/INT8/INT4,权重仅量化和KV量化 | 借助Triton/Ray等编排 | 非默认(可经外层适配) |
| TGI v3 | 支持分块与前缀缓存 | 是 | 是 | 依赖后端(如vLLM/TensorRT‑LLM) | 是(路由器+后端) | 是 |
| LMDeploy | 是(块式KV) | 自动前缀缓存 | 是(持久批处理) | AWQ/GPTQ、INT8 KV、4bit等 | 通过代理与路由扩展 | 需自建或外层提供 |
| FastChat | 否(侧重服务编排) | 间接 | 由后端决定 | 依赖后端能力 | 是(OpenAI兼容API服务层) | 是 |
| ExLlama | 侧重GPTQ内核优化 | 未强调 | 由宿主框架决定 | 权重仅量化(GPTQ/AWQ) | 依框架集成 | 依宿主框架 |

注:此表依据官方文档与公开技术对比提炼,具体能力以版本为准[^6][^7][^1][^4][^10][^11][^15][^16][^17]。

### KV缓存与分页内存管理(PagedAttention)

vLLM的PagedAttention将KV缓存切分为固定大小的块,通过逻辑到物理的块表映射,打破“连续大块”假设,既避免外部碎片,又天然支持跨序列的前缀共享。块级生命周期管理按需分配、满块追加、对话结束即释放,释放块立即复用于其他请求,配合持续批处理显著提高GPU内存利用率与系统吞吐[^6][^7][^8]。在技术讲解与案例中,传统系统KV缓存浪费比例可高达60–80%,而PagedAttention可将近零浪费;在OPT-1.3B等基准中,vLLM相对传统批处理的请求吞吐提升约2倍[^7][^8]。此外,针对大规模KV的系统化回收与传输优化,学术界亦在探索结构化逐块回收等新方法,以进一步降低长时运行的碎片与搬移成本[^22]。

### 量化与混合精度(NVIDIA栈)

TensorRT‑LLM提供覆盖FP16/BF16/FP8( Hopper)/NVFP4( Blackwell)的精度与量化策略,并支持权重仅量化(W4A16/W8A16)、SmoothQuant W8A8以及INT8/FP8 KV缓存。其依赖TensorRT的Q/DQ算子融合、图优化与张量核加速,在保证精度的前提下显著提升吞吐或降低TTFT。量化缩放支持per-tensor/per-token/per-channel及其组合,覆盖AWQ、GPTQ等主流权重仅量化路径,并提供多模型支持矩阵[^1][^2]。在工程实践中,FP8相较FP16在部分算子上可带来明显提速;结合引擎构建与并发调优,可在H100上获得>10,000 tok/s的输出速率,同时TTFT维持在百毫秒量级;若将批大小降至1并针对延迟优化,TTFT可进一步压至<10 ms,但会以牺牲吞吐为代价[^14]。

### 持续批处理与调度

持续批处理(continuous/in-flight batching)允许请求在到达后即刻参与批次计算,避免排队等待批次凑满,从而降低平均等待与尾延迟。vLLM与TensorRT‑LLM、TGI、LMDeploy均在不同层面实现了该能力。vLLM将PagedAttention与持续批处理结合,在高并发下维持较高GPU利用率与稳定尾延迟[^7];TensorRT‑LLM在NVIDIA平台上通过图优化与算子融合进一步放大批处理收益[^1];TGI在服务层提供持续批处理并与分块/前缀缓存协同,降低长提示的预填充成本[^4];LMDeploy通过持久批处理、动态拆分与融合以及高性能CUDA内核,在H100离线批场景下取得领先的tok/s表现[^10][^11]。

### 长提示处理与缓存(分块与前缀缓存)

当提示长度达到数十万甚至百万级别时,单次预填充的计算与内存压力陡增。TGI v3以分块(prefill chunking)将长提示切分为可管理段,并通过前缀缓存复用跨轮共享的常量上下文,从而显著缩短“首轮预填充”耗时并提升GPU内存的有效载荷。在公开对比中,TGI v3处理20万+令牌长提示的速度约为vLLM的13倍,且在相同GPU内存下可容纳约3倍的令牌,缓存查找开销可忽略[^4]。这类“路由器+后端”的服务层优化与后端的分页KV策略互补:前者解决“进水管粗细”,后者解决“水库地基与分格”。

### 跨框架内核与架构(C++ vs Python生态)

H100上的基准显示,LMDeploy(纯C++ TurboMind)与SGLang(强调原生内核优化)在离线批处理tok/s上相近且领先vLLM约29%,差距更多来自引擎编排与内核路径选择,而非数学核心本身[^11]。这印证了“Python+融合核”与“纯C++引擎”在顶端硬件上皆可达峰值的结论。FastChat则定位在“服务与编排层”,以OpenAI兼容API、多模型工作器与控制器为核心,便于在现有后端之上构建多模型与多租户服务[^15][^16]。


## 框架深度剖析

本节从技术创新、性能取舍、部署复杂度、社区生态与典型场景,对七个框架进行剖析。

### vLLM

vLLM的核心创新在于PagedAttention——以分页式KV缓存与虚拟到物理映射、近零碎片与前缀共享,系统性缓解内存浪费与并发受限。与持续批处理的结合使其在相同延迟下显著提升吞吐;在OPT-1.3B等基准中,相对传统批处理方法可达约2倍请求吞吐提升[^7][^8]。在服务层,vLLM提供OpenAI兼容HTTP API,且与Ray Serve等生态良好集成,便于路由与扩缩容。社区方面,2024年Stars增长至32.6k(2.3x)、贡献者740(3.8x)、月下载27k(4.5x),量化部署占比超过20%,反映出其生态与工程成熟度[^9]。典型场景包括:快速原型与跨硬件部署、多租户在线服务(配合外层路由器)、以及需要广泛模型覆盖与生态兼容的生产系统。

### TensorRT‑LLM

TensorRT‑LLM面向NVIDIA GPU深度优化,提供FP16/BF16/FP8( Hopper)/NVFP4( Blackwell)、权重仅量化(INT4/INT8)与INT8/FP8 KV缓存等全套精度与量化配方,辅以Q/DQ算子融合与图优化,将硬件特性“吃干榨尽”[^1][^2]。在H100上,FP8路径可在64并发下实现>10,000 tok/s输出,TTFT约100 ms;若将批大小降至1并启用延迟优化模式,TTFT可低至<10 ms(吞吐下降)[^1][^14]。部署上需构建TensorRT引擎并进行针对性调优,工程复杂度高于通用引擎;但在NVIDIA集群上,若目标为“峰值吞吐”或“低TTFT交互”,TensorRT‑LLM具有明显优势,常与Triton或Ray等编排框架配合构建多租户与多模型服务。

### Text Generation Inference(TGI, v3)

TGI由Rust/Python构成的服务栈,提供HTTP/gRPC、持续批处理、可观测性、自动扩缩容钩子,并在v3引入分块与前缀缓存以优化长提示处理。其“路由器+后端”架构可对接不同引擎(如vLLM、TensorRT‑LLM、LMDeploy),在多租户、多模型与多后端的生产环境中按SLA与成本进行调度;与Hugging Face生态的模型卡、部署工具无缝衔接[^4][^5][^10][^9]。在长提示场景中,TGI v3相对vLLM可取得显著的预填充加速与内存容量优势(20万+提示约13倍加速,容量约3倍),适合作为统一入口与流量编排层[^4]。

### Ollama

Ollama强调“本地化、一键式模型管理与OpenAI API兼容”,覆盖macOS/Windows/Linux,几乎零工程门槛即可在单机上拉起服务。其工程定位偏向“开发与本地试用/私有化”,在生产高并发、极致吞吐与精细调度场景中并非长项[^12][^13]。对于需要快速验证体验、离线轻量应用或隐私优先的团队,Ollama是高效之选;但在多租户在线服务与NVIDIA集群性能调优方面,应与vLLM/TensorRT‑LLM/TGI组合使用。

### LMDeploy

LMDeploy由InternLM团队打造,核心引擎TurboMind为高性能C++后端,支持块式KV、持久批处理、动态拆分与融合、张量并行与高性能CUDA内核,并在量化上支持AWQ/GPTQ与INT8/INT4路径(含KV量化)。在H100离线批处理基准中,LMDeploy与SGLang tok/s相近且领先vLLM约29%,且官方文档宣称4bit推理性能可达FP16的2.4倍(需结合工作负载与模型验证)[^10][^11]。其部署相对简洁(pip/容器),多模型多机多卡可通过代理与路由扩展。适用于需要极致H100性能且兼顾部署简便的生产环境,亦可作为TGI后端之一。

### FastChat

FastChat定位“训练+服务+评估”的开放平台与OpenAI兼容API服务层,采用控制器+模型工作器+Web服务器的架构,天然支持多模型与工作器管理、OpenAI API兼容、评估工具与Chatbot Arena经验沉淀。FastChat并不追求极致的底层内核性能,而是提供与各类后端(vLLM、LMDeploy、ExLlama等)解耦的服务编排能力,适合作为外层API与多模型路由/灰度的生产基座[^15][^16]。

### ExLlama

ExLlama聚焦GPTQ/AWQ等权重仅量化的内核优化与高速推理,常作为其他框架(如FastChat)的后端集成选择。公开资料更多集中在仓库与使用说明层面,缺少权威、可复现的系统化基准与社区活跃度数据,难以与主流引擎在同一维度进行定量比较;工程选型需结合目标模型与宿主框架进行实测。


## 性能对比与基准解读

不同基准间的可比性受到硬件、精度、并发、提示分布与离线/在线模式的共同影响。为降低误读,本节采用“来源-上下文-解读”的方式呈现数据,并给出可迁移性判断。

首先,在H100(80GB)离线批处理设定中,AIMultiple使用Llama 3.1 8B-Instruct与ShareGPT提示对vLLM、LMDeploy、SGLang进行了对比。结果显示SGLang(16,215 tok/s)与LMDeploy(16,132 tok/s)性能相近且领先vLLM(12,553 tok/s)约29%;同时,GPU内存“安全区”约为80%,95%设置会在CUDA Graph编译期间因系统RAM耗尽而崩溃[^11]。这说明在离线批场景下,内核路径与引擎编排对tok/s影响显著,亦提示资源留白对稳定性的重要性。

表2 AIMultiple H100基准(离线批处理,8B-Instruct,BF16,ShareGPT提示)
| 引擎 | tok/s | 备注 |
|---|---:|---|
| SGLang | 16,215 | 与LMDeploy差异<0.6% |
| LMDeploy | 16,132 | 纯C++ TurboMind路径 |
| vLLM | 12,553 | 生态兼容与部署便利性优势 |

其次,Marktechpost的生产级技术对比指出,TGI v3在20万+长提示场景下相对vLLM有约13倍加速,同时在相同GPU内存下可容纳约3倍的令牌;在TensorRT‑LLM侧,H100上FP8可达>10,000 tok/s(64并发),TTFT≈100 ms,批1低TTFT模式<10 ms但吞吐下降[^4]。这些结果指向同一趋势:长提示与多租户生产中,服务层的分块与前缀缓存(TGI v3)与后端的分页KV策略(各引擎)是互补的;而在NVIDIA平台上,混合精度与量化是吞吐/TTFT的主要杠杆。

表3 长提示处理与FP8性能摘要(TGI v3 vs vLLM;TensorRT‑LLM FP8模式)
| 指标 | 数值 | 场景/设定 |
|---|---:|---|
| TGI v3 vs vLLM(20万+提示) | 13× 更快 | 长提示预填充 |
| GPU内存容量(同GPU,TGI v3) | 3× 令牌数 | 长上下文 |
| TensorRT‑LLM FP8 tok/s(H100) | >10,000 | 64并发 |
| TensorRT‑LLM TTFT(FP8) | ≈100 ms | 64并发 |
| TensorRT‑LLM TTFT(批1) | <10 ms | 低TTFT模式(吞吐下降) |

第三,社区讨论亦印证了“场景差异”的直觉:在较低QPS下TGI可能略快,而在较高QPS下vLLM更具优势;该结论属于经验性观察,适用于方向性判断,具体表现仍需按本地工作负载与配置复现实验[^19]。此外,在更大范围的工程实践中,选择推理引擎还需考虑运维复杂度与生态适配度[^20][^21]。

基准迁移性建议:
- 在线与离线:在线场景的TTFT、尾延迟与队列波动对调优方向影响更大;离线批场景更关注tok/s与成本。
- 硬件差异:在不同GPU/精度/并发下,FP8/FP4与W4A16等量化收益差异明显,需以官方Precision矩阵与本地实测为准[^1]。
- 工作负载:提示长度分布与并发峰值直接决定“分块/前缀缓存”与“分页KV”的收益幅度。


## 部署复杂度与工程实践

工程复杂度主要来自四类工作:量化与引擎构建、路由与多后端编排、资源安全与稳定性、以及生态与API兼容。

- 量化与引擎构建:TensorRT‑LLM需要对目标GPU构建引擎并选择量化配方(FP8/FP4/W8A8/W4A16/INT8 KV等),涉及Q/DQ算子融合、图优化与并发策略;不同模型的量化支持矩阵与缩放模式需以官方文档为准[^1]。LMDeploy提供AWQ/GPTQ与KV量化,4bit推理可达FP16的2.4倍(需按模型与负载验证),安装与部署相对简洁[^10]。
- 路由与多后端编排:TGI v3作为路由器+模型服务器,面向多租户与多模型服务,支持将请求路由至不同后端(如H100上的TensorRT‑LLM与低优先级CPU/小型GPU),并提供可观测性与自动扩缩容钩子;与vLLM的OpenAI兼容API与Ray集成、FasChat的服务层组合可形成“控制平面+数据平面”的生产体系[^4][^5][^16]。
- 资源安全:在H100离线批场景中,GPU内存利用率过高(95%)在CUDA Graph编译期间会因系统RAM耗尽导致崩溃,“80%安全区”是工程经验值;多进程/多模型的NUMA与PCIe拓扑亦需纳入压测范围[^11]。
- 生态与API:vLLM与FastChat提供OpenAI兼容API;TGI提供HTTP/gRPC与可观测性钩子,便于纳管与灰度[^5][^16]。

表4 部署复杂度评分(相对量表)
| 框架 | 安装 | 量化/构建 | 调优 | 运维 | 备注 |
|---|---|---|---|---|---|
| vLLM | 低 | 中 | 中 | 低 | 生态广,PagedAttention即插即用 |
| TensorRT‑LLM | 中 | 高 | 高 | 中 | NVIDIA硬件极致性能路径 |
| TGI v3 | 中 | 低 | 中 | 低 | 路由器+后端,多租户生产友好 |
| LMDeploy | 低 | 中 | 中 | 低 | TurboMind C++内核,H100性能强 |
| FastChat | 低 | 低 | 低 | 低 | OpenAI兼容服务层 |
| Ollama | 极低 | 低 | 低 | 极低 | 本地化一键管理 |
| ExLlama | 中 | 中 | 中 | 中 | 依赖宿主框架 |

注:评分用于反映相对工程工作量,实际复杂度随团队经验与目标负载而变。


## 社区活跃度与生态成熟度

社区与生态不仅影响“能否用好”,更决定“能否长期稳定用”。2024年vLLM在GitHub Stars、贡献者与月下载量上均实现倍数级增长,量化部署占比超过20%,显示出强大的生态吸引力与工程信心[^9]。TGI与Hugging Face生态深度耦合,路由器+后端的设计契合企业多租户生产;FastChat沉淀了Chatbot Arena与多模型服务经验,适合作为统一服务层;LMDeploy围绕TurboMind与量化工具链形成面向生产的高性能路径;TensorRT‑LLM背靠NVIDIA硬件与算子/图优化能力,是NVIDIA集群上追求峰值性能与低TTFT的不二之选[^5][^15][^16][^1][^9]。

表5 社区活跃度指标(vLLM)
| 指标 | 2024年初 | 2024年末 | 增幅 |
|---|---:|---:|---:|
| GitHub Stars | 14,000 | 32,600 | 2.3x |
| 贡献者 | 190 | 740 | 3.8x |
| 月下载量 | 6,000 | 27,000 | 4.5x |

注:其他框架的官方量化活跃度数据在本研究信息范围内未形成统一口径,故不展开列示,结论基于文档与生态观察[^5][^15][^16][^1][^9]。


## 场景化选型建议

面向决策,应从“硬件约束—负载形态—SLA目标—工程复杂度—生态依赖”五个维度综合权衡。下表提供按典型场景的推荐组合。

表6 选型决策矩阵
| 场景 | 推荐组合 | 核心理由 | 注意事项 |
|---|---|---|---|
| 单机本地开发/试用 | Ollama;FastChat | 一键模型管理、OpenAI API兼容、快速上手 | 非极致吞吐与并发;生产需上切vLLM/TensorRT‑LLM |
| 多租户在线服务 | TGI(路由)+ vLLM/TensorRT‑LLM/LMDeploy | 路由器+后端架构;分块与前缀缓存;可观测与扩缩容 | 明确后端SLA与优先级;监控TTFT/尾延迟 |
| NVIDIA集群性能调优 | TensorRT‑LLM(FP8/FP4/W4A16/SmoothQuant) | 硬件深度优化;峰值吞吐与低TTFT模式 | 引擎构建/图优化/并发调优;基准与压测 |
| 跨硬件与生态优先 | vLLM;LMDeploy | 跨GPU/框架兼容;OpenAI API与生态集成 | 某些场景tok/s低于LMDeploy/SGLang;合理设置GPU安全区 |
| 高并发聊天/对话 | vLLM或LMDeploy + TGI | 持续批处理+分页KV;路由分优先级 | 防止GPU内存过高导致CUDA Graph编译失败(80%安全区) |
| 长提示RAG/长上下文 | TGI v3(分块+前缀缓存)+ vLLM/TensorRT‑LLM | 预填充加速与容量扩展;后端分页KV配合 | 监控缓存命中与分块策略;防止尾延迟放大 |


## 风险、限制与未来趋势

- 基准可信度与复现性:第三方基准受数据集、提示分布、并发与精度影响较大;建议在本地以固定工作负载与参数复现,并将TTFT、尾延迟与单位成本纳入观测[^11][^4]。
- 工程稳定性:过高GPU内存占用(如95%)在CUDA Graph编译阶段可能触发系统RAM耗尽崩溃;建议预留80%安全区并进行多进程拓扑压测[^11]。
- 多租户SLA与公平调度:不同后端的量化与精度策略影响SLA达成;跨后端路由的优先级与抢占需结合业务等级与成本权衡。
- 趋势判断:以PagedAttention为代表的分页式内存管理与结构化回收(如PagedEviction)将继续演进;混合精度将随Blackwell与后续架构进一步下沉到KV缓存与更细粒度算子;路由器+多后端的“服务层优化+后端极致化”将成为生产默认范式之一[^22][^1][^4]。


## 附录:术语表与参考链接索引

术语表(摘录)
- PagedAttention:将KV缓存分页并以块表进行虚拟到物理映射的注意力机制,实现近零碎片与前缀共享,显著提升并发与吞吐[^6]。
- TTFT(Time To First Token):首个令牌时间,衡量交互延迟的关键指标。
- KV缓存:存储历史令牌的键值,避免重复计算注意力,随上下文线性增长。
- 权重仅量化(Weight‑only):仅对权重进行低比特量化,激活保持高精度;常见于W4A16/W8A16。
- SmoothQuant W8A8:对激活与权重量化到INT8的量化方法,兼顾精度与速度[^1]。
- FP8/NVFP8:8位浮点精度,NVIDIA Hopper开始支持;Blackwell引入NVFP4等更低精度[^1]。
- Q/DQ:Quantize/Dequantize算子,TensorRT中用于量化与反量化的图级融合与优化[^1]。

参考链接索引(按主题)
- 内存/KV与分页:vLLM设计与PagedAttention论文[^6][^7];PagedEviction研究[^22];vLLM年度回顾(生态)[^9]。
- 量化与精度:TensorRT‑LLM数值精度文档与性能总览[^1][^2];FP8实战经验[^14]。
- 基准与性能:H100 tok/s对比(AIMultiple)[^11];生产级技术对比(Marktechpost)[^4];vLLM与TGI对比(Modal)[^10];社区讨论(Reddit)[^19];引擎选择实务(Red Hat)[^21]。
- 框架官方入口:vLLM[^3]、TensorRT‑LLM[^17]、TGI[^5][^18]、LMDeploy[^10]、FastChat[^16]、ExLlama[^17]。


---

## 参考文献

[^1]: Numerical Precision — TensorRT‑LLM. https://nvidia.github.io/TensorRT-LLM/reference/precision.html  
[^2]: Overview — TensorRT‑LLM Performance. https://nvidia.github.io/TensorRT-LLM/performance/perf-overview.html  
[^3]: vLLM — GitHub. https://github.com/vllm-project/vllm  
[^4]: vLLM vs TensorRT‑LLM vs HF TGI vs LMDeploy — Marktechpost. https://www.marktechpost.com/2025/11/19/vllm-vs-tensorrt-llm-vs-hf-tgi-vs-lmdeploy-a-deep-technical-comparison-for-production-llm-inference/  
[^5]: Text Generation Inference — Hugging Face Docs. https://huggingface.co/docs/text-generation-inference/en/index  
[^6]: Efficient Memory Management for LLM Serving with PagedAttention — arXiv. https://arxiv.org/abs/2309.06180  
[^7]: The Architecture Behind vLLM: How PagedAttention Improves Memory Utilization — Medium. https://medium.com/@mandeep0405/the-architecture-behind-vllm-how-pagedattention-improves-memory-utilization-2f9b25272110  
[^8]: Paged Attention — vLLM Docs. https://docs.vllm.ai/en/latest/design/paged_attention/  
[^9]: vLLM 2024 Retrospective and 2025 Vision. https://blog.vllm.ai/2025/01/10/vllm-2024-wrapped-2025-vision.html  
[^10]: vLLM vs. TGI — Modal Blog. https://modal.com/blog/vllm-vs-tgi-article  
[^11]: LLM Inference Engines: vLLM vs LMDeploy vs SGLang — AIMultiple. https://research.aimultiple.com/inference-engines/  
[^12]: Ollama — Official Site. https://ollama.com/  
[^13]: Ollama vs. vLLM — Red Hat Developers. https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking  
[^14]: 33% faster LLM inference with FP8 quantization — Baseten. https://www.baseten.co/blog/33-faster-llm-inference-with-fp8-quantization/  
[^15]: Integrating and Scaling LLMs with FastChat — PyImageSearch. https://pyimagesearch.com/2024/08/19/integrating-and-scaling-large-language-models-with-fastchat/  
[^16]: FastChat — GitHub. https://github.com/lm-sys/FastChat  
[^17]: ExLlamaV2 — GitHub. https://github.com/turboderp/exllamav2  
[^18]: Text Generation Inference — GitHub. https://github.com/huggingface/text-generation-inference  
[^19]: Which is faster — vLLM, TGI or TensorRT? — Reddit. https://www.reddit.com/r/LocalLLaMA/comments/1cb8i7f/which_is_faster_vllm_tgi_or_tensorrt/  
[^20]: LLM inference server performances comparison — llama.cpp Discussions. https://github.com/ggml-org/llama.cpp/discussions/6730  
[^21]: Choosing the right LLM inference engine — Red Hat Developers. https://developers.redhat.com/articles/2025/09/30/vllm-or-llamacpp-choosing-right-llm-inference-engine-your-use-case  
[^22]: PagedEviction: Structured Block-wise KV Cache Pruning — arXiv (2025). https://arxiv.org/html/2509.04377v1