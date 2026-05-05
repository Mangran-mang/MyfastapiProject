from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.model_base import Base

class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="token的id"
    )
    user_uid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user.uid",onupdate="CASCADE",ondelete="CASCADE"),# 父表主键更新，子表外键跟着更新),
        nullable= False,
        comment="用户id"
    )
    refresh_token: Mapped[str] = mapped_column(String(512),nullable= False,comment="刷新令牌")
    expire_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),nullable= False,comment="过期时间")

    user: Mapped["User"] = relationship("User",back_populates="token",uselist= False)# 一对一关系配置