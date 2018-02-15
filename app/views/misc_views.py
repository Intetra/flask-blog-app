# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm, User
from app.models.blog_models import BlogPost, Comment

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    blogposts = BlogPost.query.order_by(BlogPost.created.desc()).all()
    comments = Comment.query.order_by(Comment.created.desc()).all()
    return render_template('pages/home_page.html', blogposts=blogposts, comments=comments)

@main_blueprint.route('/new_blog_post')
@login_required  # Limits access to authenticated users
def new_blog_post():
    return render_template('pages/new_blog_post.html')

@main_blueprint.route('/submit_blog_post', methods=['POST'])
@login_required  # Limits access to authenticated users
def submit_blog_post():
    user = User.query.get(request.form['user'])
    title = request.form['title']
    content = request.form['content']
    if len(title) > 200 or len(title) < 1:
        error = "Title must be between 1 and 200 characters"
        return render_template('pages/new_blog_post.html',
                                title=title,
                                content=content,
                                error=error)
    if len(content) > 1000 or len(content) < 1:
        error = "Post must be between 1 and 1000 characters"
        return render_template('pages/new_blog_post.html',
                                title=title,
                                content=content,
                                error=error)
    blogpost = BlogPost(user=user, title=title, content=content)
    db.session.add(blogpost)
    db.session.commit()
    return redirect(url_for("main.home_page"))

@main_blueprint.route('/submit_comment', methods=['POST'])
@login_required  # Limits access to authenticated users
def submit_comment():
    user = User.query.get(request.form['user'])
    content = request.form['content']
    blogpost = BlogPost.query.get(request.form['blogpost'])

    if len(content) > 1000 or len(content) < 1:
        error = "Comment must be between 1 and 1000 characters"
        blogposts = BlogPost.query.order_by(BlogPost.created.desc()).all()
        comments = Comment.query.order_by(Comment.created.desc()).all()
        return render_template('pages/home_page.html',
                                blogposts=blogposts,
                                comments=comments,
                                error_blogpost=blogpost,
                                comment_error=error)
    comment = Comment(user=user, blogpost=blogpost, content=content)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("main.home_page"))


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('pages/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(obj=current_user)
    blogposts = BlogPost.query.order_by(BlogPost.created.desc()).filter(BlogPost.user_id==current_user.id).all()
    comments = Comment.query.order_by(Comment.created.desc()).all()
    u_comments = Comment.query.order_by(Comment.created.desc()).filter(Comment.user_id==current_user.id).all()
    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form, blogposts=blogposts,
                           comments=comments, u_comments=u_comments)
