from flask import Blueprint, request, jsonify
from app import db
from app.utils import TABLE_MODEL_MAP

crud = Blueprint('crud', __name__)

@crud.route('/api/<string:table_name>', methods=['GET'])
def get_items(table_name):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404
        
        items = model.query.all()
        items_dict = [item.as_dict() for item in items]
        print(f"Items: {items_dict}")
        return jsonify(items_dict), 200
    except Exception as e:
        print(f"Exception in get_items: {str(e)}")
        return jsonify({'message': str(e)}), 500

@crud.route('/api/<string:table_name>/<int:item_id>', methods=['GET'])
def get_item(table_name, item_id):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404
        
        item = model.query.get(item_id)
        if item is None:
            return jsonify({'message': 'Item not found'}), 404
        
        return jsonify(item.as_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@crud.route('/api/<string:table_name>', methods=['POST'])
def create_item(table_name):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404

        data = request.json
        item = model(**data)
        db.session.add(item)
        db.session.commit()
        return jsonify(item.as_dict()), 201
    except Exception as e:
        print(f"Exception in create_item: {str(e)}")
        return jsonify({'message': str(e)}), 500

@crud.route('/api/<string:table_name>/<int:item_id>', methods=['PUT'])
def update_item(table_name, item_id):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404

        data = request.json
        item = model.query.get(item_id)
        if item is None:
            return jsonify({'message': 'Item not found'}), 404

        for key, value in data.items():
            setattr(item, key, value)

        db.session.commit()
        return jsonify(item.as_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@crud.route('/api/<string:table_name>/<int:item_id>', methods=['DELETE'])
def delete_item(table_name, item_id):
    try:
        model = TABLE_MODEL_MAP.get(table_name)
        if not model:
            return jsonify({'message': f'Table {table_name} not found'}), 404

        item = model.query.get(item_id)
        if item is None:
            return jsonify({'message': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
