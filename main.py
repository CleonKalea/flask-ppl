from flask import Flask, jsonify, send_from_directory
import yfinance as yf
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)
CORS(app)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('RAILWAY_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        data.index = data.index.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(data.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Hello from backend-ppl"

@app.route('/stocklist', methods=['GET'])
def get_saham_data():
    try:
        query = text("SELECT * FROM tb_saham")
        result = db.session.execute(query)

        fetched_data = result.fetchall()
        print(f"Fetched {fetched_data} rows.") 

        column_names = ["id_saham", "kode_saham", "nama_perusahaan"]
        saham_list = []
        for row in fetched_data:
            row_dict = {}
            for index, value in enumerate(row):
                row_dict[column_names[index]] = value
            saham_list.append(row_dict)
        return jsonify(saham_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
