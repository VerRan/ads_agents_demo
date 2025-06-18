from strands import tool
from exa_py import Exa
from strands import Agent, tool
from strands_tools import file_read, file_write, editor
import asyncio
import os

@tool
def exa_search(search_text) -> str:
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise ValueError("EXA_API_KEY environment variable not set")
    
    exa = Exa(api_key=api_key)
    result = exa.search_and_contents(
        search_text,
        text={"max_characters": 1000}
    )
    print(result)

def main():
    url = "https://www.amazon.com/YAVCOOL-Shoulder-Handbags-Vacation-Holiday/dp/B0D1QJ8J7Q/ref=s9_acsd_al_ot_c2_x_1_t?_encoding=UTF8&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=NMNZA9RZS9CHR3ERBY4V&pf_rd_p=99b2cded-4dea-478b-8b60-b6c1bdb7df27&pf_rd_t=&pf_rd_i=206404546011&th=1"
    PROMPT= f"""为 {url} 在Facebook ads、Google ads等广告平台上创建具有竞争力的广告；因此需要对此网站链接进行深度的投前分析，并产出报告供我全面了解产品自身、竞品、市场情况，辅助我制定最佳的投放策略；因此需要你需要对此网站链接进行产品分析、竞品分析、市场分析、受众分析部分的详细分析，其余不要；你应该保证报告中尽可能存在量化数据指标（需有客观事实的数据来源佐证）,且竞品的品牌尽可能的与此品牌产品的风格特征、细分赛道、体量规模、网站访问量、品牌知名度上均有一定程度的接近，否则将造成竞品过大或过小，对比无任何意义；并按照以下结构分析输出：
    1.产品分析
    - 产品定位和特点
    - 产品线情况分析
    - 价格策略研究
    - 产品质量和用户评价
    - 销售渠道分析
    - 品牌故事和价值主张
    2.竞品分析
    - 找出主要竞争对手
    - 竞品定位和差异对比
    - 竞品价格策略比较
    - 竞品营销手段和渠道分析
    - 竞品市场份额和增长趋势
    - SWOT分析
    3.市场分析
    - 全球市场规模和增长趋势
    - 市场细分和目标市场分析
    - 市场发展的推动和阻碍因素
    - 行业趋势和创新动态
    - 季节性变化和地域差异
    - 市场机会和挑战
    4.受众分析
    - 目标受众的人口特征
    - 消费者行为和购买决策过程
    - 受众喜好和需求分析
    - 社交媒体参与度及影响因素
    - 用户忠诚度和复购率分析
    - 受众细分和个性化营销机会
    """

    ads_agent = Agent(
                system_prompt=(
                "你是一名资深的广告分析师"
                ),
                tools=[exa_search]
            )

    ads_agent(PROMPT)


if __name__ == "__main__":
    main()
