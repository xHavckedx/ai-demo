# ai-demo

Demo con una **plataforma de pagos mock** (Historia CBX-5): API Flask, UI web y métricas en memoria.

## Requisitos

- Python 3.11+
- Dependencias: `pip install -r requirements.txt`

## Uso

```bash
python app.py
```

Abre `http://127.0.0.1:5000/` para pagar (simulado), ver historial y métricas.

### API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/api/pagos` | Lista de pagos |
| POST | `/api/pagos` | Crear pago mock (`monto`, `descripcion`) |
| GET | `/api/metricas` | Totales, volumen y tasa de éxito |

## Tests

```bash
pytest
```
