from flask import Blueprint, request, jsonify
from app import db
from app.utils import TABLE_MODEL_MAP
from sqlalchemy import inspect

crud = Blueprint('crud', __name__)

def propagate_changes(model, changes):
    """
    Propagate changes to related tables dynamically.
    """
    try:
        session = db.session
        inspector = inspect(model)

        # Print all relationships for debugging
        print(f"Inspecting relationships for model: {model.__name__}")
        for rel in inspector.relationships:
            print(f"Relationship: {rel.key}, Mapper: {rel.mapper}, Local Columns: {rel.local_columns}, Remote Columns: {rel.remote_side}")

        for key, (old_value, new_value) in changes.items():
            if key == 'id':
                new_id = new_value
                old_id = old_value

                # Log the relationship details
                print(f"Propagating changes for key: {key}, old_id: {old_id}, new_id: {new_id}")

                # Find relationships where this model is the parent
                for rel in inspector.relationships:
                    related_model = rel.mapper.class_
                    remote_columns = {col.name for col in rel.remote_side}
                    local_columns = {col.name for col in rel.local_columns}

                    # Ensure we're updating the correct foreign key column in the related model
                    if key in local_columns:
                        for remote_column in remote_columns:
                            # Log related model and column details
                            print(f"Related model: {related_model.__tablename__}, Related column: {remote_column}")

                            # Update related models
                            rows = session.query(related_model).filter(getattr(related_model, remote_column) == old_id).all()
                            for row in rows:
                                setattr(row, remote_column, new_id)
                                session.add(row)
                                # Log each updated row
                                print(f"Updated {related_model.__tablename__} row id: {row.id} with new {remote_column}: {new_id}")
                session.commit()
    except Exception as e:
        print(f"Exception in propagate_changes: {str(e)}")
        session.rollback()





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

        ## print new data request and old data
        print(f"PUT Data Request: {data}")
        print(f"PUT Item Current: {item.as_dict()}")
        changes = {key: (getattr(item, key), value) for key, value in data.items() if getattr(item, key) != value}
        print(f"PUT Changes: {changes}")

        if item is None:
            return jsonify({'message': 'Item not found'}), 404

        for key, value in data.items():
            setattr(item, key, value)

        db.session.commit()

        # Propagate changes to related tables
        propagate_changes(model, changes)

        db.session.commit()
        return jsonify(item.as_dict()), 200
    except Exception as e:
        print(f"Exception in update_item: {str(e)}")
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
