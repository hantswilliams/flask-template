from flask import current_app
from app.extensions import Base

# from app.models import BaseUser, BaseRole, BasePermission, CustomerMetaData, Order, OrderItem
# # A dictionary to map table names to their corresponding models
# TABLE_MODEL_MAP = {
#     'baseuser': BaseUser,
#     'baserole': BaseRole,
#     'basepermission': BasePermission,
#     'customer_meta_data': CustomerMetaData,
#     'order': Order,
#     'item': OrderItem,
#     'order_item': OrderItem,
# }

def get_api_endpoints():
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('api.'):
            endpoints.append(rule.rule)
    return endpoints


def get_table_model_map():
    table_model_map = {}
    for model_class in Base.registry._class_registry.values():
        if hasattr(model_class, '__tablename__'):
            table_model_map[model_class.__tablename__] = model_class
    return table_model_map


TABLE_MODEL_MAP = get_table_model_map()
