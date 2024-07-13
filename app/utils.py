from flask import current_app
from app.models import BaseUser, BaseRole, BasePermission, CustomerMetaData, Order, OrderItem

# A dictionary to map table names to their corresponding models
TABLE_MODEL_MAP = {
    'baseuser': BaseUser,
    'baserole': BaseRole,
    'basepermission': BasePermission,
    'customer_meta_data': CustomerMetaData,
    'order': Order,
    'item': OrderItem,
    'order_item': OrderItem,
}

def get_api_endpoints():
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('api.'):
            endpoints.append(rule.rule)
    return endpoints


