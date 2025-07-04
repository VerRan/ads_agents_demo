from strands import Agent, tool
from strands_tools import file_write, file_read,http_request,python_repl
from strands.models import BedrockModel
from exa_py import Exa
from botocore.config import Config
import os
from strands.handlers.callback_handler import PrintingCallbackHandler
from custom_callback_handler import create_callback_handler
import logging

os.environ['DEV'] = 'true'

class CustomCallbackHandler:
    def __call__(self, **kwargs):
        # 只打印你关心的信息
        if "tool_result" in kwargs:
            print(f"🔧 工具执行结果: {kwargs['tool_result']}")

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
你是一个专业的广告预算调整专家Agent，负责基于历史数据和优化原则，为广告Campaign提供预算调整建议。

## 核心目标
- 1. 请结合用户提供的日预算及目标ROAS给出每个campaign的预算调整建议。
## 输出要求
- 你必须给出用户所提供数据中最新日期下每一条campaign的预算优化结果；
- 当广告数据中缺失每个campaign的当日预算时，你可以将campaign自身的当日spend视为此campaign的当日预算。
- 你必须专注于预算优化场景，禁止回复其他无关信息；
- 你必须在输出前检查结果，确保严格遵守优化规则；

## 输出格式要求
你必须使用markdown格式输出最新时间下每个campaign的预算分配结果:
- campaign_id: 广告系列ID
- current_budget: 当前预算
- current_roas：当前ROAS
- new_budget: 调整后预算
- adjustment_amount: 调整金额
- adjustment_percentage: 调整幅度
- action_type: 动作类型(增加/减少/维持/暂停)
- reason: 调整原因和数据支撑
- risk_level: 风险等级(低/中/高)
'''

# 创建自定义回调处理器 - 同时输出到终端和文件
callback_handler = create_callback_handler(
    handler_type="complete",  # 推荐: "complete" - 使用stdout重定向完全捕获输出
    log_file=None,  # 自动生成文件名，或指定如 "budget_analysis.log"
)

agent = Agent(
    model=get_llm(),
    system_prompt=PROMPT,
    tools=[file_read, python_repl],
    callback_handler=callback_handler
    )

filename="2025-03-04_input.csv"

# 测试代码 - 只在直接运行此文件时执行
if __name__ == "__main__":
    # ret = agent(f"当前目录{filename}的文件,帮我统计一下有多少行数据？")
    # print("问题1:",ret)
    daily_budget=500
    ROAS=20
    task=f"""你必须在用户的日预算{daily_budget}
    及目标KPI{ROAS}的基础上，对用户提供的广告数据{filename}进行深度分析，后给出预算调整建议。"""

    ret = agent(task)
    print(ret)
