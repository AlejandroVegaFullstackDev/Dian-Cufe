from flask import Flask, request, jsonify
from scraper import scrape_invoice_information

app = Flask(__name__)

@app.route('/api/v1/consult_invoice_information', methods=['POST'])
def consult_invoice_information():
    try:
        cufes = request.json.get('cufes')
        if not cufes:
            return jsonify({"error": "No se proporcionaron CUFES"}), 400
        
        invoice_data = {}
        for cufe in cufes:
            invoice_info = scrape_invoice_information(cufe)
            invoice_data[cufe] = invoice_info
        
        return jsonify(invoice_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
