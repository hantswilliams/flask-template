from app import create_app, db
from app.models import User, Role, Permission, CustomerMetaData, Order, OrderItem

app = create_app()

with app.app_context():
    db.create_all()

    ## Create roles and users
    if not User.query.first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)

        user1 = User(username='user1', email='user1@example.com', role='user')
        user1.set_password('password')
        db.session.add(user1)

        user2 = User(username='user2', email='user2@example.com', role='user')
        user2.set_password('password')
        db.session.add(user2)

        db.session.commit()
        print("Users created.")
    else:
        print("Database already populated.")

    ## Create a 'default' role
    if not Role.query.first():
        default_role = Role(name='default')
        db.session.add(default_role)
        db.session.commit()
        print("Default role created.")
    else:
        print("Default role already created.")

    # ## Make sure the 'admin' user has read, write, update, and delete permissions for all base API endpoints
    if not Permission.query.first():
        api_endpoints = ['/api/hello']
        for endpoint in api_endpoints:
            permission = Permission(
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

    ## Populate CustomerMetaData and Orders
    if not CustomerMetaData.query.first():
            customer1 = CustomerMetaData(name="John Doe", email="john.doe@example.com", phone="123-456-7890")
            order1 = Order(ordernumber="1001", customer=customer1)
            order_item1 = OrderItem(product_name="Widget A", quantity=10, order=order1)
            order_item2 = OrderItem(product_name="Widget B", quantity=5, order=order1)
            db.session.add_all([customer1, order1, order_item1, order_item2])

            customer2 = CustomerMetaData(name="Jane Doe", email="jane.doe@example.com", phone="123-456-7890")
            order2 = Order(ordernumber="1002", customer=customer2)
            order_item3 = OrderItem(product_name="Widget C", quantity=7, order=order2)
            order_item4 = OrderItem(product_name="Widget D", quantity=3, order=order2)
            db.session.add_all([customer2, order2, order_item3, order_item4])

            db.session.commit()
            print("CustomerMetaData, Order, and OrderItem populated.")
    else:
        print("CustomerMetaData already populated.")

