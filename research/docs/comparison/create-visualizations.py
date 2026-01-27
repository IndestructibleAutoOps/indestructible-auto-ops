#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def setup_matplotlib_for_plotting():
    """
    Setup matplotlib and seaborn for plotting with proper configuration.
    Call this function before creating any plots to ensure proper rendering.
    """
    # Ensure warnings are printed
    warnings.filterwarnings('default')  # Show all warnings

    # Configure matplotlib for non-interactive mode
    plt.switch_backend("Agg")

    # Set chart style
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")

    # Configure platform-appropriate fonts for cross-platform compatibility
    # Must be set after style.use, otherwise will be overridden by style configuration
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "PingFang SC", "Arial Unicode MS", "Hiragino Sans GB"]
    plt.rcParams["axes.unicode_minus"] = False

def create_throughput_comparison():
    """创建吞吐量对比图表"""
    setup_matplotlib_for_plotting()
    
    # 基于收集到的数据创建7B模型吞吐量对比
    frameworks = ['TensorRT-LLM', 'vLLM', 'DeepSpeed-MII', 'llama.cpp', 'LMDeploy']
    h100_throughput = [5500, 5000, 3500, 1500, 4200]  # tokens/second on H100
    a100_throughput = [3750, 3200, 2400, 1200, 2800]  # tokens/second on A100
    
    x = np.arange(len(frameworks))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars1 = ax.bar(x - width/2, h100_throughput, width, label='H100 GPU', alpha=0.8)
    bars2 = ax.bar(x + width/2, a100_throughput, width, label='A100 GPU', alpha=0.8)
    
    ax.set_xlabel('推理框架')
    ax.set_ylabel('吞吐量 (tokens/second)')
    ax.set_title('7B模型在不同推理框架上的吞吐量对比')
    ax.set_xticks(x)
    ax.set_xticklabels(frameworks, rotation=45, ha='right')
    ax.legend()
    
    # 添加数值标签
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(rect.get_x() + rect.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    autolabel(bars1)
    autolabel(bars2)
    
    plt.tight_layout()
    plt.savefig('/workspace/docs/comparison/throughput_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_latency_comparison():
    """创建延迟对比图表"""
    setup_matplotlib_for_plotting()
    
    # 首令牌延迟对比 (TTFT)
    frameworks = ['TensorRT-LLM', 'vLLM', 'DeepSpeed-MII', 'llama.cpp', 'LMDeploy']
    ttft_latency = [0.35, 0.38, 0.42, 0.45, 0.40]  # seconds on H100
    
    # 令牌间延迟对比 (ITL)
    itl_latency = [0.20, 0.22, 0.25, 0.35, 0.24]  # milliseconds on H100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # TTFT对比
    bars1 = ax1.bar(frameworks, ttft_latency, color='skyblue', alpha=0.8)
    ax1.set_title('首令牌延迟 (TTFT) 对比')
    ax1.set_ylabel('延迟 (秒)')
    ax1.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{height:.2f}s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # ITL对比
    bars2 = ax2.bar(frameworks, itl_latency, color='lightcoral', alpha=0.8)
    ax2.set_title('令牌间延迟 (ITL) 对比')
    ax2.set_ylabel('延迟 (毫秒)')
    ax2.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f}ms',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('/workspace/docs/comparison/latency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_ease_of_use_radar():
    """创建易用性雷达图"""
    setup_matplotlib_for_plotting()
    
    frameworks = ['TensorRT-LLM', 'vLLM', 'DeepSpeed-MII', 'llama.cpp', 'LMDeploy']
    
    # 易用性评分 (1-5分，5分最高)
    categories = ['安装难度', 'API友好度', '文档完善度', '社区支持', '部署复杂度']
    
    # 各框架在不同维度的评分
    scores = {
        'TensorRT-LLM': [2, 3, 3, 4, 2],  # 性能最佳但安装复杂
        'vLLM': [4, 5, 4, 5, 4],          # 平衡性好
        'DeepSpeed-MII': [3, 3, 3, 3, 3], # 中等水平
        'llama.cpp': [5, 2, 2, 4, 5],     # 最易用但功能有限
        'LMDeploy': [4, 4, 4, 3, 4]       # 新兴框架，平衡性好
    }
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))  # 闭合
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, framework in enumerate(frameworks):
        values = scores[framework]
        values += [values[0]]  # 闭合数据
        
        ax.plot(angles, values, 'o-', linewidth=2, label=framework, color=colors[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'])
    ax.grid(True)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title('推理框架易用性对比雷达图', pad=20)
    
    plt.tight_layout()
    plt.savefig('/workspace/docs/comparison/ease_of_use_radar.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_scalability_comparison():
    """创建扩展性对比图表"""
    setup_matplotlib_for_plotting()
    
    # 分布式推理支持能力对比
    frameworks = ['TensorRT-LLM', 'vLLM', 'DeepSpeed-MII', 'llama.cpp', 'LMDeploy']
    
    # 支持的并行策略 (分数越高越好)
    tensor_parallel = [5, 4, 4, 1, 4]  # 张量并行支持
    pipeline_parallel = [4, 3, 4, 1, 3]  # 流水线并行支持
    data_parallel = [4, 5, 5, 2, 4]  # 数据并行支持
    multi_gpu = [5, 4, 4, 2, 4]  # 多GPU支持
    
    x = np.arange(len(frameworks))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars1 = ax.bar(x - 1.5*width, tensor_parallel, width, label='张量并行', alpha=0.8)
    bars2 = ax.bar(x - 0.5*width, pipeline_parallel, width, label='流水线并行', alpha=0.8)
    bars3 = ax.bar(x + 0.5*width, data_parallel, width, label='数据并行', alpha=0.8)
    bars4 = ax.bar(x + 1.5*width, multi_gpu, width, label='多GPU支持', alpha=0.8)
    
    ax.set_xlabel('推理框架')
    ax.set_ylabel('支持程度 (1-5分)')
    ax.set_title('推理框架分布式推理扩展性对比')
    ax.set_xticks(x)
    ax.set_xticklabels(frameworks, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 5.5)
    
    plt.tight_layout()
    plt.savefig('/workspace/docs/comparison/scalability_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_cost_effectiveness_matrix():
    """创建成本效益矩阵图"""
    setup_matplotlib_for_plotting()
    
    frameworks = ['TensorRT-LLM', 'vLLM', 'DeepSpeed-MII', 'llama.cpp', 'LMDeploy']
    
    # 性能和开发成本的综合评分
    performance_score = [5, 4, 3, 2, 4]  # 性能评分 (1-5)
    development_cost = [5, 2, 3, 1, 2]   # 开发成本 (1-5, 数值越高成本越高)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    sizes = [100, 80, 60, 40, 70]  # 气泡大小表示综合评分
    
    scatter = ax.scatter(development_cost, performance_score, s=sizes, 
                        c=colors, alpha=0.6)
    
    for i, framework in enumerate(frameworks):
        ax.annotate(framework, (development_cost[i], performance_score[i]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=10, ha='left')
    
    ax.set_xlabel('开发成本 (数值越高成本越高)')
    ax.set_ylabel('性能评分 (数值越高性能越好)')
    ax.set_title('推理框架成本效益矩阵')
    ax.grid(True, alpha=0.3)
    
    # 添加象限说明
    ax.text(0.5, 4.5, '高性价比区域\n(低开发成本 + 高性能)', 
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5),
           ha='center')
    ax.text(4.5, 4.5, '高性能但高成本\n(仅在性能要求极高时考虑)', 
           bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5),
           ha='center')
    
    plt.tight_layout()
    plt.savefig('/workspace/docs/comparison/cost_effectiveness_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """主函数，创建所有图表"""
    print("正在创建可视化图表...")
    
    create_throughput_comparison()
    print("✓ 吞吐量对比图已创建")
    
    create_latency_comparison()
    print("✓ 延迟对比图已创建")
    
    create_ease_of_use_radar()
    print("✓ 易用性雷达图已创建")
    
    create_scalability_comparison()
    print("✓ 扩展性对比图已创建")
    
    create_cost_effectiveness_matrix()
    print("✓ 成本效益矩阵图已创建")
    
    print("\n所有图表已生成完成，保存在 /workspace/docs/comparison/ 目录下")

if __name__ == "__main__":
    main()
