from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
boto_session = Session()
region = boto_session.region_name
region

agentcore_runtime = Runtime()
agent_name="ads_go_pre_advertisement_agent"
agentcore_runtime.configure(
    entrypoint="ads_go_agent_as_tool_core_agent.py",
    execution_role="arn:aws:iam::517141035927:role/agentcore-strands_claude-role",
    auto_create_ecr=True,
    requirements_file="requirements_core_agent.txt",
    region=region,
    agent_name=agent_name
)
status_response = agentcore_runtime.status()
status = status_response.endpoint['status']
end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
while status not in end_status:
    time.sleep(10)
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']
    print(status)
status