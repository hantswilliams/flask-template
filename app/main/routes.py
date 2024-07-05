import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Role, Permission
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminCreateRoleForm, AdminSetPermissionsForm
from app.utils import get_api_endpoints


main = Blueprint('main', __name__)

@main.app_errorhandler(401)
def error_401(error):
    return render_template('errors/401.html'), 401

@main.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

@main.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@main.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    create_user_form = RegistrationForm()
    create_role_form = AdminCreateRoleForm()
    set_permissions_form = AdminSetPermissionsForm()
    
    roles = Role.query.all()
    users = User.query.all()
    
    set_permissions_form.role.choices = [(role.name, role.name) for role in roles]
    set_permissions_form.user.choices = [(user.id, user.username) for user in users]
    
    api_endpoints = get_api_endpoints()
    set_permissions_form.endpoint.choices = [(endpoint, endpoint) for endpoint in api_endpoints]
    
    if create_user_form.validate_on_submit() and request.form.get('form_name') == 'create_user_form':
        user = User(username=create_user_form.username.data, email=create_user_form.email.data, role=request.form.get('role'))
        user.set_password(create_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if create_role_form.validate_on_submit() and request.form.get('form_name') == 'create_role_form':
        role = Role(name=create_role_form.role.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if set_permissions_form.validate_on_submit() and request.form.get('form_name') == 'set_permissions_form':
        permission = Permission(
            user_id=set_permissions_form.user.data,
            endpoint=set_permissions_form.endpoint.data,
            role=set_permissions_form.role.data,
            can_read=set_permissions_form.can_read.data,
            can_write=set_permissions_form.can_write.data,
            can_update=set_permissions_form.can_update.data,
            can_delete=set_permissions_form.can_delete.data
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permissions set successfully!', 'success')
        return redirect(url_for('main.admin'))

    return render_template('admin.html', create_user_form=create_user_form, create_role_form=create_role_form, set_permissions_form=set_permissions_form, roles=roles)
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    create_user_form = RegistrationForm()
    create_role_form = AdminCreateRoleForm()
    set_permissions_form = AdminSetPermissionsForm()
    
    roles = Role.query.all()
    users = User.query.all()
    
    set_permissions_form.role.choices = [(role.name, role.name) for role in roles]
    set_permissions_form.user.choices = [(user.id, user.username) for user in users]
    
    api_endpoints = get_api_endpoints()
    set_permissions_form.endpoint.choices = [(endpoint, endpoint) for endpoint in api_endpoints]
    
    if create_user_form.validate_on_submit() and request.form.get('form_name') == 'create_user_form':
        user = User(username=create_user_form.username.data, email=create_user_form.email.data, role=request.form.get('role'))
        user.set_password(create_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if create_role_form.validate_on_submit() and request.form.get('form_name') == 'create_role_form':
        role = Role(name=create_role_form.role.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if set_permissions_form.validate_on_submit() and request.form.get('form_name') == 'set_permissions_form':
        permission = Permission(
            user_id=set_permissions_form.user.data,
            endpoint=set_permissions_form.endpoint.data,
            role=set_permissions_form.role.data,
            can_read=set_permissions_form.can_read.data,
            can_write=set_permissions_form.can_write.data,
            can_update=set_permissions_form.can_update.data,
            can_delete=set_permissions_form.can_delete.data
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permissions set successfully!', 'success')
        return redirect(url_for('main.admin'))

    return render_template('admin.html', create_user_form=create_user_form, create_role_form=create_role_form, set_permissions_form=set_permissions_form, roles=roles)
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    create_user_form = RegistrationForm()
    create_role_form = AdminCreateRoleForm()
    set_permissions_form = AdminSetPermissionsForm()
    
    roles = Role.query.all()
    set_permissions_form.role.choices = [(role.name, role.name) for role in roles]
    
    api_endpoints = get_api_endpoints()
    set_permissions_form.endpoint.choices = [(endpoint, endpoint) for endpoint in api_endpoints]
    
    if create_user_form.validate_on_submit() and request.form.get('form_name') == 'create_user_form':
        user = User(username=create_user_form.username.data, email=create_user_form.email.data, role=request.form.get('role'))
        user.set_password(create_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if create_role_form.validate_on_submit() and request.form.get('form_name') == 'create_role_form':
        role = Role(name=create_role_form.role.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully!', 'success')
        return redirect(url_for('main.admin'))
    
    if set_permissions_form.validate_on_submit() and request.form.get('form_name') == 'set_permissions_form':
        permission = Permission(
            endpoint=set_permissions_form.endpoint.data,
            role=set_permissions_form.role.data,
            can_read=set_permissions_form.can_read.data,
            can_write=set_permissions_form.can_write.data,
            can_update=set_permissions_form.can_update.data,
            can_delete=set_permissions_form.can_delete.data
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permissions set successfully!', 'success')
        return redirect(url_for('main.admin'))

    return render_template('admin.html', create_user_form=create_user_form, create_role_form=create_role_form, set_permissions_form=set_permissions_form, roles=roles)
    