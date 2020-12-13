import os
import secrets
from PIL import Image
from flask import url_for, current_app, request, abort
from flask_mail import Message
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from functools import wraps
from ListDoMikolaja import mail
from ListDoMikolaja.models import Role

def save_picture(form_picture, output_size = (125, 125)):
    #form_picture - data from form of file
    random_hex = secrets.token_hex(8)
    _f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #resize the picture
    i = Image.open(form_picture)
    i.thumbnail = output_size
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='kuczak.tomasz@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this email and no changes will be made.
    '''
    mail.send(msg)

def role_required(role_name):
    '''
    Required roles have to be passed in a list. There will be an or logical sign between the roles in the list.
    For example passing role_required(['Admin', 'Writer]) enforces the user to have Admin OR Writer role.

    This decorator combines the functionality of login_required decorator and role_required.
    It first checks if the user is logged in, if not send the user to login page.
    If the user is logged in and has the required role it returns the wrapped route.
    If the user does not have the requred role it returns current_app.login_manager.unauthorized()
    '''
    def inner_function(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not type(role_name) == list:
                raise ValueError('Pass a list as an argument')

            #checks if the specified role exists
            if not set(role_name).intersection([role.name for role in Role.query.all()]):
                raise ValueError('Specified role required does not exist')

            #if the request method is in EXEMPT_METHODS or the LOGIN is disabled return the route
            #without the need to login
            if request.method in EXEMPT_METHODS or current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)

            #check is the current_user is logged in
            if current_user.is_authenticated:
                 #if the specified role is in current_user's roles
                if set(role_name).intersection(current_user.roles_names):
                    return func(*args, **kwargs)
                else:
                    abort(403)
            else:
                return current_app.login_manager.unauthorized()

        return decorated_view
    return inner_function
