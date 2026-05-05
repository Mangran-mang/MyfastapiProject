from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.model_base import Base


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="评论id")
    content: Mapped[
        str] = mapped_column(String(255, ), nullable=False, comment="评论内容", )
    post_id: Mapped[
        int] = mapped_column(Integer, ForeignKey("posts.id", onupdate="CASCADE"), nullable=False, comment="帖子id", )
    author_uid: Mapped[
        str] = mapped_column(String(36), ForeignKey("user.uid", onupdate="CASCADE"), nullable=False, comment="作者id", )
