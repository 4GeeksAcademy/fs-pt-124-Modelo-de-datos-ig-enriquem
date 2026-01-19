from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    followers: Mapped[List["Follower"]] = relationship(back_populates="user")
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    likes: Mapped[List["Like"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Follower(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    follow_of: Mapped[int] = mapped_column(nullable=False)
    follow_by: Mapped[int] = mapped_column(nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    post_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_img: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    id_user: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="posts")
    likes: Mapped[List["Like"]] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Comment(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Like(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_list: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="likes")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }