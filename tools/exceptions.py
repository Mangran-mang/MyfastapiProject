# 全局异常处理模块
from fastapi import Request,HTTPException
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from fastapi.responses import JSONResponse
from starlette import status


# 三种不存在异常
async def post_not_found_error():
    pass

async def user_not_found_error():
    pass

async def comments_not_found_error():
    pass

# http异常
async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "异常类型": "HTTP异常",
            "异常信息": exc.detail,
        }
    )

# 数据库操作异常
async def db_exception_handler(request:Request,exc: IntegrityError):
    error_msg = str(exc.orig)  # orig 属性返回原始错误信息
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "用户不存在"
    else:
        detail = "数据库约束冲突"

    return JSONResponse(
        status_code= status.HTTP_400_BAD_REQUEST,
        content={
            "异常类型": "数据库异常",
            "异常定位":detail,
            "异常信息": str(exc),
        }
    )

# sqlalchemy异常
async def sqlalchemy_exception_handler(request:Request,exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "异常类型": "sqlalchemy异常",
            "异常信息": str(exc)
        }
    )

# 其他异常
async def other_exception_handler(request:Request,exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "异常类型": "其他异常",
            "异常信息": str(exc),
        }
    )