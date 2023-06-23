from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    author_id = Column(Integer,
                       ForeignKey("user.id", ondelete="CASCADE"),
                       nullable=False)
    author = relationship('User')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'vote'

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"),
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"),
                     primary_key=True, nullable=False)