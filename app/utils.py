from flask import current_app

def get_api_endpoints():
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('api.'):  # Adjust this prefix as necessary for your API endpoints
            endpoints.append(rule.rule)
    return endpoints
