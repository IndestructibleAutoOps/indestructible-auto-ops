# 边缘端和移动端大语言模型推理方案研究报告

## 摘要

随着大型语言模型（LLM）规模的持续增长，其在边缘设备和移动终端上的部署面临着严峻的资源约束挑战。模型参数量从数十亿到数千亿的膨胀，使得传统依赖云端服务器的计算模式面临延迟、带宽和隐私保护等多重问题。本报告系统性地研究了当前边缘端和移动端的主流推理方案，涵盖量化压缩技术（GPTQ、AWQ、GGUF、bitsandbytes）、移动端推理框架（MLC-LLM、llama.cpp、MediaPipe）、嵌入式平台部署方案（Jetson、树莓派）以及浏览器端推理技术（WebLLM、Transformers.js）。研究从模型支持范围、推理性能、内存占用、功耗表现和适用场景等多个维度进行了深入分析，旨在为开发者在不同硬件环境下选择最优部署策略提供决策依据。

## 一、引言

### 1.1 研究背景与动机

大型语言模型的快速发展正在重塑人工智能应用的格局，从自然语言处理到代码生成，从多模态理解到智能体协作，LLM展现出了前所未有的通用性和实用性。然而，这些模型庞大的参数量和计算需求长期以来限制了其在资源受限环境中的部署。以典型的70B参数模型为例，其在FP16精度下的模型大小约为140GB，需要高端GPU才能进行有效推理。这种计算资源的巨大需求与边缘设备和移动终端有限算力之间的矛盾，催生了针对边缘端和移动端优化的推理技术研究。

边缘端部署LLM的需求源于多个实际应用场景。首先是隐私保护考量，许多应用场景（如医疗问诊、法律咨询、个人助手）要求用户数据不能离开本地设备，这对依赖云端API的传统模式构成了根本性限制。其次是延迟敏感性，实时交互应用（如语音助手、智能客服）要求毫秒级响应，而网络传输带来的延迟往往无法满足这一需求。再者是网络可用性，在工业控制、野外勘探、航空航天等场景中，网络连接可能不可靠或完全缺失，此时本地推理成为唯一可行的解决方案。最后是成本效益考量，大规模云端部署的成本随用户增长呈线性甚至超线性增长，而边缘部署虽然需要前期硬件投入，但长期运营成本可能显著降低。

### 1.2 技术挑战与应对策略

边缘端和移动端部署LLM面临的核心挑战可以归纳为三个层面：计算能力限制、内存带宽约束和功耗预算紧张。现代移动处理器的浮点计算能力虽然不断提升，但与数据中心GPU相比仍有数量级的差距。以典型的移动SoC为例，其AI算力通常在10-50 TOPS范围内，而NVIDIA数据中心GPU可达数千TOPS。内存带宽是另一个关键瓶颈，LLM推理需要频繁加载大量权重参数，而移动设备的LPDDR内存带宽远低于独立显卡的GDDR/HBM显存。功耗限制在移动场景中尤为突出，持续高负载运行可能导致设备过热降频，并显著缩短电池续航。

针对这些挑战，业界发展出了多种应对策略。模型压缩技术通过降低参数精度来减少模型体积和计算量，是最基础也是最有效的优化手段。专用推理引擎针对目标硬件进行深度优化，充分利用SIMD指令、神经网络加速器和混合精度计算。系统级协同调度则通过CPU、GPU、NPU的协同工作，实现性能与功耗的最佳平衡。这些技术并非相互独立，而是往往需要组合使用才能达到理想的部署效果。

### 1.3 研究范围与方法

本报告的研究范围涵盖当前边缘端和移动端LLM推理领域的主流技术方案。量化技术方面，重点分析GPTQ、AWQ、GGUF和bitsandbytes四种代表性方法的原理、性能和适用场景。移动端框架方面，深入研究MLC-LLM、llama.cpp和MediaPipe三个主要框架的技术架构和实现特点。嵌入式平台方面，评估NVIDIA Jetson系列和树莓派等代表性硬件平台的部署能力。浏览器端推理方面，分析WebLLM和Transformers.js两个主要技术方案的实现机制和性能边界。

研究方法上，本报告采用文献调研、技术分析和实证数据综合评估相结合的方式。首先通过系统性的文献检索收集各方案的技术文档、学术论文和开源代码仓库信息。然后深入分析各技术的核心原理和实现机制，理解其设计理念和优化思路。最后整合来自官方基准测试、第三方评测和社区实践的性能数据，形成全面的对比分析。所有性能数据均注明来源和测试条件，以便读者评估其在特定环境下的适用性。

## 二、量化技术深度解析

### 2.1 量化技术概述与分类

模型量化是减少LLM部署资源需求最直接有效的技术手段。其核心思想是将模型参数从高精度浮点数（如FP32、FP16）转换为低精度表示（如INT8、INT4甚至更低），从而在保持模型效果的前提下显著降低存储空间和计算成本。量化技术可以根据应用阶段分为训练后量化（Post-Training Quantization，PTQ）和量化感知训练（Quantization-Aware Training，QAT）两大类。PTQ在模型训练完成后直接进行量化，实现简单但可能导致较大的精度损失。QAT在训练过程中模拟量化效果，使模型适应低精度表示，通常能够获得更好的精度保持，但需要额外的训练成本。

从量化维度来看，权重量化（Weight-Only Quantization）仅对模型参数进行压缩，计算时仍使用高精度累加，是当前主流的量化方式。动态量化（Dynamic Quantization）在推理时根据激活值的实际分布动态确定量化参数，精度较高但增加了运行时开销。静态量化（Static Quantization）预先确定量化参数，需要使用校准数据拟合激活分布，执行效率高但需要代表性数据集。混合量化（Mixed-Precision Quantization）对不同层或通道采用不同的量化精度，在模型大小和精度之间取得更精细的平衡。

### 2.2 GPTQ量化技术

GPTQ（Gradient Post-Training Quantization）是一种面向LLM的经典训练后量化方法，由Frantar等人于2022年提出并在后续研究中持续优化。该方法基于最优脑量化（Optimal Brain Quantization）框架，通过逐层优化来最小化量化误差。其核心创新在于使用基于层的近似二阶信息来指导量化决策，避免了全局优化的计算复杂度。GPTQ支持将模型量化至3-4位精度，在显著降低模型大小的同时保持与原始模型相当的输出质量。

从技术原理来看，GPTQ采用分层优化的策略。对于每一层，它首先计算该层参数的精确 Hessian 矩阵，然后通过迭代求解找到使得量化误差最小的量化表示。关键优化在于对求解过程的近似，避免了原始最优脑切割算法中的大量矩阵求逆操作，使得大规模模型的量化成为可能。GPTQ还引入了分层再排序和盲量化等技术，进一步提升了量化精度。该方法的一个重要特性是支持组量化（Group-wise Quantization），即对参数矩阵的不同子组采用独立的缩放因子，这在低比特量化时对精度保持至关重要。

在实际性能表现方面，GPTQ在4位量化下通常能够将困惑度（Perplexity）增加控制在1-2%的范围内，对于大多数应用场景是可接受的。在vLLM框架的基准测试中，GPTQ在Qwen2.5-32B模型上实现了276.60 token/s的输出吞吐量，虽然低于FP16基线的461.04 token/s，但模型大小从64GB压缩至约16GB。GPTQ的主要优势在于量化速度快、使用简单，有成熟的工具链支持（AutoGPTQ、GPTQ-for-LLaMa等）。其局限性在于推理速度优化高度依赖于特定GPU架构的核函数实现，在部分硬件平台上可能无法充分发挥硬件特性。

### 2.3 AWQ量化技术

AWQ（Activation-aware Weight Quantization）是一种考虑激活值分布的权重量化方法，由MIT Han Lab于2023年提出并在MLSys 2024获得最佳论文奖。AWQ的核心洞见在于：LLM中并非所有权重对模型输出同等重要，仅保护约1%的显著权重（Salient Weights）即可大幅减少量化误差。关键的技术创新在于识别显著权重的方法——AWQ主张根据激活分布而非权重本身来确定重要性，这是因为对输出影响大的权重通常会与较大的激活值相关联。

AWQ的技术实现包含三个关键步骤。首先是显著性分析，通过在少量校准数据上运行模型，收集各层的激活值分布，识别出对输出贡献最大的权重通道。其次是等效变换，根据分析结果计算各通道的缩放因子，通过数学等效变换将显著权重放大，从而在相同的量化分辨率下获得更高的有效精度。最后是量化执行，使用调整后的参数进行标准分组量化。AWQ无需反向传播或重建过程，因此可以泛化到不同的领域和模态，不会过拟合特定的校准数据集。

在性能对比方面，AWQ在多种语言建模和领域特定基准（编程、数学）上优于GPTQ和其他现有方法。配套的TinyChat推理框架在桌面和移动GPU上比Huggingface FP16实现实现了3倍以上的加速。值得注意的是，AWQ首次实现了在移动GPU上部署70B Llama-2模型的突破，展示了其出色的硬件效率。然而，vLLM的基准测试显示AWQ在吞吐量指标上表现不如GPTQ（67.73 vs 276.60 token/s），这可能与当前实现中的核函数优化程度有关。AWQ特别适合需要在边缘设备上保持高质量输出的应用场景，其激活感知的权重保护机制在处理复杂推理任务时优势明显。

### 2.4 GGUF格式与量化方案

GGUF（GPT-Generated Unified Format）是由llama.cpp团队开发的模型文件格式，专门为高效的LLM存储和推理而设计。作为GGML格式的继任者，GGUF解决了前代格式的多项局限，提供了更好的扩展性、兼容性和性能表现。该格式已成为本地LLM社区的事实标准，被llama.cpp、Ollama、Transformers等多款主流工具广泛支持。

GGUF格式的设计理念围绕三个核心目标。首先是可移植性，格式将模型权重、配置信息和分词器数据打包为单一文件，简化了模型的分发和部署流程。其次是可扩展性，格式采用基于键值对的元数据设计，可以灵活添加新信息而不破坏与旧版本的兼容性。最后是性能优化，格式设计充分考虑了推理引擎的访问模式，支持内存映射（Memory Mapping）以加速模型加载，支持高效的量化表示以减少内存占用。

GGUF支持丰富的量化级别，从2位到8位共包含多种量化方案。Q2_K将模型压缩至原大小的约29%，适合极端资源受限场景。Q3_K系列（Q3_K_M、Q3_K_L）在压缩率和质量之间取得平衡，是许多用户的默认选择。Q4_K系列（Q4_0、Q4_1、Q4_K_M）是最常用的级别，模型大小约为原FP16的36-40%，质量损失极小。Q5_K系列（Q5_0、Q5_1、Q5_K_M）进一步提升了输出质量，模型大小约为原大小的50-55%。Q6_K和Q8_0分别提供接近FP16和INT8的质量，模型大小约为原大小的70%和100%。这种精细的量化级别划分使用户能够根据具体硬件约束灵活选择。

在性能表现方面，GGUF格式配合llama.cpp在CPU推理场景中展现出卓越的效率。其纯C实现具有极低的内存开销和启动延迟，特别适合资源受限的嵌入式环境。vLLM基准测试显示GGUF（Q5_K_M）在代码生成任务（HumanEval）上取得了54.3%的Pass@1得分，超越了其他量化方法。然而，在GPU推理场景下，由于vLLM对GGUF的支持尚未完全优化，其吞吐量（81.30 token/s）和首Token时间（TTFT 1177.9 ms）表现不如GPTQ和Marlin。GGUF的另一个优势是支持存储提示模板（Prompt Template），这对于跨应用部署标准化模型非常有用。

### 2.5 bitsandbytes量化方案

bitsandbytes是由Tim Dettmers开发的量化库，已成为Hugging Face生态系统中最广泛使用的量化工具之一。该库提供了8位（LLM.int8()）和4位（NF4/FP4）两种量化模式，并且在量化过程中对关键计算保留高精度，从而在大幅压缩模型的同时最小化精度损失。bitsandbytes的一个重要特性是支持量化模型的微调（QLoRA），使得在消费级GPU上微调大模型成为可能。

8位量化采用LLM.int8()方法，其核心创新在于对"离群值"（Outlier）通道保留FP16精度。研究者发现，LLM的激活值中约0.1-1%的通道具有异常大的幅度，这些通道在INT8表示下会严重损失精度。LLM.int8()通过在矩阵乘法过程中动态检测和分离这些离群通道，分别使用FP16和INT8进行计算，最后合并结果。该方法将模型内存占用减少约50%，使得原本需要多卡部署的模型可以在单卡上运行。8位量化对参数值在约5范围内的激活效果最佳，离群值阈值默认设为6，可以通过配置调整以在精度和速度之间取得平衡。

4位量化（NF4）结合了双重量化和分块量化技术。NF4（Normal Float 4）是一种针对正态分布优化的4位数据类型，其量化间隔按照正态分布的累积分布函数设计，能够更好地保留参数的统计特性。嵌套量化（Nested Quantization）进一步节省内存，通过对量化后的缩放因子再次进行量化，在不增加计算开销的情况下额外节省约0.4 bits/参数。实测表明，Llama-13B模型可在16GB T4 GPU上使用4位嵌套量化进行微调。bitsandbytes还支持灵活的计算数据类型选择，可配置为float32（默认）或bf16进行计算累加。

在硬件支持方面，bitsandbytes覆盖了主流AI加速器。对于8位优化器和NF4量化，支持Pascal及以上架构的NVIDIA GPU。对于LLM.int8()方法，支持Turing及以上架构。Intel XPU、Habana Gaudi和CPU后端同样可用。vLLM基准测试显示，bitsandbytes在困惑度指标上表现最佳（6.6652 vs FP16基线6.5612），质量损失最小，吞吐量达到168.37 token/s。bitsandbytes的主要优势在于与Hugging Face Transformers库的深度集成，使用门槛低，且量化模型可直接用于微调。

### 2.6 量化技术对比分析

综合上述分析，各量化方法在精度、速度、易用性和适用场景上存在显著差异。在精度保持方面，bitsandbytes的4位NF4量化表现最佳，其次是AWQ和GPTQ，GGUF在低比特量化时精度略低但代码生成任务除外。在推理速度方面，Marlin（GPU优化核函数）最快，其次是GPTQ，bitsandbytes和AWQ速度相当，GGUF在CPU推理场景更快但在GPU场景需要优化。在易用性方面，bitsandbytes与Hugging Face生态系统无缝集成最为便捷，GGUF配合llama.cpp在本地部署场景使用简单，GPTQ和AWQ需要更多配置但支持更广泛的框架。

选择量化方法时需要考虑以下因素：目标模型的大小和架构、可用硬件类型和内存约束、对输出质量的敏感度、是否需要进一步微调。对于追求最佳质量且需要微调的场景，bitsandbytes是首选。对于边缘设备部署且关注功耗，AWQ的激活感知保护机制可能带来更好体验。对于追求极致压缩率和CPU推理效率，GGUF配合llama.cpp是成熟方案。对于生产环境部署且关注吞吐量，GPTQ配合vLLM可能更为适合。值得注意的是，量化方法的效果与具体模型和任务相关，建议在实际部署前进行充分的基准测试。

## 三、移动端推理框架技术分析

### 3.1 移动端推理的技术挑战

移动端部署LLM面临着与桌面和服务器环境截然不同的技术挑战。首先是异构计算资源的协调管理，现代移动SoC通常包含CPU、GPU和专用NPU等多种计算单元，如何根据工作负载特征动态分配计算任务以实现最佳性能是一个复杂问题。其次是内存带宽限制，移动设备普遍采用LPDDR内存，其带宽远低于桌面级DDR或数据中心GPU的HBM显存，而LLM推理需要频繁加载大量权重参数。再者是功耗和热管理约束，移动设备电池容量有限，且缺乏主动散热能力，长时间高负载运行可能导致系统降频或触发热保护。

针对这些挑战，移动端推理框架采用了多种优化策略。在计算优化方面，充分利用SIMD指令（如ARM NEON、ARM I8MM）加速矩阵运算，使用混合精度计算减少数据搬运开销。在内存优化方面，采用分块加载和权重缓存策略减少内存访问延迟，实现KV Cache压缩以降低长上下文场景的内存占用。在功耗优化方面，优先使用专用NPU进行推理以获得最佳能效比，实现动态频率调节以根据负载调整计算资源。在框架架构方面，支持异步执行以避免阻塞UI线程，支持模型预热和智能缓存以减少首次推理延迟。

### 3.2 MLC-LLM技术架构

MLC-LLM（Machine Learning Compilation for LLM）是由MLC AI团队开发的高性能LLM部署引擎，其设计理念是通过机器学习编译器技术实现跨平台的通用LLM部署。该项目建立在Apache TVM/Relax编译器栈之上，能够将LLM模型编译为针对目标平台优化的可执行代码，从而在多种硬件环境下获得接近手写优化的性能。MLC-LLM的使命是让每个人都能在任何平台上原生开发、优化和部署AI模型。

MLC-LLM的技术架构包含三个核心组件。首先是模型导入层，支持从PyTorch、Transformers等主流框架导入模型，支持多种模型架构和量化格式。其次是编译优化层，利用TVM的自动调度（AutoTVM）和张量IR（TensorIR）进行算子级和图级优化，包括算子融合、内存布局转换、混合精度优化等。最后是运行时引擎层，提供统一的推理API，支持OpenAI兼容的REST接口，支持Python、JavaScript、iOS、Android等多种调用方式。MLCEngine作为统一推理引擎，屏蔽了底层硬件差异，为上层应用提供一致的编程接口。

在跨平台支持方面，MLC-LLM覆盖了广泛的目标环境。桌面平台支持Windows、Linux和macOS，利用CUDA、Metal和OpenCL进行GPU加速。移动平台支持Android和iOS，分别通过OpenCL/Vulkan和Metal利用GPU加速。浏览器平台支持WebLLM项目，使用WebGPU进行硬件加速。嵌入式平台支持NVIDIA Jetson、Apple Vision Pro等设备。MLC-LLM的编译优化能够针对各平台的硬件特性进行深度调优，例如在Apple Silicon上充分利用统一内存架构和Metal性能着色器，在Android设备上适配不同厂商的GPU架构。

在性能表现方面，MLC-LLM在移动GPU推理上展现出色能力。基于大规模商用移动设备的基准测试显示，搭载Adreno 750 GPU的Snapdragon 8 Gen3设备在使用MLC-LLM时能够实现高效的LLM推理。值得注意的是，尽管理论算力更强的Mali-G720 GPU（3418 GFLOPS）在SPEC上优于Adreno 750（2232 GFLOPS），但实际推理性能反而是Adreno显著领先，这说明GPU架构特性和驱动优化对实际性能的影响远超理论算力指标。MLC-LLM的GPU利用率在5%-20%范围内，显示仍有优化空间。

### 3.3 llama.cpp移动版实现

llama.cpp是由Georgi Gerganov开发的轻量级LLM推理引擎，其设计哲学强调简单性、便携性和性能。项目采用纯C/C++实现，不依赖任何外部深度学习框架，具有极低的依赖要求和优秀的跨平台移植性。llama.cpp最初针对Apple Silicon进行优化，但已扩展支持广泛的CPU架构，包括x86-64、ARM64、RISC-V等。在移动端，llama.cpp通过Android NDK和iOS SDK支持Android和iOS平台，成为本地LLM部署的事实标准工具。

llama.cpp的核心技术特点包括以下几个方面。GGUF格式支持是项目的核心创新，llama.cpp是最早支持GGUF格式的推理引擎，并推动其成为社区标准。K-Quant系列量化方法是llama.cpp的标志性特性，提供从Q2到Q8的多种量化级别，用户可以根据质量和性能需求灵活选择。内核优化涵盖ARM NEON、AVX、AVX2、AVX-512等多种SIMD指令集，并通过手写汇编进一步提升关键运算的性能。推测解码（Speculative Decoding）支持通过小模型辅助大模型推理来加速生成过程。

在移动端性能方面，llama.cpp针对ARM架构进行了深度优化。ARM I8MM指令集优化（smla、sdot指令）可实现约4倍的性能提升。新的ARM CPU优化使得低上下文提示处理速度提升2-3倍，在7K上下文长度下有用户报告约50%的改进。llama.cpp在移动端主要依赖CPU进行推理，适合没有强大GPU加速的设备或追求极致功耗效率的场景。基于骁龙888和8GB内存的Android设备测试表明，llama.cpp能够成功运行7B参数模型，尽管速度有限。项目还集成了新的OpenCL GPU后端，为Qualcomm Adreno GPU提供GPU加速支持。

llama.cpp的生态系统非常丰富。llamafile项目将llama.cpp封装为单可执行文件，支持跨平台直接运行。Ollama进一步简化了llama.cpp的使用体验，提供模型管理和API服务能力。众多第三方应用（如PocketPal AI、MLC Chat）基于llama.cpp构建了面向终端用户的移动应用。llama.cpp的局限在于其纯CPU推理模式在需要GPU加速的场景下性能不如MLC-LLM等框架，且缺乏对NPU的支持。

### 3.4 MediaPipe LLM推理方案

MediaPipe是Google开发的开源机器学习框架，专注于快速构建跨平台ML解决方案。MediaPipe LLM Inference API是Google在设备端LLM推理领域的重要布局，提供跨Web、Android和iOS的统一API。该方案基于TensorFlow Lite运行时，针对移动设备进行了深度优化，支持int8和int4权重量化，能够在资源受限的环境中运行中小型语言模型。

MediaPipe LLM Inference的功能特性包括多个方面。权重共享机制是MediaPipe的重要优化，通过在连续推理请求间共享权重和KV Cache来降低内存占用。模型转换工具支持将Hugging Face Transformers格式的模型转换为MediaPipe Task格式，便于开发者使用自定义模型。多模态支持使其不仅限于文本生成，还能处理视觉语言模型等任务。LoRA适配器支持允许在不修改基础模型的情况下进行领域适应。

在支持的模型方面，MediaPipe LLM Inference覆盖了主流的开源模型。Gemma系列（1B、2B、7B）是Google的开源模型，与MediaPipe深度集成。Phi-2是Microsoft的小型高质量模型，适合资源受限场景。Falcon和Stable LM等其他主流开源模型也获得支持。值得注意的是，由于iOS的内存限制，目前MediaPipe在iOS上仅支持Gemma 2B（int4量化）模型运行。在Android平台上，MediaPipe更适合实验研究和原型开发，生产应用推荐使用Gemini API或Android AICore，后者支持硬件神经加速器、LoRA适配器和安全过滤器。

MediaPipe的主要优势在于与Google生态系统的紧密集成，对于已经使用MediaPipe进行其他ML任务的开发者来说，增量成本很低。预构建的Task API简化了集成流程，开发者无需深入了解底层实现细节。然而，MediaPipe LLM推理在生产级应用中的定位相对有限，Google更推荐其云端Gemini API或本地AICore方案。对于需要完全离线部署且对性能有较高要求的场景，MLC-LLM或llama.cpp可能是更好的选择。

### 3.5 移动端框架性能对比

综合各框架的技术特点和实测性能，可以从多个维度进行对比分析。在推理后端方面，llama.cpp主要针对CPU优化，在缺乏GPU加速的设备上表现稳定。MLC-LLM利用GPU加速，在配备强大移动GPU的设备上性能更优。MediaPipe支持CPU和GPU混合模式，针对特定Google硬件有深度优化。在支持的量化方面，llama.cpp支持最丰富的GGUF量化级别，MLC-LLM支持多种格式的量化模型，MediaPipe主要支持int8/int4。

在移动设备实测性能方面，基于大规模商用设备的基准测试提供了有价值的参考。在CPU推理模式下（llama.cpp，Llama-2-7B 4-bit量化），Dimensity 9300设备取得了最高性能，prefill约10.63 token/s，decode约8.22 token/s。Snapdragon 8 Gen3设备性能约为Dimensity 9300的80%。相比上一代骁龙870设备，新一代SoC的prefill性能提升约3倍，decode性能提升近5倍。在GPU推理模式下（MLC-LLM），Adreno系列GPU显著优于Mali系列，尽管后者的理论算力可能更强，这反映了GPU架构和驱动优化的重要性。

在NPU推理方面，Qualcomm AI Hub在Snapdragon 8 Gen3上实现了690 token/s的prefill速度，比CPU/GPU方案快约50倍。然而，NPU的decode速度提升有限，仅略优于CPU/GPU，这限制了在生成阶段的加速效果。MLC团队和Qualcomm合作开发的mllm和PowerInfer-2等项目正在探索更好的NPU利用方案。值得注意的是，移动GPU的利用率普遍较低（5%-20%算术单元），这表明当前的推理引擎尚未充分利用移动GPU的并行计算能力，存在进一步优化的空间。

## 四、嵌入式平台部署方案

### 4.1 NVIDIA Jetson平台概述

NVIDIA Jetson系列是嵌入式AI计算领域最具影响力的平台之一，为边缘设备上的深度学习推理提供了从入门级到高性能的完整产品线。Jetson平台的优势在于其与NVIDIA数据中心产品共享的CUDA生态系统，开发者可以轻松将在云端训练好的模型迁移到边缘设备上部署。当前主流的Jetson产品包括Jetson Orin NX、Jetson Orin Nano、Jetson AGX Orin以及最新的Jetson Thor，覆盖了从7W功耗到275W功耗、从小模型到超大规模模型的广泛部署需求。

Jetson平台的软件栈高度成熟，为LLM部署提供了完整的解决方案。TensorRT是NVIDIA的深度学习推理优化器，通过算子融合、内存优化、精度校准等技术在目标GPU上实现最佳性能。TensorRT-LLM在TensorRT基础上增加了LLM特定的优化，包括Flash Attention、KV Cache优化、连续批处理等，能够显著提升大模型的推理效率。vLLM框架也在Jetson平台上获得支持，提供了更高的推理吞吐量。此外，Jetson JetPack SDK包含了CUDA、cuDNN、TensorRT等全部必要组件，简化了开发环境的配置流程。

在硬件规格方面，不同Jetson型号的性能差异显著。入门级的Jetson Orin Nano Super提供34 TOPS的INT8算力和接近1.5 TFLOPS的FP16算力，适合运行3-7B参数的量化模型。中端的Jetson Orin NX提供100 TOPS INT8算力，能够运行14-32B参数的量化模型。高端的Jetson AGX Orin提供275 TOPS INT8算力和275 TFLOPS FP16算力，支持70B参数的量化模型。最新的Jetson Thor更是提供了 petaFLOPS 级别的FP8算力，为下一代边缘AI应用提供了强大的硬件基础。

### 4.2 Jetson平台LLM推理性能

NVIDIA官方发布的基准测试数据为Jetson平台的LLM推理能力提供了权威参考。在Jetson AGX Thor（JetPack 7.0，TensorRT 10.13）上的测试结果显示，Llama 3.1 8B模型在单并发下可达41.3 token/s，在8并发下可达150.8 token/s。更大的Llama 3.3 70B模型在单并发下为4.7 token/s，8并发下为12.6 token/s。国产模型Qwen 3 30B-A3B表现出色，单并发达61 token/s，8并发达226.4 token/s，甚至超越了更小的8B模型。DeepSeek R1系列同样展现了优秀的性能，7B模型在8并发下达304.8 token/s。

在视觉语言模型方面，Jetson AGX Thor同样表现强劲。Qwen2.5-VL 3B单并发达71.7 token/s，8并发达356.86 token/s。Qwen2.5-VL 7B单并发45 token/s，8并发252 token/s。LLama 3.2 11B Vision单并发26.31 token/s，8并发69.63 token/s。这些数据表明，Jetson平台不仅支持纯文本LLM，还能有效运行多模态视觉语言模型，为边缘端的多模态AI应用提供了可能。

Jetson AGX Orin在MLPerf基准测试中的表现同样值得关注。GPT-J 6B模型在单流测试中延迟为10204.46ms，离线场景下吞吐量达0.15 samples/s。Stable Diffusion XL的延迟为12941.92ms，离线吞吐量0.08 samples/s。对于BERT NLP任务，AGX Orin在单流测试中延迟仅5.71ms，吞吐量达553.69 samples/s，Orin NX为194.5 samples/s。这些数据表明Jetson平台在传统NLP任务上具有极低的延迟，适合实时交互应用。

### 4.3 树莓派部署方案

树莓派（Raspberry Pi）是全球最流行的单板计算机之一，以其低功耗、低成本和丰富的社区生态著称。随着Raspberry Pi 5的推出和AI HAT+扩展卡的发布，树莓派正在成为边缘AI部署的热门选择。Raspberry Pi 5搭载了Broadcom BCM2712处理器，采用四核Cortex-A76架构，运行频率2.4GHz，性能相比前代提升2-3倍。VideoCore VII GPU支持Vulkan 1.2，为AI推理提供了基础图形加速能力。

树莓派运行LLM面临的主要限制是缺乏强大的AI加速器。CPU推理在4-7B参数模型上可以实现，但速度有限。GPU加速受限于VideoCore的算力和内存带宽，实际加速效果不如独立GPU明显。针对这一限制，Raspberry Pi推出了AI HAT+扩展卡，提供8 TOPS或26 TOPS的INT8算力，专门用于加速神经网络推理。AI HAT+支持Hailo-8L或Hailo-8 AI加速器芯片，能够显著提升模型推理效率，使得在树莓派上运行更大规模的语言模型成为可能。

在软件生态方面，树莓派支持多种LLM推理框架。llama.cpp是最常用的选择，经过ARM NEON优化后可以在树莓派上实现可用的推理速度。Ollama简化了模型管理和部署流程，通过简单的命令行即可运行各种量化模型。MLC-LLM也支持树莓派平台，能够利用GPU加速提升性能。Hailo提供的TAPPAS工具链支持将模型编译为Hailo格式以充分利用AI HAT+的加速能力。Raspberry Pi官方学习路径提供了详细的部署指南，指导用户在树莓派5上运行高效的LLM模型。

在性能表现方面，基于8GB内存树莓派5的实测数据显示，1-3B参数模型在4位量化下可以实现可用的推理速度，7B模型在2位或3位超低比特量化下也可运行但速度较慢。AI HAT+扩展卡能够将推理速度提升3-5倍，使得7B模型在4位量化下也能获得可接受的用户体验。功耗方面，树莓派5运行LLM推理的功耗约为4-8W（不含AI HAT+），配合AI HAT+后约为7-15W，非常适合电池供电的边缘应用场景。

### 4.4 其他嵌入式平台对比

除Jetson和树莓派外，市场上还存在多种边缘AI平台可供选择。Google Coral TPU是Google推出的边缘AI加速器，提供4 TOPS的INT8算力，功耗仅0.5W。Google Coral Dev Board基于NXP i.MX 8M SoC配合Coral TPU，运行Linux系统，支持TensorFlow Lite模型。在与树莓派5的对比测试中，Jetson Orin NX在帧率上接近树莓派5加Coral TPU的两倍，显示出更强的AI性能。

Rockchip RK3588是瑞芯微推出的高性能AIoT处理器，集成了6 TOPS算力的NPU。该芯片已被多家厂商采用，推出了如YY3588等边缘计算板卡。在与Jetson Orin Nano和树莓派5的对比测试中，YY3588在DeepSeek LLM推理上的单推理功耗为4.3W，token生成速度介于树莓派5和Jetson Orin Nano之间，显示出良好的能效比。

NVIDIA Jetson与树莓派的对比是开发者经常关心的话题。基准测试显示，Jetson Nano在ResNet-50推理上可达约36 FPS，而树莓派3仅约1.4 FPS，性能差距约为25-30倍。在LLM推理场景下，Jetson Orin系列能够运行70B参数的量化模型，而树莓派通常限于7B及以下参数模型。然而，树莓派的价格优势明显（入门级型号仅约35美元），适合预算有限或需要大规模部署的场景。Jetson平台则面向对性能有更高要求的专业应用，其更高的价格定位（数百至数千美元）反映了其更强的计算能力和更完善的软件支持。

## 五、浏览器端推理技术

### 5.1 浏览器端推理的技术基础

浏览器端LLM推理代表了去中心化AI部署的前沿方向，其核心目标是在用户设备上的Web浏览器中直接运行语言模型，无需任何服务器参与。这一技术路线的优势是显而易见的：用户隐私得到保护（数据不离开设备），服务提供商的服务器成本趋近于零，系统可用性不受网络状况影响，AI能力的普及不再受服务器容量限制。然而，浏览器环境对计算资源的限制使得这一目标充满挑战，开发者需要在有限的硬件能力下实现尽可能高效的模型推理。

浏览器端推理的技术基础包括三个关键组件。WebGPU是新一代Web图形和计算API，提供接近原生的GPU访问能力，是浏览器端AI推理的核心加速器。与前代WebGL相比，WebGPU支持计算着色器、更灵活的内存管理和更低的API开销，能够更高效地利用现代GPU的并行计算能力。WebAssembly（WASM）提供了接近原生性能的代码执行环境，使得C/C++实现的推理引擎可以在浏览器中高效运行。Web Workers支持在后台线程中执行计算密集型任务，避免阻塞主线程导致界面卡顿。

在模型格式方面，浏览器端推理通常需要使用针对Web环境优化的模型格式。ONNX（Open Neural Network Exchange）格式通过ONNX Runtime Web在浏览器中运行，是Transformers.js的核心格式。MLC格式是MLC-LLM团队开发的自定义格式，专为WebLLM优化，支持多种量化级别。这些格式通常需要经过专门的转换和优化过程，以减少模型下载量并加速浏览器中的执行。

### 5.2 WebLLM技术实现

WebLLM是由MLC AI团队开发的浏览器端LLM推理引擎，是该领域的代表性技术方案。WebLLM将MLC-LLM的编译优化能力带入浏览器环境，通过WebGPU实现硬件加速，使用户能够在Chrome、Edge等现代浏览器中直接运行大型语言模型。项目设计目标是让Web应用开发者能够便捷地将AI能力集成到应用中，同时保持接近原生应用的性能水平。

WebLLM的技术架构建立在TVM/Relax编译器栈之上，继承了MLC-LLM的编译优化能力。模型首先被编译为针对WebGPU优化的WGSL（WebGPU Shading Language）着色器代码，然后通过WebGPU API在浏览器中执行。这一编译过程可以在模型构建时离线完成，也支持在浏览器中在线完成。WebLLM支持多种主流开源模型，包括Llama、Phi、Gemma、RedPajama、Mistral、Qwen等，覆盖了从1B到7B的参数范围。

WebLLM的核心特性包括多个方面。首先，WebLLM提供完整的OpenAI API兼容性，支持JSON模式、函数调用、流式输出等高级功能，使得现有应用可以轻松迁移至WebLLM。其次，流式输出支持使得生成过程可以实时显示，提升用户体验。Web Worker支持允许将模型推理放在后台线程执行，避免阻塞UI线程。Chrome扩展支持使得开发者可以创建基于WebLLM的浏览器扩展。模型热切换支持允许在不刷新页面的情况下切换不同模型。

在性能表现方面，WebLLM的具体指标因设备和浏览器而异。在配备高性能GPU的桌面设备上，3B参数模型可以流畅运行，7B模型在4位量化下也可达到可用的推理速度。在移动设备上，受限于移动GPU性能和内存带宽，通常只能运行1-3B参数模型。WebLLM项目还开发了TinyChat引擎优化，在移动设备上实现了显著的性能提升。值得注意的是，WebGPU API在部分浏览器中仍处于实验阶段，可能需要启用特定标志才能使用。

### 5.3 Transformers.js技术分析

Transformers.js是Hugging Face推出的浏览器端机器学习库，旨在将Transformers的强大能力带入Web环境。与WebLLM不同，Transformers.js不仅支持文本生成，还支持文本分类、命名实体识别、问答、摘要、翻译、语音识别、图像分类、目标检测等广泛的NLP、CV和语音任务。这使得Transformers.js成为构建端到端Web AI应用的通用解决方案。

Transformers.js基于ONNX Runtime Web构建，将ONNX格式的模型在浏览器中执行。ONNX（Open Neural Network Exchange）是一个开放的模型格式标准，支持从PyTorch、TensorFlow等框架导出的模型转换。ONNX Runtime Web支持WASM后端（CPU执行）和WebGPU后端（GPU加速），用户可以根据设备能力选择合适的后端。对于资源受限环境，推荐使用量化版本的模型以降低带宽需求和优化执行性能。

Transformers.js支持的模型架构超过170种，包括BERT、GPT-2、T5、Whisper、CLIP、LLaMA、Mistral、Gemma、ViT、SAM等主流模型。任务支持涵盖自然语言处理（文本分类、情感分析、命名实体识别、问答、摘要、翻译、文本生成、零样本分类、特征提取）、计算机视觉（图像分类、目标检测、图像分割、深度估计、背景移除、图像特征提取）和音频处理（语音识别、音频分类、文本转语音）以及多模态任务（embeddings、零样本分类、文档问答、图像描述）。

在性能表现方面，Transformers.js提供多种量化选项：fp32（WebGPU默认）、fp16、q8（WASM默认）和q4。量化版本显著减少模型下载量和内存占用，适合带宽受限或内存有限的环境。Transformers.js还支持Node.js环境下的服务端推理，支持Electron桌面应用和浏览器扩展等多种运行环境。对于LLM推理任务，Transformers.js支持在WebGPU后端下运行LLaMA、Mistral等主流语言模型，但性能和模型规模支持可能不如专门针对LLM优化的WebLLM。

### 5.4 浏览器端推理的挑战与前景

浏览器端LLM推理虽然前景广阔，但当前仍面临多重挑战。内存限制是首要问题，浏览器对单个页面的内存使用有严格限制，通常在数百MB到数GB范围内，这直接限制了可运行的模型规模。WebGPU支持和性能在不同浏览器和设备上差异较大，Safari浏览器对WebGPU的支持滞后于Chrome和Edge，进一步限制了用户覆盖范围。模型下载量也是一个显著问题，即使使用量化模型，7B参数4位量化的模型也需要约4-5GB下载，对于移动用户来说成本过高。

从实际应用角度，浏览器端推理当前更适合以下场景：需要完全离线运行的应用、对延迟要求不高的交互场景、以隐私为首要考量的应用、模型规模在1-3B范围内的轻量级应用。典型的应用案例包括：浏览器中的智能助手插件、离线文档摘要工具、客户端文本处理工具、基于浏览器的代码辅助工具等。这些应用对模型规模的限制有清晰认知，能够在浏览器能力范围内提供有价值的功能。

展望未来，浏览器端LLM推理技术仍有巨大的发展空间。WebGPU标准的持续完善和浏览器支持的普及将逐步解决性能一致性问题。模型压缩技术的进步（如更激进的量化、知识蒸馏）将使得更大模型能够在浏览器中运行。WebGPU的下一代特性（如Subgroups、Wider行存储）将提供更多优化空间。硬件方面，独立GPU在轻薄本中的普及将提升主流设备的AI能力。随着这些因素的共同作用，浏览器端LLM推理有望成为AI应用分发的的重要渠道。

## 六、方案选型指南与最佳实践

### 6.1 场景化选型建议

针对不同的应用场景，各推理方案的优势差异明显。对于追求最高性能的生产环境部署，Jetson AGX Orin/Thor配合TensorRT-LLM是当前的最佳选择，能够在边缘设备上实现接近云端的推理性能。对于需要广泛硬件兼容性的本地部署，llama.cpp凭借其纯C实现和丰富的量化支持，是覆盖面最广的通用方案。对于需要跨移动端和桌面端的统一部署，MLC-LLM的编译优化和跨平台支持提供了最一致的体验。对于预算有限的个人用户和爱好者，树莓派配合llama.cpp或Ollama是性价比最高的入门选择。对于浏览器端应用，WebLLM和Transformers.js各有优势，前者专精LLM推理，后者提供更广泛的ML任务支持。

从模型规模角度，部署方案的选择也高度依赖于目标模型大小。70B及以上参数的超大模型通常只能在Jetson AGX Orin/Thor等高端嵌入式平台或配备大显存的桌面GPU上运行，量化后可部署在Jetson Orin NX等中端平台。30-70B参数的大模型可以在Jetson Orin NX/Nano上以量化形式运行，或在配备24GB以上显存的桌面GPU上运行。7-30B参数的中等模型是边缘部署的主力范围，可在Jetson Orin Nano、树莓派+AI HAT+、高端移动设备上运行。7B及以下参数的小型模型可以在大多数移动设备和树莓派上流畅运行，是当前浏览器端推理的主要对象。

从精度与效率权衡角度，量化方法的选择需要综合考虑模型质量要求和硬件约束。8位量化（Q8_0或INT8）质量损失最小（通常小于1%困惑度增加），适合对输出质量敏感的应用，但内存压缩有限。4位量化（Q4_K_M或AWQ/GPTQ 4-bit）是最常用的选择，模型大小约为FP16的36-40%，质量损失通常在1-3%范围内，适合大多数应用场景。2-3位超低比特量化可将模型压缩至原大小的20-30%，但质量损失显著增加，仅适合对质量要求不高的特定场景或资源极度受限的设备。

### 6.2 硬件配置建议

针对不同部署场景，硬件配置建议如下。对于高端边缘服务器场景，Jetson AGX Thor或配备RTX 4090的工控机是首选，前者提供完整的边缘AI解决方案，后者提供更强的通用计算能力。内存建议32GB以上，存储建议使用NVMe SSD以加速模型加载。对于中端嵌入式场景，Jetson Orin NX或AGX Orin是主流选择，配合TensorRT优化可获得最佳性价比。内存建议16GB以上，存储建议使用高速eMMC或NVMe SSD。对于入门级边缘场景，树莓派5配合AI HAT+ 26TOPS版本提供了极具性价比的选择，8GB内存足够运行7B 4位量化模型。对于移动设备场景，应优先选择配备强大GPU或NPU的旗舰芯片（如Snapdragon 8 Gen系列、苹果A系列芯片），内存建议12GB以上以支持更大的模型。

功耗是边缘部署的重要考量因素。Jetson AGX Orin的典型功耗为15-60W（取决于工作模式），适合有稳定电源供应的场景。Jetson Orin Nano典型功耗为7-15W，可使用电池供电。树莓派5典型功耗为4-8W（不含AI HAT+），非常适合电池供电的便携应用。移动设备的功耗完全依赖电池，推理任务会显著增加功耗 drain，建议设计合理的任务调度和休眠策略。

### 6.3 性能优化最佳实践

模型层面的优化是提升推理性能的基础。选择适合目标任务的最小模型可以显著减少计算量，例如对于简单的分类任务使用1-3B模型而非7B模型。应用量化是必须的步骤，建议从4位量化开始，根据质量评估结果决定是否需要提升到更高精度。模型蒸馏（Distillation）可以将大模型的能力迁移到小模型，是获得高质量轻量级模型的有效方法。提示优化（Prompt Engineering）虽然不直接提升推理速度，但可以减少生成token数量，间接改善用户体验。

运行时优化方面，批处理（Batching）可以显著提升吞吐量，适合非实时应用场景。KV Cache优化（分页注意力、压缩缓存）可以减少长上下文场景的内存占用和计算量。连续批处理（Continuous Batching）可以在不增加延迟的情况下提升服务器端吞吐量。预热推理（Warm-up Inference）可以消除首次推理的冷启动延迟，提升用户体验。

系统级优化方面，确保使用最新的驱动程序和框架版本可以避免已知的性能问题。针对特定硬件调整线程数、内存分配策略等参数可以获得额外收益。监控工具（如NVIDIA Nsight Systems、Arm Streamline）可以帮助识别性能瓶颈。针对功耗敏感场景，使用NPU推理而非GPU/CPU可以获得更好的能效比。

### 6.4 常见问题与解决方案

模型加载缓慢是最常见的问题之一。解决方案包括：使用更快的存储介质（如NVMe SSD而非eMMC或SD卡），使用内存映射（Memory Mapping）减少加载开销，预加载常用模型到内存或使用模型缓存机制，选择更小的量化模型。推理速度不达预期时的排查步骤包括：确认量化配置正确（使用正确的量化格式和参数），检查是否有足够的内存（避免频繁的Swap/分页），验证是否充分利用了GPU/NPU加速（检查硬件利用率），考虑使用更小参数量的模型或更激进的量化级别。

内存不足是另一个常见问题。解决方案包括：使用更低位数的量化（如从Q5_K_M降至Q4_K_M），减少上下文长度（长上下文会显著增加KV Cache内存占用），启用权重共享或分页缓存机制，使用内存泄漏检测工具确保没有内存泄漏。对于持续运行的服务，定期的内存回收和模型重载可能是必要的维护操作。

## 七、技术趋势与未来展望

### 7.1 硬件发展趋势

边缘AI硬件正在经历快速演进。NVIDIA的下一代Jetson Thor将提供petaFLOPS级别的FP8算力，为边缘AI开辟新的可能性。高通和联发科的下一代移动芯片将集成更强大的NPU，AI算力有望突破100 TOPS。Apple Silicon的持续演进使得在Mac上运行LLM的效率不断提升。专用AI加速器（如Google TPU、Intel Movidius、Hailo）的边缘化版本将为特定应用场景提供更高的能效比。内存技术的发展（如LPDDR6、HBM3e）将提升带宽，缓解当前的内存瓶颈。

### 7.2 软件技术演进

模型压缩技术方面，更激进的量化方法（2-bit、1-bit）正在研究中，有望进一步压缩模型大小。专家混合模型（MoE）架构允许在推理时只激活部分参数，显著降低计算需求。动态计算图优化可以根据输入特性自适应调整计算路径。硬件感知的神经网络架构搜索（HW-NAS）可以为特定硬件平台生成最优化的模型结构。

推理引擎方面，投机解码（Speculative Decoding）通过小模型辅助大模型加速生成过程。持续批处理和动态分块技术提升服务器端吞吐量。异构计算调度器能够更智能地分配CPU、GPU、NPU的计算任务。分布式推理技术使得多设备协作运行大模型成为可能。

### 7.3 应用场景展望

边缘端LLM的应用场景正在快速拓展。个人AI助手将在手机、电脑、可穿戴设备上提供完全离线或以隐私为首要考量的智能服务。工业AI应用将在制造、能源、物流等领域实现实时的智能决策和优化。车载AI系统将在自动驾驶、智能座舱等场景提供本地化的语音交互和环境理解能力。医疗健康领域的本地诊断辅助将保护患者隐私的同时提供高质量的医疗建议。教育领域的个性化学习助手将根据学生的学习进度和特点提供定制化的辅导内容。

## 八、结论

本报告系统性地研究了边缘端和移动端LLM推理的主流技术方案，涵盖量化技术、移动端框架、嵌入式平台和浏览器端推理四大领域。研究表明，当前边缘端推理技术已经取得了显著进步，在特定条件下能够实现接近云端部署的用户体验。

量化技术是边缘部署的基础，bitsandbytes以最小的质量损失和便捷的使用体验成为微调场景的首选，AWQ通过激活感知保护机制在边缘设备上展现了出色的质量保持，GGUF配合llama.cpp在CPU场景提供了优秀的效率和丰富的量化选项，GPTQ在GPU推理吞吐量上表现突出。开发者应根据硬件平台、质量要求和易用性需求选择合适的量化方法。

移动端框架方面，MLC-LLM凭借编译优化和跨平台支持提供了最一致的部署体验，llama.cpp以极简的依赖和广泛的兼容性成为本地部署的事实标准，MediaPipe为Google生态系统提供了便捷的设备端AI方案。性能测试显示，移动GPU的利用率仍有提升空间，NPU在Prefill阶段展现了巨大潜力。

嵌入式平台方面，NVIDIA Jetson系列提供了从入门到高端的完整产品线，TensorRT-LLM优化能够充分发挥GPU性能。树莓派配合AI HAT+为预算有限的用户提供了可行的入门方案。浏览器端推理虽然受限于内存和计算资源，但在特定场景下提供了独特的价值。

展望未来，边缘端LLM推理将在硬件能力提升、软件优化和应用场景拓展的共同推动下持续发展。开发者应密切关注技术演进，根据具体应用需求灵活选择和组合各种技术方案，以在边缘设备上实现最佳的AI部署效果。

---

## 参考文献

[1] [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323) - High Reliability - 学术论文，提出GPTQ量化方法

[2] [The Complete Guide to LLM Quantization with vLLM](https://docs.jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) - High Reliability - vLLM官方博客，包含详细基准测试数据

[3] [AWQ: Activation-aware Weight Quantization for LLM](https://arxiv.org/abs/2306.00978) - High Reliability - MLSys 2024最佳论文，MIT Han Lab官方论文

[4] [GGUF versus GGML](https://www.ibm.com/think/topics/gguf-versus-ggml) - High Reliability - IBM技术文档，提供GGUF格式详细分析

[5] [bitsandbytes Quantization](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes) - High Reliability - Hugging Face官方文档

[6] [MLC LLM Universal Deployment Engine](https://llm.mlc.ai/) - High Reliability - MLC AI官方项目主页

[7] [Large Language Model Performance Benchmarking on COTS Mobile Devices](https://arxiv.org/html/2410.03613v1) - High Reliability - 学术论文，移动端LLM基准测试研究

[8] [llama.cpp Performance on Mobile Devices](https://github.com/ggml-org/llama.cpp) - High Reliability - llama.cpp官方GitHub仓库

[9] [Large Language Models On-Device with MediaPipe](https://developers.googleblog.com/large-language-models-on-device-with-mediapipe-and-tensorflow-lite/) - High Reliability - Google Developers官方博客

[10] [Jetson Benchmarks](https://developer.nvidia.com/embedded/jetson-benchmarks) - High Reliability - NVIDIA官方基准测试数据

[11] [Raspberry Pi AI HAT+ Introduction](https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5/) - High Reliability - Raspberry Pi官方新闻

[12] [Benchmarking Edge AI Platforms: Performance Analysis of NVIDIA Jetson and Raspberry Pi 5 with Coral TPU](https://www.researchgate.net/publication/391165194_Benchmarking_Edge_AI_Platforms_Performance_Analysis_of_NVIDIA_Jetson_and_Raspberry_Pi_5_with_Coral_TPU) - High Reliability - 学术论文，边缘AI平台性能分析

[13] [WebLLM: High-Performance In-Browser LLM Inference Engine](https://webllm.mlc.ai/) - High Reliability - WebLLM官方项目主页

[14] [Transformers.js Documentation](https://huggingface.co/docs/transformers.js) - High Reliability - Hugging Face官方文档