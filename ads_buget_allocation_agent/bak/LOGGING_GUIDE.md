# 📝 预算分配Agent日志记录指南

## 🎯 概述

现在你可以将`PrintingCallbackHandler`的所有输出保存到文件中，同时保持在终端的实时显示。**重要更新**：我们已经完美解决了Python代码执行结果的捕获问题，现在终端输出和文件记录完全一致！

## 🔧 多种日志模式

### 1. 简单文件记录 (`simple`)
- **特点**: 只将关键信息写入文件
- **适用**: 需要简洁日志记录的场景
- **输出**: 文件记录 + 可选终端显示

### 2. 双输出模式 (`dual`)
- **特点**: 完全保持原有的终端输出，同时写入文件
- **适用**: 既要实时查看又要保存日志
- **输出**: 终端显示 + 完整文件记录

### 3. 完整捕获模式 (`complete`) ⭐ **强烈推荐**
- **特点**: 完美捕获所有Python执行结果，包括数据框、统计信息、图表等
- **适用**: 需要完整记录数据分析过程的场景
- **输出**: 终端显示 + **完整Python执行结果** + 结构化文件记录
- **格式**: 使用图标标识（🔧工具调用 🤖Agent回复 📊Python执行结果）

### 4. 结构化日志 (`structured`)
- **特点**: 详细的步骤化日志，带时间戳和步骤编号
- **适用**: 需要详细分析执行过程的场景
- **输出**: 结构化文件 + 可选终端摘要

## 🚀 使用方法

### 方法1: 修改现有代码 (最简单)

在你的`buget_allocation_agent.py`中，现在已经更新为：

```python
from custom_callback_handler import create_callback_handler

# 创建自定义回调处理器 - 完美捕获Python执行结果
callback_handler = create_callback_handler(
    handler_type="complete",  # 强烈推荐：完整捕获所有输出
    log_file=None,  # 自动生成文件名
)

agent = Agent(
    model=get_llm(),
    system_prompt=PROMPT,
    tools=[file_read, python_repl],
    callback_handler=callback_handler
)
```

### 方法2: 使用专门的运行脚本

```bash
# 运行带日志记录的分析
python run_with_logging.py

# 或者直接运行主程序
python buget_allocation_agent.py
```

### 方法3: 自定义配置

```python
# 自定义日志文件名 - 完整模式
callback_handler = create_callback_handler(
    handler_type="complete",
    log_file="my_budget_analysis_2024.log"
)

# 只记录到文件，不在终端显示
callback_handler = create_callback_handler(
    handler_type="simple",
    also_print=False
)

# 测试简单场景
callback_handler = create_callback_handler(
    handler_type="complete",
    log_file="simple_test.log"
)
```

## 📁 日志文件格式

### 自动生成的文件名格式:
- `budget_analysis_complete_20250703_145634.txt` (complete模式) ⭐ **推荐**
- `budget_analysis_log_20240101_143022.txt` (dual模式)
- `budget_analysis_detailed_20240101_143022.txt` (structured模式)

### 日志内容示例 (complete模式):

```
=== 预算分配Agent完整执行日志 ===
开始时间: 2025-07-03 14:56:34
==================================================

[14:56:38] 🔧 工具 #1: file_read
----------------------------------------

[14:56:40] 🤖 Agent回复:
----------------------------------------
我会帮您分析广告数据并给出预算调整建议。首先，让我查看您提供的数据文件。
========================================

[14:56:40] 📊 Python执行结果:
----------------------------------------
Content of 2025-03-04_input.csv:
adset_id,campaign_id,daily_budget,purchase,ctr,roas...
adse_1835,camp_4441,51.1,3.0,0.0,41.8,48.5,1.3...
========================================

[14:56:43] 🔧 工具 #2: python_repl
----------------------------------------

[14:56:47] 📊 Python执行结果:
----------------------------------------
数据形状: (18, 22)

数据列名: ['adset_id', 'campaign_id', 'daily_budget', 'purchase'...]

数据前几行:
    adset_id campaign_id  ...  add_to_cart  cost_per_add_to_cart
0  adse_1835   camp_4441  ...          6.0                   8.5
1  adse_4014   camp_0057  ...         -1.0                  -1.0
...

按Campaign分组的数据:
   campaign_id  daily_budget  purchase  purchase_value       roas
0    camp_0057           0.0      -1.0            -1.0  -1.000000
1    camp_0296          24.5       2.0          1220.0  48.900000
...

预算调整建议:
| Campaign ID | 当前预算 | 当前ROAS | 调整后预算 | 调整金额 | 调整幅度 |
| ----------- | -------- | -------- | ---------- | -------- | -------- |
| camp_0296   | $24.5    | 48.9     | $35.87     | $11.37   | 46.39%   |
...
========================================

[14:58:25] 🤖 Agent回复:
----------------------------------------
# 广告预算调整建议

根据您提供的广告数据，我已完成对2025-03-04数据的分析...
========================================
```

## 🎯 实际使用场景

### 场景1: 日常分析 (推荐complete模式) ⭐
```python
# 完整捕获所有Python执行结果，包括数据框和统计信息
callback_handler = create_callback_handler("complete")
```

### 场景2: 批量处理 (推荐simple模式)
```python
# 减少终端输出，专注于文件记录
callback_handler = create_callback_handler("simple", also_print=False)
```

### 场景3: 调试分析 (推荐structured模式)
```python
# 详细的步骤记录，便于问题排查
callback_handler = create_callback_handler("structured")
```

### 场景4: 快速测试
```python
# 使用简单测试脚本验证功能
python simple_test.py
```

## 📊 日志文件的价值

### 1. 完整的分析过程追溯 ⭐ **新功能**
- 完整记录AI的思考过程
- **完整的Python代码执行结果**（数据框、统计信息、图表）
- 工具调用的详细信息
- 数据处理的每个步骤

### 2. 结果验证
- 对比不同参数下的分析结果
- 验证预算调整建议的合理性
- 追踪优化效果
- **查看完整的数据分析表格和统计信息**

### 3. 问题排查
- 当分析出现异常时，可以查看详细日志
- 了解在哪个步骤出现了问题
- 优化prompt和参数设置
- **检查Python代码执行的具体输出**

### 4. 报告生成
- 基于日志生成详细的分析报告
- 向客户展示分析的专业性和透明度
- 作为决策依据的支撑材料
- **包含完整的数据分析结果和可视化内容**

## 🆕 最新功能特性

### ✅ 完美解决的问题
1. **Python执行结果完整捕获** - 现在可以完整记录所有print输出、数据框显示、统计信息等
2. **终端和文件输出一致** - 解决了之前终端有内容但文件缺失的问题
3. **结构化日志格式** - 使用图标和清晰的分隔符，便于阅读和分析
4. **流式数据处理** - 正确处理Strands框架的流式回调机制

### 🎯 核心改进
- **CompleteDualCallbackHandler**: 新的回调处理器，完美捕获所有输出
- **智能数据解析**: 正确解析工具结果中的Python执行输出
- **清洁的日志格式**: 移除调试信息，保持日志文件整洁
- **自动文件管理**: 自动生成带时间戳的日志文件名

## 🔧 高级配置

### 测试和验证
```bash
# 运行简单测试验证功能
python simple_test.py

# 运行完整的预算分析
python buget_allocation_agent.py

# 检查生成的日志文件
ls -la *.log *.txt
```

### 自定义日志格式
```python
class MyCustomHandler:
    def __init__(self, log_file):
        self.log_file = log_file
    
    def __call__(self, **kwargs):
        # 自定义处理逻辑
        with open(self.log_file, 'a') as f:
            f.write(f"Custom log: {kwargs}\n")

# 使用自定义处理器
agent = Agent(
    model=get_llm(),
    system_prompt=PROMPT,
    tools=[file_read, python_repl],
    callback_handler=MyCustomHandler("custom.log")
)
```

### 日志轮转和管理
```python
import os
from datetime import datetime, timedelta

def cleanup_old_logs(log_dir=".", days_to_keep=7):
    """清理超过指定天数的日志文件"""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    for filename in os.listdir(log_dir):
        if filename.startswith("budget_analysis_"):
            file_path = os.path.join(log_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            
            if file_time < cutoff_date:
                os.remove(file_path)
                print(f"删除旧日志文件: {filename}")
```

## 🎉 总结

现在你可以：

1. ✅ **保持原有体验**: 终端输出完全不变
2. ✅ **完整Python结果捕获**: 所有数据框、统计信息、图表都被完整记录 ⭐ **新功能**
3. ✅ **自动保存日志**: 所有输出自动写入文件
4. ✅ **灵活配置**: 多种模式适应不同需求
5. ✅ **便于分析**: 结构化的日志便于后续分析
6. ✅ **问题排查**: 详细记录便于调试和优化
7. ✅ **专业格式**: 使用图标和清晰分隔符的专业日志格式

**强烈推荐使用complete模式**，它能完美捕获所有Python执行结果，让你的数据分析过程完全透明和可追溯！

## 🚀 快速开始

```bash
# 1. 运行预算分析（自动使用complete模式）
python buget_allocation_agent.py

# 2. 查看生成的日志文件
ls -la budget_analysis_complete_*.txt

# 3. 运行简单测试验证功能
python simple_test.py
```

现在你的预算分配Agent不仅能提供专业的分析建议，还能完整记录整个分析过程！🎉