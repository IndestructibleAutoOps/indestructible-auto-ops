# 轻量化和边缘部署的开源推理解决方案:量化技术、轻量化模型、移动端框架、推理优化与专用硬件适配

## 1. 执行摘要与结论先导

在移动与边缘设备上部署开源模型,技术路线的核心取舍可以归结为四个维度:时延、能耗、内存占用与精度保持。本文围绕量化(INT8/INT4/FP16)、轻量模型(Phi-4-mini、MiniCPM 等)、移动端框架(ONNX Runtime、TensorFlow Lite、Core ML、NCNN)与专用硬件(NPU/DSP 等)加速,给出工程可执行的选型与组合优化策略。

首先,量化是轻量化与端侧部署的首要抓手。实践表明,后训练量化(Post-Training Quantization,PTQ)能够以较低成本迅速压缩模型;量化感知训练(Quantization-Aware Training,QAT)在更低比特(如 INT4)时能显著抑制精度下滑。以 3B 规模语言模型为例,BF16 约 6GB,经 4-bit PTQ 可降至约 2.1GB,进一步采用 GGUF q4_k_m 格式约 1.88GB,整体压缩约 68–69%,在通用学术评测(如 MMLU)上保持可接受的精度水平;但若任务敏感或算子对量化较敏感,INT8 往往比 INT4 更稳健,需结合校准数据与混合精度策略择优落地[^1][^4][^5][^6][^7]。

其次,轻量化模型为端侧带来更高的“能效—延迟—内存”性价比。Microsoft Phi-4-mini(3.8B)支持 128K 上下文,面向指令遵循与安全加固,在多项评测中表现优于同尺寸开源模型;OpenBMB 的 MiniCPM 系列通过稀疏注意力、QAT 与推理系统优化,在端侧实现显著解码加速与跨平台适配,适合作为手机、AIPC 与嵌入式平台的“小而强”主力模型[^14][^15][^16][^17][^18][^19]。

第三,框架层面建议优先采用 ONNX Runtime(ORT)作为跨平台统一推理路径。ORT 提供丰富的执行提供程序(Execution Provider,EP)以对接 NNAPI、QNN、CoreML、XNNPACK、OpenVINO 等硬件加速通道,并配套图优化、Float16/混合精度与 Transformers 优化器、Olive 端到端优化工具;在移动端落地中,配合 TFLite、Core ML 与 NCNN 的工具链与后端,形成“模型—格式—EP”的组合优化闭环[^8][^9][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30]。

第四,专用硬件适配是获得能效与尾延迟 SLO 的关键。NPU 原生支持 INT8/INT4、低比特推理,并通过本地暂存器、智能预取、数据流感知 DMA 与图编译实现高吞吐与低能耗;DSP 适合信号处理类任务与确定性低时延场景。在端侧生成式 AI 中,采用 CPU+iGPU+NPU 的异构协同并结合图融合与流水线调度,可有效提升峰值与平均性能[^31][^32][^33][^34][^35][^36][^37]。

基于上述分析,我们给出三类典型场景的推荐基线:
- 手机端(Android/iOS):Phi-4-mini(3.8B)或 MiniCPM-2B/4B 作为 SLM 首选;采用 ORT + NNAPI/QNN(Android)或 CoreML(iOS)作为统一推理路径;在算子敏感层保留 FP16 或 INT8,整体以 PTQ 为主,必要层 QAT 纠偏;在 GPU 可用时引入混合精度与图优化[^8][^20][^21][^22][^25]。
- AIPC(PC 端):优先选择 MiniCPM-4/4.1(8B)或 MiniCPM-2B,结合 Intel OpenVINO 或 NVIDIA TensorRT(若环境可用)进行图级优化与 INT8 量化;在 Windows/Linux 上通过 ORT-EP 组合获得稳定加速与易维护性[^9][^15]。
- MCU/边缘 SoC:采用 TFLite 与 NCNN,优先 INT8 量化与结构化剪枝,利用 NNAPI、RKNPU 或其他供应商 EP 进行硬件加速;如需进一步能效优化,考虑 Ceva 等 NPU IP 的图编译与稀疏利用[^2][^6][^24][^26][^31]。

为确保工程落地质量,建议建立统一的评测基线与观测指标:
- 指标:时延(P50/P90)、吞吐(tokens/s 或 FPS)、内存峰值与模型体积、能效(Joules/Token 或 Joules/Image)、精度(任务特定指标)、尾延迟 SLO 达成率;
- 场景:空闲/中载/重载与多线程配置下的稳定性;
- 回归:版本升级或 EP 切换后进行 A/B 测试与性能-精度回归。

需要说明的是,本文在若干关键处存在信息缺口:例如 Qwen2 在移动端推理的系统化官方基准尚待补充;TensorFlow Lite 端到端 INT8 校准流程的细化步骤在当前材料中不完整;跨框架、跨硬件的统一端侧基准数据不足;部分 NPU/DSP 的 TOPS 与实测能效缺乏可核验矩阵。我们在相应章节中予以标注,并给出后续补齐建议[^1][^2][^6]。

## 2. 方法与评估框架

边缘 AI 的成功落地取决于数据、模型与系统三层的协同优化。本文采用综合调查所述的“优化三元组”方法论:在数据侧强调清洗、增强与压缩,提升有效信息密度与泛化;在模型侧通过量化、剪枝、蒸馏、低秩分解与紧凑架构设计(含 NAS)实现结构效率;在系统侧利用推理框架与硬件执行通道进行图级优化与算子调度,从而在端侧约束下达成目标性能与能效[^3][^2][^6]。

评估指标建议包括:
- 时延分布:P50、P90 与尾延迟,尤其在交互式生成任务(如 LLM 解码)中至关重要;
- 吞吐:tokens/s(LLM)或 FPS(视觉);
- 内存峰值与模型体积:前者影响稳定性与并发,后者影响下载/更新与存储成本;
- 能效:单位工作量能耗,适用于长时间运行与移动设备场景;
- 精度:任务级指标(如 MMLU、GSM8K 等学术基准或业务 KPI);
- 稳定性:多线程、异构执行与热升级下的波动与回归。

测试工况应覆盖:
- 设备与 OS:Android、iOS、Linux(嵌入式/AIPC/边缘盒子);
- 线程数与负载:空闲/中载/重载下的时延与能耗曲线;
- 加速后端:NNAPI/QNN/CoreML/XNNPACK/OpenVINO/TensorRT 等;
- 版本回归:框架与 EP 升级后的 A/B 对比。

合规与安全方面,端侧部署强化隐私与数据驻留优势,但仍需关注模型与数据的版本治理、访问审计与加密,以及在异构环境下 EP 回退策略的正确性与可验证性[^2][^3]。

## 3. 量化技术综述(INT8、INT4、FP16)

量化的核心是将浮点参数与激活转换为更低比特的表示,以降低内存、带宽与计算开销。其基本公式可理解为 q = round(r/s) + z,其中 r 为原始浮点值,s 为尺度,z 为零点;通过合理选择量化区间与阈值,可以在压缩与精度之间取得平衡[^1]。工程路径通常先易后难:优先 PTQ 以快速收益,必要时对敏感层保留更高精度(混合精度),在极低比特或任务对量化较敏感时引入 QAT 进行纠偏与稳健化[^4][^5]。

在不同比特位宽下,FP16 提供约 2 倍压缩(相对 FP32),通常精度影响很小;INT8 约 4 倍压缩,精度影响适中且更稳健;INT4 约 8 倍压缩,精度下滑更明显,需要更精细的校准与 QAT;低于 4-bit 的方案通常仅适用于特定任务或对误差不敏感的场景[^1][^2][^6]。在端侧生态中,TFLite、ONNX、NCNN 与 CoreML 对量化有不同程度的支持,配合校准数据与图优化可获得显著收益[^2][^6][^26]。

为便于决策,下表给出常见精度级别的压缩与精度影响的经验对比(以 3B 规模 LLM 案例为参考)。

表 1 量化级别对比:精度—压缩—适用性(以 3B LLM 为例)

| 精度级别 | 压缩比(相对 FP32) | 精度影响(经验区间) | 典型适用场景 | 生态支持要点 |
|---|---:|---|---|---|
| FP16 | ≈2× | 可忽略(<1% 困惑度增加) | 高端设备、对精度敏感任务 | ORT Float16/混合精度、CoreML GPU 推理[^9][^28] |
| INT8 | ≈4× | 适中(2–5% 困惑度增加) | 中端手机、AIPC;主力端侧推理 | TFLite 整数量化、ORT 量化、QNN/NNAPI 加速[^4][^7][^21][^22] |
| INT4 | ≈8× | 更显著(5–15%,视策略) | 内存严格受限设备;极小模型 | 需校准+混合精度;QAT 纠偏;硬件支持差异化[^1][^2][^6] |
| <4-bit | >8× | 通常显著退化 | 特定任务/窄域场景 | 谨慎评估,常与蒸馏/剪枝/架构优化组合[^2] |

从表 1 可见,INT8 在端侧的综合性价比通常更优;INT4 在压缩率上更具吸引力,但需要更强的工艺(校准数据质量、敏感层保留、QAT)来抑制精度回退。FP16 在高端设备与对误差敏感的任务中仍具价值,尤其与 GPU/Apple 设备上的混合精度推理配合使用。

为进一步量化压缩收益,以下以 Llama 3.2 3B 为例展示 BF16→4-bit→GGUF(q4_k_m)的体积变化。

表 2 3B LLM 量化示例(BF16→4-bit→GGUF q4_k_m)

| 模型/格式 | 体积(GB) | 压缩率(相对 BF16) | 典型评测(示例) |
|---|---:|---:|---|
| Llama 3.2 3B(BF16) | 6.00 | — | 原始精度基线 |
| 4-bit 量化(PTQ) | ≈2.10 | ≈64.9% 减少 | 精度较基线略有下滑 |
| GGUF q4_k_m | 1.88 | ≈68.7% 减少 | MMLU ≈61.8%;Perplexity(Wikitext2)≈8.57[^1] |

从表 2 可见,GGUF q4_k_m 在不损失主要功能的前提下显著降低内存与存储压力,适合移动端下载与驻留;但在具体业务中,需针对任务指标进行 A/B 验证,以决定是否对关键层保留更高精度或切换至 QAT。

在工具链与流程方面:
- TFLite:提供训练后整数量化与动态范围量化、FP16 量化,以及量化感知训练(QAT);QAT 在模拟低比特推理的同时训练修正权重,有利于最终生成真正量化的模型并缓解精度下滑[^4][^5]。
- ONNX Runtime:提供量化、Float16 与混合精度、图优化与 Transformers 优化器,支持将量化模型通过不同 EP 加速到 NNAPI、QNN、CoreML、XNNPACK、OpenVINO 等后端;Olive 工具可用于端到端优化流程[^7][^9]。
- NCNN:在 ARM 上进行 NEON 级优化,支持 8-bit 量化与半精度存储,适合手机端极致轻量推理[^26]。

### 3.1 FP16 与混合精度

FP16 在拥有 GPU 或 Apple 设备加速的场景中常常作为“低成本压缩”的第一选择。它在保持较高精度的同时,将模型体积与内存占用减半,并在支持半精度运算的硬件上提升吞吐。对于生成式任务中一些对误差敏感层(如归一化、嵌入层或小型分类头),与 INT8/INT4 的混合精度策略能够在不显著牺牲质量的情况下降低整体成本。ORT 的 Float16/混合精度优化与 Core ML 在 Apple 设备上的加速能力,为工程团队提供了现成路径[^9][^28]。

### 3.2 INT8:主力端侧精度-效率折中

INT8 以其稳健的工程特性成为端侧部署的主力选择。其优势在于压缩比适中、生态完善、硬件支持成熟;在图像分类、目标检测、语音与中小型语言模型中,往往只需少量校准数据与阈值调优即可达成可接受精度。TFLite 的训练后整数量化(PTQ)流程与 ORT 的量化优化,使端侧应用能够通过 NNAPI、QNN、XNNPACK、OpenVINO 等后端获得可观的时延与能耗改善[^4][^7][^21][^22]。

### 3.3 INT4 与更低比特:极致压缩的边界

INT4 在极低内存设备或超小模型上具有吸引力,但需谨慎处理精度回退与算子不兼容。最佳实践包括:提升校准数据的覆盖与质量;对敏感层保留 INT8 或采用混合精度;在低比特下引入 QAT 进行权重修正;并通过图融合与流水线调度减少访存与尾延迟。端侧场景的学术与产业研究正在推动 4-bit 更广泛落地,但在通用生成式任务中仍建议以任务级 A/B 验证与能耗观测为决策依据[^1][^2]。

## 4. 轻量化模型盘点(Phi-4-mini、MiniCPM、Qwen2 等)

轻量化模型(Small Language Models,SLMs)在端侧的价值在于:更小的内存与存储占用、更低的时延与能耗、以及在大多数通用任务中可接受的精度。它们的成功往往来自高质量训练数据、针对效率的架构设计与推理系统优化。

Phi-4-mini(3.8B)以高质量、推理密集型数据与安全对齐为特色,支持 128K 上下文与多语言,面向指令遵循与工具调用场景,在 Arena Hard、MMLU、GSM8K、MATH 等指标上优于同尺寸模型,适合移动端与 AIPC 的主力语言模型[^14][^15][^16]。MiniCPM 系列通过可训练稀疏注意力、QAT、推测解码与推理系统(如 CPM.cu 与 ArkInfer)优化,在端侧实现显著解码加速与跨平台适配,并在多项对比中超越更大规模的通用模型,适合在内存受限设备上提供接近大型模型的体验[^17][^18][^19]。Qwen2 家族在 SLM 领域具备影响力,但当前材料缺少其端侧推理的系统化官方基准,建议后续补齐评测矩阵与端侧部署指南。

表 3 轻量模型对比(以代表性指标为例)

| 模型 | 参数量 | 上下文长度 | 代表性评测(示例) | 端侧特性 | 生态/框架支持 |
|---|---:|---:|---|---|---|
| Phi-4-mini-instruct | 3.8B | 128K | MMLU(5-shot)≈67.3;GSM8K(8-shot)≈88.6;MATH(0-shot)≈64.0;总体≈63.5 | 多语言、指令遵循、函数调用;安全对齐 | Transformers 集成;Azure 可用;端侧建议 ORT/TFLite+EP[^14][^15][^16] |
| MiniCPM-4/4.1 | 8B | 32K(可扩展至 128K) | 同尺寸对比中多项领先;解码速度提升(与 Qwen3-8B 对比,Orin 上≈7×) | 稀疏注意力、QAT、推测解码;CPM.cu/ArkInfer | 支持 Transformers、vLLM、llama.cpp、Ollama 等[^17][^18][^19] |
| MiniCPM-2B/2B-128k | 2B | 128K(扩展) | 接近 Mistral-7B 的综合表现(中文/数学/代码更优) | 轻量但能力强,适合手机与嵌入式 | 同上 |
| MiniCPM-S-1B | 1B | — | FFN 层平均稀疏度≈87.89%;FLOPs 减少≈84% | 极致稀疏,适合超低资源设备 | 同上 |

从表 3 可见,Phi-4-mini 在通用推理与指令遵循方面提供了稳健的端侧体验;MiniCPM 通过架构与推理系统优化在速度与能效上更具优势。两者均适合在 Android/iOS 与 AIPC 上通过 ORT 与相应 EP 落地,结合 INT8/FP16 的混合精度策略可获得稳定收益。

### 4.1 Phi-4-mini(3.8B)要点

Phi-4-mini 采用高质量合成与筛选数据,强调推理密集与安全对齐,在多语言理解与数学/逻辑推理上表现突出;128K 上下文增强了长对话与工具调用的可用性,适合在移动端与本地隐私场景中作为主力 SLM。部署建议方面,可在 Android/iOS 上通过 ORT 的 CoreML/NNAPI/QNN 路径加速,并在关键层保留 FP16/INT8 以维持生成质量[^14][^15][^8]。

### 4.2 MiniCPM 系列要点

MiniCPM-4/4.1 在同尺寸模型中实现更强的推理与生成速度,受益于稀疏注意力、长文本扩展与推理系统优化;MiniCPM-2B 在内存受限设备上提供接近更大模型的综合表现;MiniCPM-S-1B 则以极高稀疏度换取超低 FLOPs,适合可接受轻微精度损失的极致轻量场景。部署生态上,支持多种推理后端与工具链,便于跨平台落地与维护[^17][^18][^19]。

## 5. 移动端与边缘推理框架对比(ONNX Runtime、TFLite、Core ML、NCNN)

选择推理框架时,应综合考虑硬件加速能力、量化支持、图优化与生态工具完善度。ONNX Runtime 以跨平台与 EP 丰富著称,适合作为“统一推理路径”,并提供性能分析与调试工具;TensorFlow Lite 在移动端轻量部署与 TFLite Converter、PTQ/QAT 支持方面成熟;Core ML 在 iOS 设备上提供极快性能与完善工具链,并有设备端 LLM 实践;NCNN 在 Android 的 ARM NEON 与 Vulkan 优化上表现突出,适合极致轻量与无第三方依赖的场景[^8][^9][^20][^23][^24][^25][^26][^27][^28][^29][^30]。

表 4 框架能力与硬件兼容矩阵(概览)

| 框架 | 主要平台 | 量化支持 | 可用 EP/加速 | 图优化/工具 | 生态成熟度 |
|---|---|---|---|---|---|
| ONNX Runtime | Android/iOS/Linux/Windows | INT8、FP16、混合精度 | NNAPI、QNN、CoreML、XNNPACK、OpenVINO、TensorRT(供应商 EP) | Transformers 优化器、图优化、Profiling、Olive | 高(跨平台与 EP 丰富)[^8][^9][^20][^21][^22][^23][^24][^25] |
| TensorFlow Lite | Android/iOS/嵌入式 Linux/MCU | PTQ(INT8/动态范围/FP16)、QAT | NNAPI(Android)等 | TFLite Converter、模型优化工具 | 高(移动端经典)[^4][^5][^6] |
| Core ML | iOS/macOS/watchOS/visionOS | Core ML 优化、混合精度 | Apple 设备加速(Metal/BNNSGraph) | Xcode 模型预览与性能洞察、Foundation Models | 高(Apple 生态一体)[^28][^29][^30] |
| NCNN | Android/iOS/Linux | 8bit 量化与半精度存储 | ARM NEON、Vulkan GPU | 纯 C++、无第三方依赖;自定义层扩展 | 高(移动端极致轻量)[^26] |

上述矩阵强调:若需跨平台统一与多 EP 回退,优先 ORT;若聚焦移动端轻量与历史资产,TFLite 仍具优势;在 iOS 上,Core ML 与 Foundation Models 提供更顺滑的开发体验;在 Android 纯轻量与极限优化场景,NCNN 是可靠选择。

### 5.1 ONNX Runtime:跨平台与 EP 生态

ORT 在 IoT/边缘的部署强调“端侧优势”(低时延、隐私、离线、成本节省),同时明确模型与硬件的限制。Android 上建议结合 NNAPI/QNN 加速;iOS 上通过 CoreML EP;通用 CPU 场景可启用 XNNPACK EP;在 x86 平台上,OpenVINO EP 可显著提升性能。ORT 的性能主页、调优指南与分析工具,有助于系统化地排查瓶颈与迭代优化[^8][^9][^20][^21][^22][^23][^24][^25]。

### 5.2 TensorFlow Lite:移动端经典轻量路径

TFLite 的训练后量化(PTQ)与量化感知训练(QAT)覆盖常见移动场景;其 Converter 与优化工具链成熟,配合 NNAPI 加速在 Android 设备上广泛落地。相较 ORT,TFLite 在极简推理与资源占用方面仍具优势,适合纯移动端或对体积敏感的项目[^4][^5][^6]。

### 5.3 Core ML:iOS 设备端高性能选项

Core ML 集成简单、性能优异,配套 Foundation Models、Metal/Accelerate/BNNSGraph 与 MLX,构成完整的端侧数值与推理生态。Apple 的设备端 LLM 实践展示了在 Apple 芯片上达成实时交互性能的可能,为 iOS 应用提供高质量本地智能能力[^28][^29][^30]。

### 5.4 NCNN:极致移动端轻量与 Vulkan/NEON 优化

NCNN 以纯 C++、无第三方依赖与 ARM NEON/Vulkan 优化著称,支持 8bit 量化与半精度存储,直接内存零拷贝加载模型,便于在 Android 上构建轻量高效推理管线;同时兼容多种模型格式(ONNX、Caffe、PyTorch 等)与自定义层扩展,适合性能与体积双敏感的端侧项目[^26]。

## 6. 模型压缩与端侧优化(剪枝、蒸馏、低秩分解、NAS)

边缘推理的优化管线应采用“多策略组合”:剪枝用于减少冗余结构与 FLOPs;蒸馏用于将大模型知识转移到小模型;低秩分解通过矩阵近似降低参数与计算;NAS 则在约束下自动搜索高效架构。系统层配合图融合、算子内核优化与内存规划,进一步降低访存与尾延迟[^2][^41][^40][^42][^43]。

表 5 优化技术—收益—代价—兼容性(概览)

| 技术 | 预期收益 | 代价/风险 | 框架兼容性与要点 |
|---|---|---|---|
| 结构化剪枝 | 降低 FLOPs 与内存,提升时延与能效 | 可能影响精度;需重训练或 QAT 纠偏 | TensorRT Model Optimizer、NAS 组合;与量化/蒸馏协同[^40][^2] |
| 非结构化剪枝 | 参数减少,模型体积下降 | 硬件加速收益有限(稀疏支持差异) | 需稀疏友好后端;常与量化结合[^2] |
| 知识蒸馏 | 小模型逼近大模型性能 | 蒸馏策略与数据质量敏感 | 视觉与 NLP 通用;与剪枝/量化组合更佳[^41][^43] |
| 低秩分解 | 计算与内存降低 | 需再训练收敛;实现成本高 | 训练期 SVD、Micro-Factorized 卷积等[^2] |
| 量化(PTQ/QAT) | 内存与计算显著降低 | 低比特下精度下滑风险 | TFLite/ORT/NCNN 支持;混合精度与 QAT 纠偏[^4][^5][^7][^26] |
| NAS(硬件感知) | 自动设计轻量架构 | 搜索成本高;结果解释性弱 | MoENAS、RaNAS、QuantNAS 等方法;部署后自适应[^42][^41][^43] |

从表 5 可见,单一技术难以覆盖所有约束,工程上通常将剪枝+蒸馏+量化+NAS 进行组合,并在系统层通过图融合与内存规划获得稳定收益。

### 6.1 剪枝:结构化优先

结构化剪枝(如通道/滤波器级剪枝)在端侧更易转化为时延与能耗收益,因其与硬件内核的计算结构一致;非结构化剪枝虽然能减少参数,但对通用加速器的收益受限,需要稀疏友好后端或额外的重训练/QAT 支持[^40][^2]。

### 6.2 蒸馏与 QAT 协同

蒸馏让学生模型学习教师中间表示,在模型的软标签与端侧配合 QAT 能更好适配低比特量化;针对 Transformer 的蒸馏策略需要关注层间对齐与注意力模块的知识迁移,以避免在长文本与复杂推理任务上出现明显性能回退[^41][^43]。

### 6.3 硬件感知 NAS

硬件感知 NAS 在约束(如延迟、能耗、内存)下自动搜索轻量架构,适合移动/嵌入式设备的专用任务。资源感知(RaNAS)与混合专家(MoENAS)方法可在搜索空间中平衡精度与资源消耗;在部署后场景中,AdaptiveNet 展示了架构后自适应以应对环境与负载变化的可能性[^42][^41][^43]。

## 7. 专用硬件适配(NPU/DSP/FPGA/GPU):算子与图级优化

边缘 SoC 正在从通用计算走向异构专业化:CPU/DSP/GPU/NPU 的组合成为主流;智能内存层次结构与高带宽互连提升数据到达率与内核利用率。NPU 原生支持 INT8/INT4 并通过本地暂存器、智能预取与数据流感知 DMA 减少外存依赖;图编译与稀疏利用进一步提升吞吐与能效。DSP 在信号处理与确定性低时延任务上具备优势;GPU 在并行与灵活性方面表现良好但功耗较高;FPGA 则提供高度可定制与低功耗的可重构加速路径,但开发门槛与成本较高[^31][^32][^33][^36][^37]。

表 6 硬件类型—精度—加速—能效—生态(概览)

| 硬件类型 | 支持精度 | 典型加速路径 | 能效特征 | 生态与工具链 |
|---|---|---|---|---|
| NPU | INT8/INT4(图编译支持混合) | 图融合、稀疏利用、数据流调度、本地暂存 | 高能效,低时延 | Ceva-NeuPro(Studio)、QNN、NNAPI、Vitis AI[^31][^32][^22][^37] |
| DSP | 定点/浮点(供应商相关) | 专用信号处理、确定性时延 | 低功耗,实时性强 | Ceva-XC/SensPro、Hexagon 工具链[^31][^33] |
| FPGA | 自定义(定点/浮点) | 定制数据流与算子 | 低功耗,高灵活性 | 白皮书与供应商工具(Vitis 等)[^36][^37] |
| GPU | FP32/FP16/INT8 | 并行内核、混合精度 | 高吞吐,功耗高 | TensorRT、OpenVINO(Intel GPU)、CoreML GPU[^9][^24][^28] |

从表 6 可见,NPU 是端侧生成式 AI 与视觉推理的主力能效选择;DSP 在音频/通信/传感处理中发挥确定性优势;FPGA 为特定工作负载提供“按需定制”的能效与时延,但工程复杂度高;GPU 则用于高性能与通用加速场景。

### 7.1 NPU 优化要点

面向边缘 NPU 的优化策略包括:图级算子融合以减少内核调度与访存;稀疏性利用(权重与激活稀疏)提升有效计算;混合精度(INT8 主、关键层 FP16/INT4)降低误差;数据流调度与本地暂存规划减少外部内存访问。工具链方面,Ceva-NeuPro Studio、QNN、NNAPI、Vitis AI 提供从模型到可执行图的高效通道[^31][^32][^22][^37]。

### 7.2 DSP/其他加速器的使用建议

DSP 适合信号处理(音频、雷达、通信)与低时延确定性任务,建议在系统架构中作为协处理器与 NPU/CPU 协同;FPGA 在特定算子与定制数据流上可实现极高能效,但需评估开发周期与成本;GPU 用于高并行与高吞吐场景,在移动/边缘设备上应结合功耗管理策略与混合精度优化[^31][^36][^37]。

## 8. 性能-精度权衡与场景化选型建议

将上述技术与框架落入场景,需要从业务目标出发做组合优化与基线评估:
- 手机端(Android/iOS):首选 Phi-4-mini(3.8B)或 MiniCPM-2B/4B;Android 采用 ORT + NNAPI/QNN 与 XNNPACK;iOS 采用 ORT + CoreML 或直接 Core ML;量化以 PTQ 为主、关键层保留 FP16/INT8,必要时引入 QAT;图优化与 Transformers 优化器用于提升解码与预填充速度[^8][^14][^15][^17]。
- AIPC(PC 端):优先 MiniCPM-4/4.1(8B),在 Intel 平台通过 OpenVINO EP 加速;若配备 NVIDIA GPU,则结合 TensorRT 进行图融合与 INT8 量化;在 Windows/Linux 上通过 ORT 统一部署路径与 Profiling 工具,建立 P50/P90 时延与能耗基线[^9][^15]。
- MCU/边缘 SoC:以 TFLite/NCNN + NNAPI/RKNPU 为主,采用 INT8 PTQ 与结构化剪枝;如需更强能效与可控图级优化,评估 NPU IP(如 Ceva-NeuPro)与工具链,实现稀疏利用与数据流调度[^2][^6][^26][^31]。

为帮助快速落地,下面给出场景化基线建议表(不填具体数值,留待项目评测填充)。

表 7 场景—模型—量化—框架—EP—目标(基线表)

| 场景 | 模型 | 量化策略 | 框架与 EP | 目标(待测) |
|---|---|---|---|---|
| Android 手机 | Phi-4-mini(3.8B)或 MiniCPM-2B | INT8 PTQ + 关键层 FP16 | ORT(NNAPI/QNN/XNNPACK) | P50/P90 时延、tokens/s、能耗、精度 |
| iOS 设备 | Phi-4-mini(3.8B)或 MiniCPM-2B/4B | INT8 PTQ + CoreML 加速 | ORT(CoreML EP)/Core ML | 同上 |
| AIPC(Intel) | MiniCPM-4/4.1(8B) | INT8 + 图优化 | ORT(OpenVINO EP) | 同上 |
| MCU/边缘 SoC | MiniCPM-2B/1B 或轻量视觉模型 | INT8 PTQ + 结构化剪枝 | TFLite/NCNN + NNAPI/RKNPU | 同上 |

在执行层面,应建立版本回归机制:框架升级、EP 切换或模型更新后,进行 A/B 测试与精度-性能回归;对尾延迟与能耗进行 SLO 监控,确保交互体验与续航表现。

## 9. 端到端参考工作流与最佳实践

工作流建议从训练→优化→编译→部署→监控闭环管理:
1. 训练/微调:在高质量数据上进行指令微调与对齐,保证基础能力;
2. 量化/剪枝/蒸馏:优先 PTQ;对低比特或敏感任务引入 QAT;结构化剪枝减少 FLOPs;蒸馏提升小模型泛化;
3. 格式转换:转换为 ONNX/TFLite/CoreML/NCNN 等目标格式;
4. 图优化与 EP 选择:启用 ORT 的图优化与 Transformers 优化器;根据平台选择 NNAPI/QNN/CoreML/XNNPACK/OpenVINO;在 TFLite 上使用 PTQ/QAT;在 Core ML 上进行设备端优化;
5. Profiling 与内存/线程调优:使用 ORT 的 Profiling、日志、线程管理与 I/O 绑定;在异构环境中进行核间绑定与亲和性调优;
6. 回归与灰度:建立 P50/P90 与尾延迟 SLO;进行能耗观测与精度回归;采用灰度策略逐步扩大覆盖[^8][^9][^4][^5][^28]。

质量保障方面,建议:
- 精度回归:在关键任务指标与学术基准(如 MMLU、GSM8K)上建立最小可接受阈值;
- 能耗测试:在空闲/中载/重载下记录 Joules/Token 或 Joules/Image;
- 稳定性与兼容性:多线程与异构 EP 回退验证;模型升级与框架版本升级后的回归测试。

## 10. 风险与限制

- 低比特量化的精度风险:INT4 及以下在通用生成式任务中可能产生显著精度回退,需通过混合精度、QAT 与数据质量提升进行缓解;建议以任务级 A/B 验证为准[^1]。
- 硬件差异与 EP 兼容风险:不同设备上的 EP 能力与算子支持差异较大,需在 ORT 中设计回退策略(如 NNAPI→XNNPACK、QNN→CPU),并进行版本回归与性能基准管理[^8]。
- 维护与生态更新风险:框架与工具链升级可能引入性能波动或 API 变更;建议建立持续评测管线与灰度发布机制。
- 合规与隐私:端侧部署虽然强化隐私与数据驻留,但仍需模型/数据访问控制与审计,尤其在跨平台与第三方 EP 场景中[^2]。

## 11. 附录:术语、工具链与参考链接

术语表(择要):
- PTQ/QAT:后训练量化/量化感知训练。前者快速、成本低;后者在低比特下更稳健;
- 混合精度:在不同层或算子上采用不同精度(如 FP16/INT8/INT4);
- EP(Execution Provider):执行提供程序,框架对接硬件加速的后端;
- 图编译/图优化:对计算图进行融合、内存规划与算子调度优化;
- 稀疏性:权重或激活的零值比例提升,用于减少有效计算;
- SLO(Service Level Objective):服务级目标,如尾延迟阈值。

工具链索引:
- 量化与优化:TFLite(PTQ/QAT)、ORT(量化、Float16、图优化、Transformers 优化器、Olive);
- 模型与生态:Phi-4-mini(Microsoft/Hugging Face/Azure)、MiniCPM(OpenBMB);
- 硬件与 EP:NNAPI、QNN、CoreML、XNNPACK、OpenVINO、RKNPU、CANN、ACL/ArmNN、Vitis AI;
- 基准与文档:ORT 性能与 EP 文档、NCNN GitHub、TFLite 模型优化、Edge AI 综合调查。

信息缺口说明:
- Qwen2 轻量化版本的移动端部署与基准需补充官方材料与可复现实验;
- TensorFlow Lite 端到端 INT8 校准流程的细化步骤需结合官方教程补齐;
- 跨框架、跨硬件的统一端侧基准数据(时延/吞吐/能耗/内存)需在项目中建立评测矩阵;
- 部分 NPU/DSP 的 TOPS 与实测能效缺乏可核验数据,需供应商白皮书或第三方评测。

---

## 参考文献

[^1]: Optimizing LLMs Using Quantization For Mobile Execution - arXiv (2512.06490v1). https://arxiv.org/html/2512.06490v1  
[^2]: Optimizing Edge AI: A Comprehensive Survey on Data, Model, and System Optimization - arXiv (2501.03265v1). https://arxiv.org/html/2501.03265v1  
[^3]: Edge AI in Practice: A Survey and Deployment Framework - MDPI Electronics. https://www.mdpi.com/2079-9292/14/24/4877  
[^4]: Post-training integer quantization | Google AI Edge. https://ai.google.dev/edge/litert/conversion/tensorflow/quantization/post_training_integer_quant  
[^5]: Quantization aware training - TensorFlow Model Optimization. https://www.tensorflow.org/model_optimization/guide/quantization/training  
[^6]: Model optimization | Google AI Edge. https://ai.google.dev/edge/litert/conversion/tensorflow/quantization/model_optimization  
[^7]: Quantization — Qualcomm AI Hub documentation. https://workbench.aihub.qualcomm.com/docs/hub/quantize_examples.html  
[^8]: Deploy on IoT and edge - ONNX Runtime. https://onnxruntime.ai/docs/tutorials/iot-edge/  
[^9]: ONNX Runtime Performance. https://onnxruntime.ai/docs/performance/  
[^10]: Performant on-device inferencing with ONNX Runtime. https://opensource.microsoft.com/blog/2023/02/08/performant-on-device-inferencing-with-onnx-runtime  
[^11]: Edge AI: TensorFlow Lite vs. ONNX Runtime vs. PyTorch Mobile - DZone. https://dzone.com/articles/edge-ai-tensorflow-lite-vs-onnx-runtime-vs-pytorch  
[^12]: Benchmark ONNX runtime performance with onnxruntime_perf_test - Arm Learning. https://learn.arm.com/learning-paths/servers-and-cloud-computing/onnx-on-azure/benchmarking/  
[^13]: High performance on-device real-time ML with NimbleEdge, using ONNX Runtime. https://onnxruntime.ai/blogs/nimbleedge-x-onnxruntime  
[^14]: microsoft/Phi-4-mini-instruct - Hugging Face. https://huggingface.co/microsoft/Phi-4-mini-instruct  
[^15]: Phi-4-mini Microsoft Blog. https://aka.ms/phi4-feb2025  
[^16]: Phi-4-mini Technical Report. https://aka.ms/phi-4-multimodal/techreport  
[^17]: OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs. https://github.com/OpenBMB/MiniCPM  
[^18]: MiniCPM-V 4.5: A GPT-4o Level MLLM for Single Image ... - GitHub. https://github.com/OpenBMB/MiniCPM-V  
[^19]: Minicpm4: Ultra-efficient llms on end devices - arXiv. https://arxiv.org/pdf/2506.07900  
[^20]: Execution Providers — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/  
[^21]: Android - NNAPI Execution Provider — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/NNAPI-ExecutionProvider.html  
[^22]: Qualcomm - QNN Execution Provider — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html  
[^23]: Apple - CoreML Execution Provider — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html  
[^24]: Intel - OpenVINO Execution Provider — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/OpenVINO-ExecutionProvider.html  
[^25]: XNNPACK Execution Provider — ONNX Runtime. https://onnxruntime.ai/docs/execution-providers/Xnnpack-ExecutionProvider.html  
[^26]: ncnn: high-performance neural network inference framework - GitHub. https://github.com/Tencent/ncnn  
[^27]: A Comprehensive Benchmark of Deep Learning Libraries on Mobile ... - arXiv. https://arxiv.org/pdf/2202.06512  
[^28]: Machine Learning & AI - Apple Developer. https://developer.apple.com/machine-learning/  
[^29]: On Device Llama 3.1 with Core ML - Apple Machine Learning Research. https://machinelearning.apple.com/research/core-ml-on-device-llama  
[^30]: Deploy machine learning and AI models on-device with Core ML (WWDC24 10161). https://developer.apple.com/la/videos/play/wwdc2024/10161/  
[^31]: Edge AI SoC Design: AI-Driven Silicon IP and NPU IP for AI Inference - Ceva IP Blog. https://www.ceva-ip.com/blog/how-ai-is-redefining-edge-ai-soc-design-and-what-silicon-ip-providers-must-do-for-ai-inference/  
[^32]: Ceva-NeuPro-M product page. https://www.ceva-ip.com/product/ceva-neupro-m/  
[^33]: Accelerate Edge AI with the Hexagon Hardware Support Package - MathWorks. https://blogs.mathworks.com/deep-learning/2025/06/16/accelerate-edge-ai-with-the-hexagon-hardware-support-package/  
[^34]: Real-time Edge-optimized AI powered Parallel Pixel-upscaling - AMD Developer. https://www.amd.com/en/developer/resources/technical-articles/2025/real-time-edge-optimized-ai-powered-parallel-pixel-upscaling-eng.html  
[^35]: Complex Mix Of Processors At The Edge - Semiconductor Engineering. https://semiengineering.com/complex-mix-of-processors-at-the-edge/  
[^36]: FPGA vs. GPU for Deep Learning Applications - IBM. https://www.ibm.com/think/topics/fpga-vs-gpu  
[^37]: Accelerating Edge AI Inference with Vitis AI NPU on iWave's Versal - DigiKey. https://www.digikey.at/en/blog/accelerating-edge-ai-inference  
[^38]: MLX: Apple silicon上的数值计算与机器学习框架. https://mlx-framework.org/