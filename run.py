from flask import Flask
from flasgger import Swagger
from app import create_app

app = create_app()
swagger = Swagger(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5027)
