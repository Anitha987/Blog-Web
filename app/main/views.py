from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import User,Blog,Category,Comment,Subcription
from .forms import UpdateProfile,BlogForm,CategoryForm,CommentForm
from ..import db,photos
from . import main 
from ..requests import get_quotes
import datetime

@main.route('/')
def index():

  '''
  View root page function that returns the index page and its data
  '''
  new_category=Category.query.all()
  blogs=Blog.query.all()
  quote = get_quotes(category)

  
  return render_template('index.html',quote=quote,blogs=blogs,new_category=new_category)

@main.route('/add/category',methods=['GET','POST'])
@login_required
def new_category():
  '''
  view new group route function that returns a page with a form to create a category
  '''
  form = CategoryForm()
  if form.validate_on_submit():
    name = form.name.data
    new_category= Category(name=name)
    new_category.save_category()
    return redirect(url_for('.index'))
  title = 'New category'
  return render_template('new_category.html',Category_form=form,title=title)

    
@main.route('/categories/<int:id>')    
def category(id):
  category =Category.query.get(id)
  blogs = Blog.query.filter_by(category=id).all()                           
  return render_template('category.html',blogs=blogs,category=category)

@main.route('/categories/view_blog/add/<int:id>',methods=['GET','POST'])
@login_required
def new_blog(id):
  '''
  function to check blogs form and from the fields
  '''
  form = BlogForm()
  category= Category.query.filter_by(id=id).first()
  if category is None:
    abort(404)
  if form.validate_on_submit():
    content = form.content.data
    new_blog= Blog(content=content,category=category.id,user_id=current_user.id)
    new_blog.save_blog()
    return redirect(url_for('.category',id=category.id))
  title='New Blog'
  return render_template('new_blog.html',title=title,blog_form = form,category = category)

@main.route('/user/<uname>/blogs',methods=['GET','POST'])
def user_blogs(uname):
  user=User.query.filter_by(username=uname).first()
  blogs=Blog.query.filter_by(user_id = user.id).all()
  return render_template('blog.html', user = user,blogs= blogs)
  
@main.route('/categories/view_blog/<int:id>',methods=['GET','POST'])
@login_required
def view_blog(id):
  '''
  function that returns a single blog for comment to be added 
  '''
  print (id)
  blogs=Blog.query.get(id)
  posted_date=blog.posted.xxxtime('%b,%d,%Y')
  if blogs is None:
    abort(404)
  comment=Comments.get_comments(id)
  return redirect (url_for('.blog',id=blog.id))

  form = CommentForm()
  if form.validate_on_submit():
    comment = form.text.data
    new_comment = Comment(comment = comment,user= current_user,blog_id = blog)
    new_comment.save_comment()
    comments =Comment.get_comments(blog)
  return return_template('blog.html',blogs=blogs,comment=comment,category_id=id,comment_form=form,date = posted_date)
@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username = uname).first()

  if user is None:
    abort(404)
  return render_template("profile/profile.html", user = user)

@main.route('/subscribe/',methods = ['GET','POST'])
def subscribe():
  '''
  function thatenables one to make a subcribe on the blog
  '''
  form=SubscribeForm()
  if form.validate_on_submit():
    subscription = Subscription(email = form.email.data)
    db.session.add(subscription)
    db.session.commit()
    return redirect(url_for('main.index'))
  return render_template('subscribe.html',form=form) 
  

@main.route('/delete/<int:id>',methods = ['GET','POST'])  
def delete(id):
  blogs =Blog.query.filter_by(id=id).first()
  db.session.delete(blogs)
  db.session.commit()
  return redirect(url_for('.index')) 
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username = uname).first()
  if user is None:
    abort(404)
  form = UpdateProfile()
  if form.validate_on_submit():
      user.bio = form.bio.data
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('.profile',uname=user.username))
  return render_template('profile/update.html',form =form)  


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username = uname).first()
  if 'photo' in request.files:
      filename = photos.save(request.files['photo'])
      path = f'photos/{filename}'
      user.profile_pic_path = path
      db.session.commit()
  return redirect(url_for('main.profile',uname=uname))        

