from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from .import db,login_manager


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
class Quote:
  '''
  Quote class to define Quote Objects
  '''

  def __init__(self,id,author,quote):
    self.id =id
    self.author = author
    self.quote= quote    

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer,primary_key = True)
  username = db.Column(db.String(255),index=True)
  email= db.Column(db.String(225),unique=True,index=True)
  pass_secure=db.Column(db.String(255))
  blogs= db.relationship('Blog',backref='user',lazy = "dynamic")
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

class Blog(db.Model):
  __tablename__ = 'blogs'

  id = db.Column(db.Integer,primary_key = True)
  name = db.Column(db.String(255))
  content=db.Column(db.String(255))
  category = db.Column(db.Integer,db.ForeignKey('categories.id'))
  vote = db.Column(db.Integer)
  user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
  comments = db.relationship('Comment',backref = 'blogs',lazy="dynamic")
  

  def __repr__(self):
    return f'User {self.name}'

  def save_blog(self):
    db.session.add(self)
    db.session.commit()  
  
  @classmethod
  def get_blogs(cls):
    blog = blog.query.all()
    return blogs  

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
  blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))


  def save_comment(self):
    db.session.add(self)
    db.session.commit()
   
  
  @classmethod
  def get_comments(cls):
    comment = comment.query.all()
    return comments

class PhotoProfile(db.Model):
  __tablename__='photoprofiles'
  id=db.Column(db.Integer,primary_key=True)
  pic_path = db.Column(db.String())
  user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
