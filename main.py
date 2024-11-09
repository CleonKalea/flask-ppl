from flask import Flask, jsonify, send_from_directory
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run()  # Set debug=False in production
