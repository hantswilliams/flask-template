from flask import Flask
from flasgger import Swagger
from app import create_app

app = create_app()
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Documentation",
        "description": "API documentation with authentication and role-based access control",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5027)
