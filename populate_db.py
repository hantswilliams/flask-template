from app import create_app, db
from app.models import BaseUser, BaseRole, BasePermission, Customer, Order, OrderItem, Product

app = create_app()

with app.app_context():
    db.create_all()

    ## Create roles and users
    if not BaseUser.query.first():
        admin = BaseUser(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)

        user1 = BaseUser(username='user1', email='user1@example.com', role='user')
        user1.set_password('password')
        db.session.add(user1)

        user2 = BaseUser(username='user2', email='user2@example.com', role='user')
        user2.set_password('password')
        db.session.add(user2)

        db.session.commit()
        print("Users created.")
    else:
        print("Database already populated.")

    ## Create a 'default' role
    if not BaseRole.query.first():
        default_role = BaseRole(name='default')
        db.session.add(default_role)
        db.session.commit()
        print("Default role created.")
    else:
        print("Default role already created.")

    # ## Make sure the 'admin' user has read, write, update, and delete permissions for all base API endpoints
    if not BasePermission.query.first():
        api_endpoints = ['/api/hello']
        for endpoint in api_endpoints:
            permission = BasePermission(
                user_id=1,
                endpoint=endpoint,
                role='admin',
                can_read=True,
                can_write=True,
                can_update=True,
                can_delete=True
            )
            db.session.add(permission)
        db.session.commit()
        print("Permissions created.")

    # Populate Products
    if not Product.query.first():
        product_names = [
            {"name": "Widget A", "price": 10.0},
            {"name": "Widget B", "price": 12.0},
            {"name": "Widget C", "price": 8.0},
            {"name": "Widget D", "price": 15.0},
            {"name": "Widget E", "price": 9.0},
            {"name": "Widget F", "price": 11.0},
            {"name": "Widget G", "price": 13.0},
            {"name": "Widget H", "price": 7.0},
            {"name": "Widget I", "price": 14.0},
            {"name": "Widget J", "price": 6.0},
        ]
        for product_data in product_names:
            product = Product(name=product_data['name'], price=product_data['price'])
            db.session.add(product)
        db.session.commit()
        print("Products created.")
    else:
        print("Products already populated.")

    if not Customer.query.first():
        customer1 = Customer(name="John Doe", email="john.doe@example.com", phone="123-456-7890")
        order1 = Order(ordernumber="1001", customer=customer1)

        customer2 = Customer(name="Jane Doe", email="jane.doe@example.com", phone="123-456-7890")
        order2 = Order(ordernumber="1002", customer=customer2)

        db.session.add_all([customer1, order1, customer2, order2])
        db.session.commit()

        # Fetch products from the database
        product1 = Product.query.filter_by(name="Widget A").first()
        product2 = Product.query.filter_by(name="Widget B").first()
        product3 = Product.query.filter_by(name="Widget C").first()
        product4 = Product.query.filter_by(name="Widget D").first()

        order_item1 = OrderItem(product=product1, quantity=10, associated_order_id=order1.id)
        order_item2 = OrderItem(product=product2, quantity=5, associated_order_id=order1.id)
        order_item3 = OrderItem(product=product3, quantity=7, associated_order_id=order2.id)
        order_item4 = OrderItem(product=product4, quantity=3, associated_order_id=order2.id)
        db.session.add_all([order_item1, order_item2, order_item3, order_item4])

        db.session.commit()
        print("Customer, Order, and OrderItem populated.")
    else:
        print("Data already populated.")

