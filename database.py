from sqlalchemy import BigInteger, Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    volume_kind: Mapped[str] = mapped_column(
        Enum("piece", "kg", "litre", name="volume_kind")
    )


class Seller(Base):
    __tablename__ = "sellers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), unique=True)
    # rate


class Buyer(Base):
    __tablename__ = "buyers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), unique=True)
    # rate


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    volume: Mapped[int]
    price: Mapped[int]
    description: Mapped[str]
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))


# class Deal(Base)
# class Comment(Base)
# class Rate(Base)
