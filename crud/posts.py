from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func
from starlette import status

from models import User
from models.model_posts import Posts
from schemas.posts import PostsCreateModel, PostsUpdateModel


class PostService:
    async def crud_add_new_post(self,db:AsyncSession,post:PostsCreateModel):
        orm_post = Posts(**post.model_dump())
        db.add(orm_post)
        await db.commit()
        await db.refresh(orm_post)
        return orm_post

    async def crud_get_posts_list(
            self,
            db:AsyncSession,
            page:int=1,
            page_size:int=10,
            author_uid:str=None,
            current_user_uid:str=None
            ):
        """
        获取帖子列表
        拿到总列表数，以确定是否还有更多帖子
        如果没有指定作者的话，直接查所有帖子，并返回按创建时间排序好的帖子
        返回找到的帖子总数和查到的帖子的列表
        """

        stmt = select(Posts).order_by(Posts.created_time.desc())# 找帖子表的内容并按时间排序
        skip = (page -1)*page_size

        is_author = (author_uid == current_user_uid) if author_uid is not None else False  # 判断当前用户是否是作者

        if author_uid is not None:
            stmt = stmt.where(Posts.author_uid == author_uid)# 附加条件，要求帖子作者为指定作者
            stmt_count = select(func.count()).where(Posts.author_uid == author_uid,Posts.is_public or is_author)# 拿到指定作者的帖子数
            # 并减去私密帖子
        else:
            stmt_count = select(func.count()).where(Posts.is_public or is_author)# 如果未指定作者，则查询所有帖子的总数
        count_result = await db.execute(stmt_count)
        total = count_result.scalar_one_or_none()

        stmt = stmt.where(Posts.is_public or is_author)# 根据作者来决定是否公开所有帖子

        stmt = stmt.offset(skip).limit(page_size)

        result = await db.execute(stmt)
        post_list = result.scalars().all()
        return total,post_list

    async def crud_get_post_details_by_id(self,db:AsyncSession,post_id:int,current_user_uid:str):
        """
        通过id找到具体帖子
        根据帖子是否隐藏与当前用户是否是作者来决定是否显示
        返回的是一个ORM模型
        """
        stmt = select(Posts).where(Posts.id == post_id)
        result = await db.execute(stmt)
        post_detail = result.scalars().first()
        if post_detail.is_public or post_detail.author_uid == current_user_uid:
            return post_detail
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="无权限查看此帖子")

    async def crud_update_post(self,
            db:AsyncSession,
            post_id:int,
            post:PostsUpdateModel,
            user: User
    ):
        """
        与删除业务类似
        """
        orm_post = await self.crud_get_post_details_by_id(db,post_id,user.uid)
        if orm_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="帖子不存在")

        if orm_post.author_uid != user.uid and not user.is_superuser:# 如果用户不是管理员，和用户不是作者，则无权限修改
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="无权限修改此帖子")

        update_data = post.model_dump(exclude_unset= True)
        for key,value in update_data.items():
            setattr(orm_post,key,value)

        await db.commit()
        await db.refresh(orm_post)
        return orm_post



    async def crud_delete_post(self,db:AsyncSession,post_id:int,user: User):
        """
        删除帖子
        但要求是贴主或管理员身份

        将在路由函数中先拿到用户
        拿用户的方法是dependencies的get_user_by_token
        通过token拿用户
        然后再把User传进来拿uid
        """
        orm_post = await self.crud_get_post_details_by_id(db,post_id,user.uid)
        if orm_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
                )

        if orm_post.author_uid != user.uid and not user.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="无权限删除此帖子")

        stmt = delete(Posts).where(Posts.id == post_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount >0
