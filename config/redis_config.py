from redis.asyncio import Redis
from config.config import Config

JTI_EXPIRY = 3600# JTI就是JWT的ID

# 创建一个Redis客户端连接实例
token_blocklist = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True# 将返回值转换为字符串
)

async def add_jti_to_blocklist(jti: str):
    """
    将JTI添加到黑名单中
    默认过期时间为1小时
    """
    try:
        await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    except Exception as e:
        print(f"添加缓存失败{e}")

async def is_jti_in_blocklist(jti: str) -> bool:
    """
    检查JTI是否在黑名单中
    并返回True或False
    """
    try:
        jti = await token_blocklist.get(name=jti)
        return jti is not None
    except Exception as e:
        print(f"获取缓存失败{e}")
        return False
