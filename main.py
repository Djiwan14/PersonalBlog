import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
# postgresql://personalblog_jwpo_user:GnWg3iU9AQwqHYVBkSS2AAXlSgXo22D6@dpg-co97r65jm4es73aqkong-a.frankfurt-postgres.render.com/personalblog_jwpo
app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
location = "C:/Users/Shokhrukh N/Desktop/PycharmProjects/Python Web Programming/Flask BackEnd/67Day/instance/posts.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE")
# f'sqlite:///{location}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# FORM CREATION
app.config['SECRET_KEY'] = "Heyyo"
class NamerForm(FlaskForm):
    title = StringField("Blog Post title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your name", validators=[DataRequired()])
    img_url = StringField("Blog image url", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "date": self.date,
            "body": self.body,
            "author": self.author,
            "img_url": self.img_url,
        }

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show_post/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/add_new_post", methods=['GET', 'POST'])
def add_new_post():
    date = f'{datetime.datetime.now().month} {datetime.datetime.now().date()}, {datetime.datetime.now().year}'
    form = NamerForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            date=date,
            body=form.body.data,
            img_url=form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form, new_post=True)

# TODO: edit_post() to change an existing blog post

@app.route('/edit_post/<post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = NamerForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        date=post.date,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title=edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=edit_form, new_post=False)

# TODO: delete_post() to remove a blog post from the database

@app.route('/delete/<int:post_id>', methods=["GET", "POST", "DELETE"])
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
