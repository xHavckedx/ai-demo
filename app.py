from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

_pagos: list[dict] = []


def _procesar_pago_mock(monto: float, descripcion: str) -> dict:
    """Simula el procesamiento de un pago (sin pasarela real)."""
    if monto < 0.01:
        estado = "fallido"
        mensaje = "Monto inválido"
    else:
        estado = "completado"
        mensaje = "Pago procesado correctamente (mock)"
    pago = {
        "id": str(uuid4()),
        "monto": round(monto, 2),
        "descripcion": descripcion,
        "estado": estado,
        "mensaje": mensaje,
        "creado_en": datetime.now(timezone.utc).isoformat(),
    }
    _pagos.append(pago)
    return pago


def _calcular_metricas() -> dict:
    total = len(_pagos)
    completados = sum(1 for p in _pagos if p["estado"] == "completado")
    fallidos = sum(1 for p in _pagos if p["estado"] == "fallido")
    volumen = sum(p["monto"] for p in _pagos if p["estado"] == "completado")
    tasa_exito = (completados / total * 100) if total else 0.0
    return {
        "total_pagos": total,
        "pagos_completados": completados,
        "pagos_fallidos": fallidos,
        "volumen_completado": round(volumen, 2),
        "tasa_exito_porcentaje": round(tasa_exito, 2),
    }


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = [
        {"nombre": "Cliente A"},
        {"nombre": "Cliente B"},
        {"nombre": "Cliente C"},
    ]
    return jsonify(clientes), 200


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(Path(__file__).resolve().parent, "index.html")


@app.route("/api/pagos", methods=["GET"])
def listar_pagos():
    return jsonify(list(reversed(_pagos))), 200


@app.route("/api/pagos", methods=["POST"])
def crear_pago():
    data = request.get_json(silent=True) or {}
    try:
        monto = float(data.get("monto", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "monto debe ser numérico"}), 400
    descripcion = str(data.get("descripcion", "")).strip() or "Pago sin descripción"
    pago = _procesar_pago_mock(monto, descripcion)
    status = 201 if pago["estado"] == "completado" else 422
    return jsonify(pago), status


@app.route("/api/metricas", methods=["GET"])
def metricas():
    return jsonify(_calcular_metricas()), 200


def reset_pagos() -> None:
    """Vacía el almacén en memoria (útil en tests)."""
    _pagos.clear()


if __name__ == "__main__":
    app.run(debug=True)
