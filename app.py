from flask import Flask, jsonify

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
