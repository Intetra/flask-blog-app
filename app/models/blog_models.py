from user_models import User
from datetime import datetime
from app import db

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship(User, backref=db.backref('blog_posts', lazy='dynamic'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship(User, backref=db.backref('comments', lazy='dynamic'))
    blogpost_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id', onupdate="CASCADE", ondelete="CASCADE"))
    blogpost = db.relationship(BlogPost, backref=db.backref('comments', lazy='dynamic'))
