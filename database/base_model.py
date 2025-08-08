from datetime import datetime

from sqlalchemy import DateTime, func, update as sqlalchemy_update, select, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        _name = self.__name__
        _new_name = _name[0]
        for i in _name[1:]:
            if i.isupper():
                _new_name += '_'
            _new_name += i
        if _new_name[-1] == 'y':
            _new_name = _new_name[:-1] + 'ies'
        return _new_name.lower()


class Database:

    def __init__(self):
        self._engine = None
        self._session = None

    def init(self):
        self._engine = create_async_engine(settings.postgres_async_url)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)()

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as engine:
            await engine.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as engine:
            await engine.run_sync(Base.metadata.drop_all)


db = Database()
db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.id == id_)
        return (await db.execute(query)).scalar()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars()


class Model(Base, AbstractClass):
    __abstract__ = True


class CreatedModel(Model):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
