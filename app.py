import os

from flask import Flask, jsonify, request, send_from_directory

import payment_store

app = Flask(__name__)
_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(_ROOT, 'index.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = [
        {'nombre': 'Cliente A'},
        {'nombre': 'Cliente B'},
        {'nombre': 'Cliente C'}
    ]
    return jsonify(clientes), 200


@app.route('/pagos', methods=['GET'])
def list_pagos():
    return jsonify(payment_store.list_payments()), 200


@app.route('/pagos', methods=['POST'])
def crear_pago():
    data = request.get_json(silent=True) or {}
    monto = data.get('monto')
    concepto = data.get('concepto')

    if monto is None or concepto is None:
        return jsonify({'error': 'monto y concepto son obligatorios'}), 400

    try:
        monto_float = float(monto)
    except (TypeError, ValueError):
        return jsonify({'error': 'monto debe ser numérico'}), 400

    if monto_float <= 0:
        return jsonify({'error': 'monto debe ser mayor que cero'}), 400

    if not str(concepto).strip():
        return jsonify({'error': 'concepto no puede estar vacío'}), 400

    cliente = data.get('cliente')
    pago = payment_store.create_payment(monto_float, str(concepto), cliente)
    return jsonify(pago), 201


@app.route('/metricas', methods=['GET'])
def metricas():
    return jsonify(payment_store.get_metrics()), 200


if __name__ == '__main__':
    app.run(debug=True)
