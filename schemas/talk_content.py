from pydantic import BaseModel, Field


class agent_talk(BaseModel):
    """
    对话内容
    """
    question: str = Field(...,description="问题",min_length=1,max_length=1000)