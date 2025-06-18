from fastmcp import FastMCP

import os
import sys
from typing import Optional
from pydantic import BaseModel
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrockConverse
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.controller.service import Controller

mcp = FastMCP("Browser Use 🚀")
cdp_url = "http://localhost:9222"
max_steps = "10"

def get_llm():
    config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', config=config)

    return ChatBedrockConverse(
        model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        temperature=0.0,
        max_tokens=None,
        client=bedrock_client,
    )


@mcp.tool
async def execute_task(task):
    try:
        # Initialize browser session
        browser_session = BrowserSession(cdp_url=cdp_url)

        # browser_profile = BrowserProfile(
        #     executable_path=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        # )
        # browser_session = BrowserSession(browser_profile=browser_profile)
        
        # Initialize LLM
        llm = get_llm()
        
        # Create agent
        agent = Agent(
            task=task,
            llm=llm,
            controller=Controller(),
            browser_session=browser_session,
            validate_output=True,
        )
        
        # Execute task
        try:
            await agent.run(max_steps=max_steps)
            result = agent.last_response  # Get the last response from the agent
        finally:
            await browser_session.close()
            
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        print(f"Error executing task: {e}")

if __name__ == "__main__":
    mcp.run(transport="sse")