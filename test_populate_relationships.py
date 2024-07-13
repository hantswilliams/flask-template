from app import create_app
from app.models import CustomerMetaData

app = create_app()

with app.app_context():
    customers = CustomerMetaData.query.all()
    for customer in customers:
        print(customer.as_dict())