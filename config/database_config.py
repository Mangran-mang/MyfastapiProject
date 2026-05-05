from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "mysql+aiomysql://root:123456@127.0.0.1:3306/mangran?charset=utf8mb4"

# 数据库引擎
async_engine = create_async_engine(DATABASE_URL, echo=True,pool_size=10,max_overflow=20)

# 会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_= AsyncSession,# 指定会话类型是异步，AsyncSession是ORM会话
    expire_on_commit=False# 提交事务后依然可以访问那个orm对象
)

async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise