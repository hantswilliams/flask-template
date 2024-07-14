from datetime import datetime
from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return BaseUser.query.get(int(user_id))

class BaseUser(db.Model, UserMixin):
    __tablename__ = 'baseuser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 

class BaseRole(db.Model):
    __tablename__ = 'baserole'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class BasePermission(db.Model):
    __tablename__ = 'basepermission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('baseuser.id'), nullable=False)
    endpoint = db.Column(db.String(128))
    role = db.Column(db.String(64))
    can_read = db.Column(db.Boolean, default=False)
    can_write = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    user = db.relationship('BaseUser', backref=db.backref('basepermissions', lazy=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    orders = db.relationship('Order', backref=db.backref('customer'), lazy='joined', cascade='all, delete-orphan')

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['order'] = [order.as_dict() for order in self.orders]
        return data

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordernumber = db.Column(db.String(128), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_item = db.relationship('OrderItem', backref=db.backref('order'), lazy='joined', cascade='all, delete-orphan')

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['order_item'] = [item.as_dict() for item in self.order_item]
        return data

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    associated_order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('order_item', lazy=True))

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['product'] = self.product.as_dict() if self.product else None
        return data
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    

