from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='False')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey('all_users.id', ondelete="CASCADE"), nullable=False)
## referencing the class not the table
    owner = relationship("User")
    def __repr__(self):
        return f"Item title: {self.title}, published: {self.published}"


class User(Base):
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
