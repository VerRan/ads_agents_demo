from strands import Agent, tool
from strands_tools import file_write, file_read,http_request,python_repl
from strands.models import BedrockModel
from exa_py import Exa
from botocore.config import Config
import os
from strands.handlers.callback_handler import PrintingCallbackHandler
import logging

os.environ['DEV'] = 'true'

# def task_to_code(task):
# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.INFO)
# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_llm():
    # model_id="amazon.nova-lite-v1:0"
    # model_id="us.amazon.nova-pro-v1:0"
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    ## increate the timeout for bedrock
    config = Config(read_timeout=1000)

    # Create a BedrockModel
    bedrock_model = BedrockModel(
        model_id=model_id,
        region_name='us-east-1',
        temperature=0.3,
        config=config
    )
    return bedrock_model

# 2. 理解数据结构
# 3. 提供数据的分布
PROMPT='''
作为一位专业的数据分析专家和Python编程专家，请帮我编写代码完成以下数据分析任务。

## 分析目标
{用户在此描述他们想要实现的具体分析目标}

## 数据描述
- 数据格式：{CSV/Excel/JSON/SQL数据库等}
- 数据大致内容：{简要描述数据包含哪些字段和记录}
- 关键字段：{列出需要特别关注的字段名称及其含义}
- 数据规模：{数据量大小，如行数、列数}

## 所需分析类型
{选择一个或多个：
- 探索性数据分析
- 描述性统计
- 可视化分析
- 相关性分析
- 时间序列分析
- 分组统计与比较
- 预测建模
- 其他特定分析}

## 特殊要求
{任何特殊要求，如特定的库偏好、性能考量、输出格式等}

请生成可执行的Python代码，包括:
1. 必要的库导入
2. 数据加载和预处理步骤
3. 逐步的分析过程，每步附有注释说明
4. 适当的可视化（如需要）
5. 分析结果的解释与总结

请确保代码遵循PEP 8标准，并优化性能。如果有任何假设，请明确指出。
'''

# SYS_PROMPT="""
# you are a professional data analyst , please anlysis the data  step by step
# 1. you 
# 2. Output a script that does what we just spoke about!
#    Use your python tools to confirm that the script works before outputting it
# """
agent = Agent(
    model=get_llm(),
    system_prompt=PROMPT,
    tools=[file_read, python_repl],
    callback_handler=PrintingCallbackHandler()
    )

filename="google.campaign_daily_geo_stats.csv"

# 测试代码 - 只在直接运行此文件时执行
if __name__ == "__main__":
    # ret = agent(f"当前目录{filename}的文件,帮我统计一下有多少行数据？")
    # print("问题1:",ret)
    ret = agent(f"当前目录{filename}的文件,帮我统计文件中有多少个缺失值？")
    print("问题2:",ret)
