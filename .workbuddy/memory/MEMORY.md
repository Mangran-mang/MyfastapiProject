# FastAPI School Discussion Platform - Project Notes

## Project Structure
- FastAPI + SQLAlchemy async + MySQL + Redis
- MVC-like: models/ schemas/ crud/ routers/ separation
- JWT double-token auth with Redis JTI blacklist logout
- Alembic migrations

## Key Decisions
- `UserUpdateModel.is_active` type: `Optional[bool]` (NOT `str`)
- Posts author_uid is ALWAYS set from token, never from frontend request body
- Visibility: public posts visible to all; private posts only visible to author
- Delete/update user: only self or superuser permitted
- Category CRUD: admin-only for create/update/delete
- Comments: parent_id for nested replies, Text type for content (unlimited length)
- Like/Bookmark: toggle-style (same endpoint for on/off)
- Notification types: reply / like / system

## Templates & Conventions
- Response format: `{"code": int, "message": str, "data": any}` (from original code)
- Exception handling uses FastAPI exception handlers registered in main.py
- Router prefix convention: /api/{resource}
