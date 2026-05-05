from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from routers import user,posts,comments
from config import database_config
from models import model_base
import models
from tools.exceptions import http_exception_handler,db_exception_handler,sqlalchemy_exception_handler,other_exception_handler


# async def init_db() -> None:
#     async with database_config.async_engine.begin() as conn:
#         await conn.run_sync(model_base.Base.metadata.create_all)# 我这里第一次写时用成了会话工厂.create_all

def register_exception_handler(fapp):
    fapp.add_exception_handler(HTTPException, http_exception_handler)
    fapp.add_exception_handler(IntegrityError, db_exception_handler)
    fapp.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    fapp.add_exception_handler(Exception, other_exception_handler)



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("如果需要改ORM模型，则到main函数中重新启用init_db函数")
    # await init_db()
    yield
app = FastAPI(lifespan=lifespan)
# app.lifespan = lifespan
register_exception_handler(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # *代表所有，允许所有源访问
    allow_credentials=True,# 允许携带cookie
    allow_methods=["*"],# 允许所有请求方法
    allow_headers=["*"],# 允许所有请求头
)

app.include_router(user.router)
app.include_router(posts.router)
app.include_router(comments.router)