from flask import Flask, request, jsonify
from scraper import scrape_info
from config_database import db, init_db,dict_to_invoice
from models import Invoice, Event


app = Flask(__name__)
init_db(app)




@app.route('/api/v1/consult_invoice_information', methods=['POST'])
def consult_invoice_information():
    try:
        json_data = request.json
        result = scrape_info(json_data['cufes'])

        for cufe, cufe_info in result.items():
            invoice = dict_to_invoice(cufe, cufe_info)
            db.session.add(invoice)

            for event_data in cufe_info["events"]:
                event = Event(
                    eventNumber=event_data["eventNumber"],
                    eventName=event_data["eventName"],
                    invoice=invoice
                )
                db.session.add(event)

        db.session.commit()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
