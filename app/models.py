from config_database import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cufe = db.Column(db.String(100))
    seller_document = db.Column(db.String(255))
    seller_name = db.Column(db.String(255))
    receiver_document = db.Column(db.String(255))
    receiver_name = db.Column(db.String(255))
    link_graphic_representation = db.Column(db.String(255))
    events = db.relationship('Event', backref='invoice', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventNumber = db.Column(db.String(10))
    eventName = db.Column(db.String(255))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)

