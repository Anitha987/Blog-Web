from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField,SubmitField,ValidationError,BooleanField,SelectField,RadioField
from wtforms.validators import Required
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
class PitchForm(FlaskForm):
    content = TextAreaField('Post your pitch')
    submit= SubmitField('Submit Pitch')
class CategoryForm(FlaskForm):
    name =TextAreaField('Category')
    submit = SubmitField()
class CommentForm(FlaskForm):
    comment = TextAreaField('comment',validators=[Required()])
    submit = SubmitField() 
    vote=RadioField('default field arguments',choices=[('1','UpVote'),('1','DownVote')])   
