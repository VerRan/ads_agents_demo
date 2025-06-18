from strands import Agent, tool
from strands_tools import file_write, http_request, agent_graph as strands_agent_graph
from strands.models import BedrockModel
from exa_py import Exa
from botocore.config import Config

def run_agent_graph(task):
    # Create an agent with agent_graph capability
    agent = Agent(tools=[strands_agent_graph])

    coordinator_sys_prompt = """
                            #产品分析项目总监
                            ## 角色定位
                            你是一名资深的产品分析项目总监，具备深厚的商业分析、市场研究和数据洞察能力。你负责统筹整个URL产品分析项目，确保分析的系统性、准确性和商业价值。

                            ## 核心使命
                            ### 使命一：制定详细分析计划并协调执行
                            - 接收URL输入并验证有效性
                            - 基于URL内容快速判断产品类型和分析重点
                            - 制定详细的分析执行计划和时间节点
                            - 按逻辑顺序调度各专业Agent执行任务
                            - 监控各Agent输出质量，必要时要求重新分析
                            - 确保分析过程的完整性和连贯性

                            ### 使命二：整合信息生成综合分析报告
                            - 收集所有子Agent的分析结果
                            - 进行跨维度的信息整合和逻辑梳理
                            - 识别关键洞察和战略机会点
                            - 生成结构化的综合分析报告
                            - 提供可操作的战略建议和执行优先级

                            ### 使命三：输出JSON化受众信息
                            - 基于受众分析结果提取关键信息
                            - 输出标准化的JSON格式受众数据
                            - 包含推荐市场国家、日预算、投放媒体、ROAS等关键指标
                            - 确保数据格式符合广告投放系统要求

                            ### 输出规则
                            - 使用中文回复
                            - 最终结果存储到文件里
        """

    product_analyst_sys_prompt= """
                                ##产品分析
                                - 产品定位和特点
                                - 产品线情况分析
                                - 价格策略研究
                                - 产品质量和用户评价
                                - 销售渠道分析
                                - 品牌故事和价值主张

                                ##质量自检清单
                                [ ] 产品特征描述是否准确全面？
                                [ ] 核心卖点是否提炼到位？
                                [ ] 信息是否为后续分析提供了足够支撑？
                                [ ] 是否避免了过度解读和无关信息？
                                                """

    competitor_analyst_sys_prompt="""
                    ##竞品分析
                    - 找出主要竞争对手
                    - 竞品定位和差异对比
                    - 竞品价格策略比较
                    - 竞品营销手段和渠道分析
                    - 竞品市场份额和增长趋势
                    - SWOT分析

                    ##质量自检清单
                    [ ] 是否严格按照体量匹配标准筛选竞品？
                    [ ] 竞品的体量数据是否经过验证？
                    [ ] 是否深入分析了竞品的广告投放策略？
                    [ ] 是否识别了明确的差异化机会点？"""

    market_analyst_sys_prompt="""
                    ##市场分析
                    - 全球市场规模和增长趋势
                    - 市场细分和目标市场分析
                    - 市场发展的推动和阻碍因素
                    - 行业趋势和创新动态
                    - 季节性变化和地域差异
                    - 市场机会和挑战
                    ##质量自检清单
                    [ ] 市场规模和趋势分析是否准确？
                    [ ] 竞争格局和机会点是否识别清晰？
                    [ ] 投放时机和地区建议是否具体可行？
                    [ ] 是否为投放策略提供了有价值的市场洞察？"""

    # Create a research team with a star topology
    result = agent.tool.agent_graph(
        action="create",
        graph_id="ads_pre_analysis",
        topology={
            "type": "star",
            "nodes": [
                {
                    "id": "coordinator",
                    "role": "team_lead",
                    "system_prompt": coordinator_sys_prompt
                },
                {
                    "id": "data_analyst",
                    "role": "analyst",
                    "system_prompt":product_analyst_sys_prompt
                },
                {
                    "id": "competitor_analyst",
                    "role": "analyst",
                    "system_prompt": competitor_analyst_sys_prompt
                },
                {
                    "id": "market_analyst",
                    "role": "analyst",
                    "system_prompt": market_analyst_sys_prompt
                }
            ],
            "edges": [
                {"from": "coordinator", "to": "data_analyst"},
                {"from": "coordinator", "to": "competitor_analyst"},
                {"from": "coordinator", "to": "market_analyst"},
                {"from": "data_analyst", "to": "coordinator"},
                {"from": "competitor_analyst", "to": "coordinator"},
                {"from": "market_analyst", "to": "coordinator"}
            ]
        }
    )

    # Send a task to the coordinator
    agent.tool.agent_graph(
        action="message",
        graph_id="ads_pre_analysis",
        message={
            "target": "coordinator",
            "content": task
        }
    )
##### 下面通过工具来实现 Multi-Level Hierarchy
def get_llm():
    # model_id="amazon.nova-lite-v1:0"
    # model_id="us.amazon.nova-premier-v1:0"
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


API_KEY = "00a01fd0-0483-4bba-91b6-1a719838238a"
@tool
def exa_search(search_text) -> str:
    exa = Exa(api_key = API_KEY)
    result = exa.search_and_contents(
        search_text,
        text = { "max_characters": 1000 }
    )
    # print(result)
    return result

#产品分析专家Agent - 产品特征挖掘师
@tool
def product_analyst(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: 要分析的产品名称

    Returns:
       根据系统提示词要求返回产品特征相关信息
    """

    RESEARCH_ASSISTANT_PROMPT = """
                            ##产品分析
                            - 产品定位和特点
                            - 产品线情况分析
                            - 价格策略研究
                            - 产品质量和用户评价
                            - 销售渠道分析
                            - 品牌故事和价值主张

                            ##质量自检清单
                            [ ] 产品特征描述是否准确全面？
                            [ ] 核心卖点是否提炼到位？
                            [ ] 信息是否为后续分析提供了足够支撑？
                            [ ] 是否避免了过度解读和无关信息？
                                            """

    try:
        # Strands agents makes it easy to create a specialized agent
        research_agent = Agent(
            model=get_llm(),
            system_prompt=RESEARCH_ASSISTANT_PROMPT,
            tools=[exa_search]
        )

        # Call the agent and return its response
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
    
@tool
def competitor_analyst(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: 要分析的产品名称

    Returns:
       根据系统提示词要求返回竞争对手相关信息
    """
    SYS_PROMPT="""
                ##竞品分析
                - 找出主要竞争对手
                - 竞品定位和差异对比
                - 竞品价格策略比较
                - 竞品营销手段和渠道分析
                - 竞品市场份额和增长趋势
                - SWOT分析

                ##质量自检清单
                [ ] 是否严格按照体量匹配标准筛选竞品？
                [ ] 竞品的体量数据是否经过验证？
                [ ] 是否深入分析了竞品的广告投放策略？
                [ ] 是否识别了明确的差异化机会点？"""
    try:
        product_agent = Agent(
            model=get_llm(),
            system_prompt=SYS_PROMPT,
            tools=[exa_search]
        )
        # Call the agent and return its response
        response = product_agent(query)

        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"
    
@tool
def market_analyst(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: 要分析的产品名称

    Returns:
       根据系统提示词要求返回相市场相关信息
    """
    SYS_PROMPT="""
                ##市场分析
                - 全球市场规模和增长趋势
                - 市场细分和目标市场分析
                - 市场发展的推动和阻碍因素
                - 行业趋势和创新动态
                - 季节性变化和地域差异
                - 市场机会和挑战
                ##质量自检清单
                [ ] 市场规模和趋势分析是否准确？
                [ ] 竞争格局和机会点是否识别清晰？
                [ ] 投放时机和地区建议是否具体可行？
                [ ] 是否为投放策略提供了有价值的市场洞察？"""
    try:
        travel_agent = Agent(
            model=get_llm(),
            system_prompt=SYS_PROMPT,
            tools=[exa_search]
        )
        # Call the agent and return its response
        response = travel_agent(query)

        return str(response)
    except Exception as e:
        return f"Error in trip planning: {str(e)}"

@tool
def audience_analyst(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: 要分析的产品名称

    Returns:
       根据系统提示词要求返回受众相关信息
    """
    SYS_PROMPT="""
                ##受众分析
                - 目标受众的人口特征
                - 消费者行为和购买决策过程
                - 受众喜好和需求分析
                - 社交媒体参与度及影响因素
                - 用户忠诚度和复购率分析
                - 受众细分和个性化营销机会
                ##质量自检清单
                [ ] 用户画像是否精准具体？
                [ ] 核心需求和痛点是否挖掘到位？
                [ ] 行为特征和媒体偏好是否清晰？
                [ ] 是否识别了有价值的潜在受众 """

    try:
        product_agent = Agent(
            model=get_llm(),
            system_prompt=SYS_PROMPT,
            tools=[exa_search]
        )
        # Call the agent and return its response
        response = product_agent(query)

        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"

# 将Agent作为工具，实现多Agent的编排，该场景，编排agent会根据任务的理解，决定使用哪个工具Agent，
# 被使用的agent会根据自身的需要调用自己的工具完成子任务，最终由编排Agent完成最终的处理。
def coordinator_agent(task):
    # Create the coordinator agent with all tools
     coordinator_sys_prompt = """
                        #产品分析项目总监
                        ## 角色定位
                        你是一名资深的产品分析项目总监，具备深厚的商业分析、市场研究和数据洞察能力。你负责统筹整个URL产品分析项目，确保分析的系统性、准确性和商业价值。

                        ## 核心使命
                        ### 使命一：制定详细分析计划并协调执行
                        - 接收URL输入并验证有效性
                        - 基于URL内容快速判断产品类型和分析重点
                        - 制定详细的分析执行计划和时间节点
                        - 按逻辑顺序调度各专业Agent执行任务
                        - 监控各Agent输出质量，必要时要求重新分析
                        - 确保分析过程的完整性和连贯性

                        ### 使命二：整合信息生成综合分析报告
                        - 收集所有子Agent的分析结果
                        - 进行跨维度的信息整合和逻辑梳理
                        - 识别关键洞察和战略机会点
                        - 生成结构化的综合分析报告
                        - 提供可操作的战略建议和执行优先级

                        ### 使命三：输出JSON化受众信息
                        - 基于受众分析结果提取关键信息
                        - 输出标准化的JSON格式受众数据
                        - 包含推荐市场国家、日预算、投放媒体、ROAS等关键指标
                        - 确保数据格式符合广告投放系统要求

                        ### 输出规则
                        - 使用中文回复
                        - 最终结果存储到文件里
    """
     coordinator_agent = Agent(
        system_prompt=coordinator_sys_prompt,
        tools=[
            product_analyst,
            audience_analyst,
            market_analyst,
            competitor_analyst
        ],
        callback_handler=None
    )
     # Print only the last response
     response = coordinator_agent(task)
     return response

def main():
    task="分析一下https://www.kreadoai.com/"
    # run_agent_graph(task)
    coordinator_agent(task)

if __name__ == "__main__":
    main()