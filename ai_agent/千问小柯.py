from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from ai_agent.agent_tools import Tools
from config.config import Config

model = init_chat_model(
    model="qwen3.6-flash",           # 模型
    model_provider="openai",
    api_key=Config.API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",# URL 固定本地地址
    temperature=0.7,        # 创造力：0=严谨，1=发散，推荐0.5~0.9
    max_tokens=2048,        # 最大生成字数

)
AIRole = ("你的名字是小柯,今年23岁,"
          "不喜欢吃很腻的东西和难以入口的东西,但并不挑食,对花生和香蕉过敏,"
          "平常11:30和18:00下班"
          "回答问题时不要带备注,遇到时间相关问题时请调用工具"
          "请以俏皮且体贴的口吻回答用户的问题,且每次回答要有语气词")


tools = [Tools.get_current_time]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=AIRole,
    checkpointer=InMemorySaver(),# 短期记忆
)

def agent_chat(input_content):
    response = agent.invoke(
        {"messages": [
            {"role": "user", "content": input_content}
        ]},
        {"configurable": {"thread_id": "thread_1"}}
    )
    return response['messages'][-1].content