from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import User,Blog,Category,Comment,Vote
from .forms import UpdateProfile,BlogForm,CategoryForm,CommentForm
from ..import db,photos
from . import main 
from ..request import get_quotes

@app.route('/')
def index():

  '''
  View root page function that returns the index page and its data
  '''

  # Getting different quote
  different_quotes = get_quotes('different')
  print(different_quotes)
  title = 'Home - Welcome to the Blog-web page'
  return render_template('index.html', title = title,different = different_quotes)

@main.route('/')
def index():
  '''
  view root page function that returns the index page and its data
  '''
  # category = Category.query.all()
  category = Category.get_categories()

  return render_template('index.html',category = category)
@main.route('/add/category',methods=['GET','POST'])
@login_required
def new_category():
  '''
  viewnew group route function that returns a page with a form to create a category
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
@main.route('/categories/view_blog/<int:id>',methods=['GET','POST'])
@login_required
def view_blog(id):
  '''
  function that returns a single blog for comment to be added 
  '''
  print (id)
  blogs=Blog.query.get(id)
  if blogs is None:
    abort(404)
  comment=Comments.get_comments(id)
  return return_template('blog.html',blogs=blogs,comment=comment,category_id=id)
@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username = uname).first()

  if user is None:
    abort(404)
  return render_template("profile/profile.html", user = user)


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

