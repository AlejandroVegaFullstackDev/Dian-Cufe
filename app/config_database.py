from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus


db = SQLAlchemy()

def init_db(app):
    password = quote_plus("RRoot123!@#")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{password}@localhost/facturas_dian'
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
