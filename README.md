# 🧾 CUFE Scraper DIAN — Consulta masiva de facturas electrónicas

Servicio **Flask + Selenium** que automatiza la búsqueda de **CUFEs** en el
[Catálogo de Facturación Electrónica de la DIAN](https://catalogo-vpfe.dian.gov.co/User/SearchDocument)
y persiste la información estructurada en **MySQL**. Empaquetado con Docker.

![CI](https://github.com/AlejandroVegaFullstackDev/Dian-Cufe/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0-black)
![Selenium](https://img.shields.io/badge/selenium-4-43B02A)
![MySQL](https://img.shields.io/badge/mysql-5.7-336791)

---

## ✨ Qué hace

1. Recibe un **array de CUFEs** por una API REST.
2. Por cada CUFE, automatiza la navegación en el catálogo DIAN con Selenium
   (incluye reintentos ante el reCAPTCHA).
3. Extrae **emisor**, **receptor**, **eventos** y el enlace a la representación
   gráfica del documento.
4. Persiste todo en MySQL (`invoices` + `events`) y devuelve el JSON resultante.

---

## 🔌 API

### `POST /api/v1/consult_invoice_information`

**Request**

```json
{
  "cufes": ["<cufe-1>", "<cufe-2>"]
}
```

**Response `200`**

```json
{
  "<cufe-1>": {
    "sellerInformation":   { "Document": "900123456", "Name": "ACME S.A.S" },
    "receiverInformation": { "Document": "800654321", "Name": "Cliente Ltda" },
    "events": [
      { "eventNumber": "030", "eventName": "Acuse de recibo" }
    ],
    "linkGraphicRepresentation": "https://catalogo-vpfe.dian.gov.co/..."
  }
}
```

Si falta el campo `cufes` se responde `400` con `{"error": "..."}`.

---

## 🧱 Estructura

```
app/
├── routes.py            # API Flask (endpoint REST)
├── scraper.py           # Automatización Selenium del catálogo DIAN
├── config_database.py   # Configuración SQLAlchemy + mapeo dict→ORM
└── models.py            # Modelos Invoice y Event
tests/
└── test_mapping.py      # Tests unitarios del mapeo (sin DB)
```

---

## 🚀 Cómo correrlo

### Docker (recomendado)

```bash
cp .env.example .env      # ajusta credenciales si quieres
docker-compose up --build
```

La API queda en `http://localhost:5000`. El contenedor ya trae Chrome y corre el
scraper en modo headless (`SCRAPER_HEADLESS=1`).

### Local

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # configura tu MySQL (DB_HOST=localhost, etc.)
python app/routes.py
```

> Requiere Google Chrome instalado; `webdriver-manager` descarga el driver
> automáticamente.

---

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=app
```

Los tests cubren el mapeo `dict → ORM` sin necesidad de base de datos ni
navegador (incluyen la regresión del bug que insertaba los eventos por
duplicado).

---

## 🔐 Configuración y secretos

Toda la configuración sensible se lee de variables de entorno (`.env`, ignorado
por git). Ver `.env.example`:

| Variable | Descripción | Default (dev) |
|----------|-------------|---------------|
| `DB_USER` / `DB_PASSWORD` | Credenciales MySQL | `root` / `root` |
| `DB_HOST` / `DB_PORT` | Host y puerto MySQL | `mysql` / `3306` |
| `DB_NAME` | Base de datos | `facturas_dian` |
| `SCRAPER_HEADLESS` | `1` para Chrome headless | `0` |

---

## 🛠️ Stack

`Python 3.11` · `Flask 3` · `Selenium 4` · `SQLAlchemy 2` · `MySQL 5.7` · `Docker`
