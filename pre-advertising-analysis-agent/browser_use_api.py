"""
FastAPI wrapper for browser automation using CDP.
"""

import os
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrockConverse
from browser_use import Agent
from browser_use.browser import BrowserSession
from browser_use.controller.service import Controller

app = FastAPI(title="Browser Automation API",
             description="API for browser automation using CDP")

class BrowserRequest(BaseModel):
    task: str
    cdp_url: str = "http://localhost:9222"
    max_steps: int = 30

def get_llm():
    config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', config=config)

    return ChatBedrockConverse(
        model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        temperature=0.0,
        max_tokens=None,
        client=bedrock_client,
    )

@app.post("/execute_task")
async def execute_task(request: BrowserRequest):
    try:
        # Initialize browser session
        browser_session = BrowserSession(cdp_url=request.cdp_url)
        
        # Initialize LLM
        llm = get_llm()
        
        # Create agent
        agent = Agent(
            task=request.task,
            llm=llm,
            controller=Controller(),
            browser_session=browser_session,
            validate_output=True,
        )
        
        # Execute task
        try:
            await agent.run(max_steps=request.max_steps)
            result = agent.last_response  # Get the last response from the agent
        finally:
            await browser_session.close()
            
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)