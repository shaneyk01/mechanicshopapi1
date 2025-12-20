from flask import Flask
from app.extensions import ma, limiter,cache
from app.models import db
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.serviceTickets import service_tickets_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_name):
    
    
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
   
    
    db.init_app(app)  
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    # Swagger UI at /docs, pointing to static swagger.yaml
    swagger_url = '/docs'
    api_url = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={'app_name': 'Mechanic Shop API'}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)
    return app