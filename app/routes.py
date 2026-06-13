from flask import Flask, request, jsonify
from scraper import scrape_info
from config_database import db, init_db, dict_to_invoice


app = Flask(__name__)
init_db(app)


@app.route('/api/v1/consult_invoice_information', methods=['POST'])
def consult_invoice_information():
    json_data = request.json or {}
    cufes = json_data.get('cufes')
    if not cufes:
        return jsonify({'error': "Falta el campo 'cufes' (lista de CUFEs)."}), 400

    try:
        result = scrape_info(cufes)

        for cufe, cufe_info in result.items():
            # dict_to_invoice ya construye la factura con sus eventos asociados;
            # al agregar la factura, la cascada persiste también los eventos.
            invoice = dict_to_invoice(cufe, cufe_info)
            db.session.add(invoice)

        db.session.commit()
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
