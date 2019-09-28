from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from .import db,login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer,primary_key = True)
  username = db.Column(db.String(255),index=True)
  email= db.Column(db.String(225),unique=True,index=True)
  pass_secure=db.Column(db.String(255))
  pitches= db.relationship('Pitch',backref='user',lazy = "dynamic")
  comments= db.relationship('Comment',backref='user',lazy = "dynamic")
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String())
  password_hash = db.Column(db.String(255))
  photoprofiles = db.relationship('PhotoProfile',backref='user',lazy = "dynamic")
  @property
  def password(self):
      raise AttributeError('You cannot read the password attribute')

  @password.setter
  def password(self, password):
      self.pass_secure = generate_password_hash(password)


  def verify_password(self,password):
    return check_password_hash(self.pass_secure,password)

  def __repr__(self):
    return f'User {self.username}'

class Pitch(db.Model):
  __tablename__ = 'pitches'

  id = db.Column(db.Integer,primary_key = True)
  name = db.Column(db.String(255))
  # title=db.Column(db.String(255))
  content=db.Column(db.String(255))
  category = db.Column(db.Integer,db.ForeignKey('categories.id'))
  vote = db.Column(db.Integer)
  user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
  comments = db.relationship('Comment',backref = 'pitches',lazy="dynamic")
  votes = db.relationship('Vote',backref = 'pitches',lazy="dynamic")

  def __repr__(self):
    return f'User {self.name}'

  def save_pitch(self):
    db.session.add(self)
    db.session.commit()  
  
  @classmethod
  def get_pitches(cls):
    pitch = pitch.query.all()
    return pitches  

class Category(db.Model): 
  __tablename__= 'categories' 
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(255))

  def save_category(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_categories(cls):
    categories = Category.query.all()
    # category= Category.get_categories()
    return categories

class Comment(db.Model):
  __tablename__='comments'
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
  votes = db.relationship('Vote',backref = 'comments', lazy = "dynamic")

  def save_comment(self):
    db.session.add(self)
    db.session.commit()
   
  
  @classmethod
  def get_comments(cls):
    comment = comment.query.all()
    return comments

class Vote(db.Model):
  __tablename__='votes'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(225))
  vote=db.Column(db.Integer)
  pitch_id=db.Column(db.Integer,db.ForeignKey('pitches.id'))
  comment_id=db.Column(db.Integer,db.ForeignKey('comments.id'))

  def save_vote(self):
    db.session.add(self)
    db.session.commit()

  
  @classmethod
  def get_votes(cls,user_id,pitches_id):
    vote = vote.query.filter_by(user_id=user_id,pitches_id=pitches_id).all()
    return votes  
class PhotoProfile(db.Model):
  __tablename__='photoprofiles'
  id=db.Column(db.Integer,primary_key=True)
  pic_path = db.Column(db.String())
  user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
