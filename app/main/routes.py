import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.utils import TABLE_MODEL_MAP

main = Blueprint('main', __name__)

def get_nested_data(obj, depth=1, parent_data=None):
    if depth > 3:  # Adjust the depth limit as needed
        return obj.__dict__
    
    data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    
    # Combine parent data with current data if parent_data is provided
    if parent_data:
        data.update(parent_data)

    print(f"Depth {depth}: {data}")  # Debugging print

    for key, value in obj.__dict__.items():
        if key.startswith('_') or key in data:  # Skip internal attributes and already added columns
            continue
        if isinstance(value, list):
            data[key] = [get_nested_data(v, depth + 1, data) for v in value]
        elif hasattr(value, '__dict__'):
            data[key] = get_nested_data(value, depth + 1, data)
        else:
            data[key] = value
    return data


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

@main.route('/get_tables', methods=['GET'])
def get_tables():
    tables = db.metadata.tables.keys()
    print(f"Tables: {tables}")
    return jsonify(list(tables))


@main.route('/datatable/<string:table_name>', methods=['GET'])
@main.route('/datatable/<string:table_name>/<int:item_id>', methods=['GET'])
def datatable(table_name, item_id=None):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404
        
        items = model.query.all()

        # Serialize items to dict
        items_dict = [item.as_dict() for item in items]

        # Create foreign key mapping dynamically
        foreign_key_mapping = {}
        for column in model.__table__.columns:
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    foreign_key_mapping[column.name] = fk.column.table.name


        # Print returned items data with rows
        print(f"Items: {items_dict}")

        # Return the data to the datatable.html
        return render_template('datatable.html', table_name=table_name, items=items_dict, item_id=item_id, foreign_key_mapping=foreign_key_mapping)

    except Exception as e:
        print(f"Exception in datatable: {str(e)}")
        return jsonify({'message': str(e)}), 500


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

