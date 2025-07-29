from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy() 


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False) 

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    followers: Mapped[list["Follower"]] = relationship("Follower", back_populates="user_to", foreign_keys="[Follower.user_to_id]")
    following: Mapped[list["Follower"]] = relationship("Follower", back_populates="user_from", foreign_keys="[Follower.user_from_id]")

    

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(300))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    
    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "timestamp": self.timestamp,
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
 
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "timestamp": self.timestamp
            # do not serialize the password, its a security breach
        }
    

class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_from: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")


    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            # do not serialize the password, its a security breach
        }
    
class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
            # do not serialize the password, its a security breach
        }
        
from eralchemy2 import render_er 

render_er(db.Model, 'diagram.png')