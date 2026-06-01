from fastapi import APIRouter
from ai_agent.千问小柯 import agent_chat
from schemas.talk_content import agent_talk

router = APIRouter(prefix="/api/ai_agent",tags=["人工智能"])

@router.post("/test")
async def test_agent(
        input_content:agent_talk
):
    """
    测试人工智能
    """
    return agent_chat(input_content.question)