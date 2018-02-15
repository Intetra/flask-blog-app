# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role
from app.models.blog_models import BlogPost, Comment


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    create_blogposts()
    create_comments()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user = find_or_create_user(
        u'Admin', u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(
        u'Member', u'Member', u'Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def create_blogposts():
    """ Create blog posts """
    users = User.query.all()
    for u in users:
        blogpost = BlogPost(user=u, title='title placeholder', content='blog post content placeholder')
        db.session.add(blogpost)
    db.session.commit()


def create_comments():
    """create comments"""
    users = User.query.all()
    blogposts = BlogPost.query.all()
    for b in blogposts:
        for u in users:
            comment = Comment(user=u, blogpost=b,
                            content='comment content placeholder')
            db.session.add(comment)
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(username, first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
