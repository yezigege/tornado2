from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from client.mysql import Base, NotNullColumn, DATETIME


class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = NotNullColumn(VARCHAR(50), unique=True, nullable=False)
    password = NotNullColumn(VARCHAR(50), nullable=False)
    last_login = NotNullColumn(DATETIME, default=datetime.now)

    def __repr__(self):
        return f'<User ===>{self.id}: {self.name}>'
