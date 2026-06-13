import os
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus


db = SQLAlchemy()


def _database_uri() -> str:
    """Construye la URI de conexión a MySQL desde variables de entorno.

    Los valores por defecto son sólo para desarrollo local; en cualquier otro
    entorno deben definirse mediante variables de entorno (ver `.env.example`).
    """
    user = os.getenv("DB_USER", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", "root"))
    host = os.getenv("DB_HOST", "mysql")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "facturas_dian")
    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{name}"


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = _database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        

def dict_to_invoice(cufe, cufe_info):
    from models import Invoice, Event
    invoice = Invoice(
        cufe=cufe,
        seller_document=cufe_info["sellerInformation"]["Document"],
        seller_name=cufe_info["sellerInformation"]["Name"],
        receiver_document=cufe_info["receiverInformation"]["Document"],
        receiver_name=cufe_info["receiverInformation"]["Name"],
        link_graphic_representation=cufe_info["linkGraphicRepresentation"]
    )

    events_data = cufe_info.get("events", [])  
    for event_data in events_data:
        event = Event(
            eventNumber=event_data["eventNumber"],
            eventName=event_data["eventName"],
            invoice=invoice
        )
        invoice.events.append(event)

    return invoice
