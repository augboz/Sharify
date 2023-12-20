from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(100))
    song_name = db.Column(db.String(100))
    song_artist = db.Column(db.String(1000))
    song_link = db.Column(db.String(1000))
    audio_link = db.Column(db.String(1000))
    album_cover = db.Column(db.String(1000))
    caption = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    date =db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150))
    email=db.Column(db.String(150), unique=True)
    password= db.Column(db.String(600))
    profile_pic = db.Column(db.String(6000))
    bio = db.Column(db.String(150))
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    num_of_posts = db.Column(db.Integer)
    posts = db.relationship('Post')


class Follow(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username_follower = db.Column(db.String(150))
    username_followed = db.Column(db.String(150))
    accepted = db.Column(db.Boolean, default=False)


from sqlalchemy.orm import relationship

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_liker = db.Column(db.String(150))
    username_liked = db.Column(db.String(150))
    liked_post_name = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    user = relationship('User', backref='likes_given', foreign_keys=[user_id])
    post_rel = relationship('Post', backref='likes_rel')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment_text = db.Column(db.String(1000), nullable=False)