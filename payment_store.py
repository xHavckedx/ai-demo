"""Almacén en memoria para pagos mock y métricas derivadas."""

from __future__ import annotations

import statistics
import uuid
from datetime import datetime, timezone
from typing import Any

_payments: list[dict[str, Any]] = []


def create_payment(monto: float, concepto: str, cliente: str | None = None) -> dict[str, Any]:
    payment = {
        "id": str(uuid.uuid4()),
        "monto": round(float(monto), 2),
        "concepto": concepto.strip(),
        "cliente": (cliente or "Anónimo").strip(),
        "estado": "completado",
        "creado_en": datetime.now(timezone.utc).isoformat(),
    }
    _payments.append(payment)
    return payment


def list_payments() -> list[dict[str, Any]]:
    return list(reversed(_payments))


def get_metrics() -> dict[str, Any]:
    montos = [p["monto"] for p in _payments]
    total = round(sum(montos), 2)
    count = len(montos)
    promedio = round(statistics.mean(montos), 2) if count else 0.0
    return {
        "total_pagos": count,
        "monto_total": total,
        "monto_promedio": promedio,
        "monto_maximo": round(max(montos), 2) if count else 0.0,
        "monto_minimo": round(min(montos), 2) if count else 0.0,
    }


def clear_payments() -> None:
    """Vacía el almacén; útil en pruebas."""
    _payments.clear()
