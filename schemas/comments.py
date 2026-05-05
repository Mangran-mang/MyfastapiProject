from pydantic import BaseModel


class CommentsCreateModel(BaseModel):
    content: str
    # comment_user_uid: str
    # post_id: int