from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
boto_session = Session()
region = boto_session.region_name
region

agentcore_runtime = Runtime()

agent_name="ads_go_pre_advertisement_agent"
response = agentcore_runtime.configure(
    entrypoint="ads_go_agent_as_tool_core_agent.py",
    execution_role="arn:aws:iam::517141035927:role/agentcore-strands_claude-role",
    auto_create_ecr=True,
    requirements_file="requirements_core_agent.txt",
    region=region,
    agent_name=agent_name
)
launch_result = agentcore_runtime.launch()
launch_result