CUFE‑Scraper API – Consulta masiva de facturas electrónicas DIAN

Servicio Flask + Selenium que automatiza la búsqueda de CUFEs en el catálogo DIAN y persiste la información en MySQL. Dockerizado para facilitar la ejecución local o en servidores.

✨ ¿Qué hace este proyecto?

Recibe un array de CUFEs → consulta el Catálogo de Facturación Electrónica DIAN.

Extrae datos de emisor, receptor, eventos y el enlace a la representación gráfica.

Guarda la respuesta estructurada en una base MySQL (facturas_dian).

Expone un endpoint REST POST /api/v1/consult_invoice_information que devuelve el JSON obtenido.

⚙️ Tecnologías

Capa

Tecnología

Versión

API

Flask

2.x

Scraping

Selenium + ChromeDriver

4.x / Chrome estable

BD

MySQL

5.7

ORM

SQLAlchemy

2.x

Contenedores

Docker + Compose

26+

🚀 Puesta en marcha rápida

# 1. Clona el repositorio
$ git clone https://github.com/AlejandroVegaFullstackDev/cufe-scraper-api.git \
  && cd cufe-scraper-api

# 2. Arranca la pila
$ docker compose up -d --build

# 3. Prueba el endpoint (cURL)
$ curl -X POST http://localhost:5000/api/v1/consult_invoice_information \
  -H "Content-Type: application/json" \
  -d '{"cufes":["<CUFE_1>","<CUFE_2>"]}'

Nota: Chrome corre en modo incognito; activa el flag headless en scraper.py si lo deseas para entornos sin interfaz gráfica.

🔗 Endpoint principal

Método

Ruta

Descripción

POST

/api/v1/consult_invoice_information

Consulta un array de CUFEs, scrapea la DIAN y persiste resultados

Ejemplo de cuerpo

{
  "cufes": [
    "12345...",
    "67890..."
  ]
}

Respuesta (200)

{
  "12345...": {
    "sellerInformation": { "Document": "900123456", "Name": "ACME SAS" },
    "receiverInformation": { "Document": "1012345678", "Name": "Juan Pérez" },
    "events": [ { "eventNumber": "3", "eventName": "Recibo de bien" } ],
    "linkGraphicRepresentation": "https://catalogo-vpfe.dian.gov.co/.../document.pdf"
  },
  "67890...": { ... }
}

Errores → 400 { "error": "mensaje" }.

🗄️ Modelo de datos

Invoice(id, cufe, seller_document, seller_name, receiver_document, receiver_name, link_graphic_representation)
Event(id, eventNumber, eventName, invoice_id*)

Relación 1 :N → una factura tiene muchos eventos.

🧪 Pruebas manuales vs. automáticas

El scraping depende de la UI pública de la DIAN (recaptcha, tiempos). Recomendación:

Mantén ChromeDriver actualizado (webdriver-manager lo resuelve automáticamente).

Ajusta WebDriverWait y time.sleep según latencia.

Para pruebas unitarias, mockea scrape_info devolviendo JSON fijo.

☁️ Despliegue

Funciona en cualquier VM/host que soporte Docker. Para producción:

Activa headless Chrome.

Añade un scheduler (cron/k8s Job) si requieres consultas periódicas.

Protege el endpoint con token/API‑key si el servicio es público.

⚖️ Aviso legal

Este proyecto es de uso educativo/personal. Es responsabilidad del usuario respetar los términos del portal DIAN y la legislación colombiana en materia de scraping y protección de datos.

📄 Licencia

Publicado bajo MIT.

👨‍💻 Autor

Alejandro Vega – AlejandroVegaFullstackDev

