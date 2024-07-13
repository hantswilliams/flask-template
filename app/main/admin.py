import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import BaseUser, BaseRole, BasePermission
from app.forms import RegistrationForm, AdminCreateRoleForm, AdminSetPermissionsForm
from app.utils import get_api_endpoints

admin = Blueprint('admin', __name__)

@admin.route("/", methods=['GET', 'POST'])
@login_required
def admin_home():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))

    create_user_form = RegistrationForm()
    create_role_form = AdminCreateRoleForm()
    set_permissions_form = AdminSetPermissionsForm()

    roles = BaseRole.query.all()
    users = BaseUser.query.all()

    set_permissions_form.role.choices = [(role.name, role.name) for role in roles]
    set_permissions_form.user.choices = [(user.id, user.username) for user in users]

    api_endpoints = get_api_endpoints()
    set_permissions_form.endpoint.choices = [(endpoint, endpoint) for endpoint in api_endpoints]

    if create_user_form.validate_on_submit() and request.form.get('form_name') == 'create_user_form':
        user = BaseUser(username=create_user_form.username.data, email=create_user_form.email.data, role=request.form.get('role'))
        user.set_password(create_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.admin_home'))

    if create_role_form.validate_on_submit() and request.form.get('form_name') == 'create_role_form':
        role = BaseRole(name=create_role_form.role.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully!', 'success')
        return redirect(url_for('admin.admin_home'))

    if set_permissions_form.validate_on_submit() and request.form.get('form_name') == 'set_permissions_form':
        existing_permission = BasePermission.query.filter_by(
            user_id=set_permissions_form.user.data,
            endpoint=set_permissions_form.endpoint.data,
            role=set_permissions_form.role.data
        ).first()
        
        if existing_permission:
            flash('This user already has permissions for this API endpoint and role.', 'warning')
        else:
            permission = BasePermission(
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
        return redirect(url_for('admin.admin_home'))

    permissions = db.session.query(BasePermission, BaseUser).join(BaseUser).all()

    return render_template('admin.html', create_user_form=create_user_form, create_role_form=create_role_form, set_permissions_form=set_permissions_form, roles=roles, users=users, permissions=permissions)

@admin.route("/edit_user/<int:user_id>", methods=['POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    user = BaseUser.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@admin.route("/delete_user/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    user = BaseUser.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')    
    return jsonify({'message': 'User deleted successfully'})

# soft delete user
@admin.route("/soft_delete_user/<int:user_id>", methods=['POST'])
@login_required
def soft_delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    user = BaseUser.query.get_or_404(user_id)
    user.active = False
    db.session.commit()
    return jsonify({'message': 'User deactivated successfully'})

# restore user
@admin.route("/restore_user/<int:user_id>", methods=['POST'])
@login_required
def restore_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    user = BaseUser.query.get_or_404(user_id)
    user.active = True
    db.session.commit()
    return jsonify({'message': 'User restored successfully'})

@admin.route("/update_permission", methods=['POST'])
@login_required
def update_permission():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    user_id = data['user_id']
    endpoint = data['endpoint']
    permission = data['permission']
    value = data['value']

    perm = BasePermission.query.filter_by(user_id=user_id, endpoint=endpoint).first()
    if not perm:
        return jsonify({'message': 'Permission not found'}), 404

    if permission == 'read':
        perm.can_read = value
    elif permission == 'write':
        perm.can_write = value
    elif permission == 'update':
        perm.can_update = value
    elif permission == 'delete':
        perm.can_delete = value

    db.session.commit()
    return jsonify({'message': 'Permission updated successfully'})

@admin.route("/delete_permission", methods=['DELETE'])
@login_required
def delete_permission():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    user_id = data['user_id']
    endpoint = data['endpoint']

    perm = BasePermission.query.filter_by(user_id=user_id, endpoint=endpoint).first()
    if not perm:
        return jsonify({'message': 'Permission not found'}), 404

    db.session.delete(perm)
    db.session.commit()
    flash('Permission deleted successfully!', 'success')
    return jsonify({'message': 'Permission deleted successfully'})

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
