from typing import Optional

from pydantic import BaseModel


class PostsCreateModel(BaseModel):
    """
    需要标题、内容、作者uid
    """
    title: str
    content: str
    summary: Optional[str] = None
    is_public: bool = True
    author_uid: str

    model_config = {"from_attributes": True}

class PostsUpdateModel(BaseModel):
    """
    需要标题、内容
    """
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    is_public: Optional[bool] = True

    model_config = {"from_attributes": True}