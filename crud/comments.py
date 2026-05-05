from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from models import User
from models.model_comments import Comments
from models.model_posts import Posts

from schemas.comments import CommentsCreateModel

class CommentsService:
    async def crud_add_new_comment_into_post(
            self,
            db:AsyncSession,
            comment:CommentsCreateModel,
            post_id:int,
            commenter_uid:str
    ):
        """
        用某个账户在某文章下发表评论

        添加评论需要：评论内容
        评论者信息(因为评论不涉及管理员权限，所以直接拿评论者uid即可)
        帖子信息

        评论需要用到联表查询
        返回ORM评论模型
        """
        orm_comment = Comments(
            content = comment.content,
            author_uid = commenter_uid,
            post_id = post_id
        )
        db.add(orm_comment)
        await db.commit()
        await db.refresh(orm_comment)
        return orm_comment


    async def crud_get_comments_by_post_id(
            self,
            db:AsyncSession,
            post_id:int,
            page:int=1,
            page_size:int=10
    ):
        """
        返回某个文章下的所有评论
        """
        # ===================拿评论总数======================
        stmt_count = select(func.count()).where(Comments.post_id == post_id)
        result = await db.execute(stmt_count)
        total = result.scalar_one_or_none()
        #=================================================

        offset = (page-1)*page_size
        # ==============关联查询==========================
        stmt = (select(Comments,Posts.created_time.label("post_created_time"),Posts.id.label("post_id"))
                .join(Posts,Comments.post_id == Posts.id)# 通过帖子id关联两个表
                .where(Comments.post_id == post_id)# 筛选出该文章下的所有评论
                .order_by(Comments.created_time.desc())# 按时间排序
                .offset(offset).limit(page_size)# 分页
                )

        result = await db.execute(stmt)
        comments_list = result.scalars().all()
        return total,comments_list

    async def crud_get_comment_by_comment_id(self, db: AsyncSession, comment_id: int):
        """
        通过评论id获取ORM评论
        """
        stmt = select(Comments).where(Comments.id == comment_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def crud_delete_comment_by_comment_id(
            self,
            db:AsyncSession,
            comment_id:int,
            current_user_uid:str,
            user:User
    ):
        """
        删除某个评论

        删评需要检查是评论者本人还是管理员
        """
        orm_comment = await self.crud_get_comment_by_comment_id(db,comment_id)
        if orm_comment is None:
            raise HTTPException(status_code=404,detail="该评论不存在")
        if orm_comment.author_uid != current_user_uid and not user.is_superuser:
            raise HTTPException(status_code=403,detail="没有权限删除该评论")

        stmt = delete(Comments).where(Comments.id == comment_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount >0