from flask import Flask, request, jsonify
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from scraping import scrape_info
import json
import time

app = Flask(__name__)


@app.route('/api/v1/consult_invoice_information', methods=['POST'])
def consult_invoice_information():
    try:
        json_data = request.json
        result = scrape_info(json_data['cufes'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
