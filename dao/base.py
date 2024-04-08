import logging

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from database import User, async_session_maker

logger = logging.getLogger(__name__)


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def upsert(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data)
                await session.execute(query)
            except IntegrityError:
                await session.rollback()
                query = (
                    update(User)
                    .where(User.tg_id == data.get("tg_id"))
                    .values(name=data.get("name"))
                )
                await session.execute(query)
            await session.commit()
