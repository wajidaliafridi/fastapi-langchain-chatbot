from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from app.backend.db_conn.database_conn import Base, engine, get_db

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String, unique=True)
    password_hashed = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Integer, default=1)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, password_hashed={self.password_hashed}, created_at={self.created_at}, is_active={self.is_active})"
    



class UserMessages(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"UserMessages(user_id={self.user_id}, message={self.message}, created_at={self.created_at})"



Base.metadata.create_all(bind=engine)



