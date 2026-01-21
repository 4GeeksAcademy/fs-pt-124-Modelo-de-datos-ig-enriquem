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

    #foreign key

    #relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    user_comments: Mapped[List["Comment"]] = relationship(back_populates="comment_author")
    user_likes: Mapped[List["Like"]] = relationship(back_populates="like_user")
    follower_by: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.follower_by_user_id", back_populates="follower_by_user")
    follower_of: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.follower_of_user_id", back_populates="follower_of_user")
    
class Follower(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)

    #foreign key
    follower_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower_of_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #relationships
    follower_by_user: Mapped["User"] = relationship(foreign_keys=[follower_by_user_id], back_populates="follower_by")
    follower_of_user: Mapped["User"] = relationship(foreign_keys=[follower_of_user_id], back_populates="follower_of")
class Post(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    post_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_img: Mapped[str] = mapped_column(String(300), nullable=False)
    user_list: Mapped[str] = mapped_column(String(120), nullable=False)

    #foreign key
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    post_comments: Mapped[List["Comment"]] = relationship(back_populates="comment_post")
    post_likes: Mapped[List["Like"]] = relationship(back_populates="like_post")


class Comment(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    
    #foreign key
    comment_author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comment_post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    #relationships
    comment_author: Mapped["User"] = relationship(back_populates="user_comments")
    comment_post: Mapped["Post"] = relationship(back_populates="post_comments")

class Like(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)

    #foreign key
    like_post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    like_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #relationships
    like_post: Mapped["Post"] = relationship(back_populates="post_likes")
    like_user: Mapped["User"] = relationship(back_populates="user_likes")
