"""Tests de la función de mapeo `dict_to_invoice`.

No necesitan base de datos: construyen objetos ORM en memoria y verifican el
mapeo. Cubren además la regresión del bug en el que los eventos se insertaban
dos veces (la factura ya trae sus eventos asociados por la cascada del ORM).
"""
from config_database import dict_to_invoice


SAMPLE = {
    "sellerInformation": {"Document": "900123456", "Name": "ACME S.A.S"},
    "receiverInformation": {"Document": "800654321", "Name": "Cliente Ltda"},
    "linkGraphicRepresentation": "https://dian.example/doc.pdf",
    "events": [
        {"eventNumber": "030", "eventName": "Acuse de recibo"},
        {"eventNumber": "032", "eventName": "Recepción de bien"},
    ],
}


def test_mapea_campos_de_la_factura():
    invoice = dict_to_invoice("CUFE-123", SAMPLE)

    assert invoice.cufe == "CUFE-123"
    assert invoice.seller_document == "900123456"
    assert invoice.seller_name == "ACME S.A.S"
    assert invoice.receiver_document == "800654321"
    assert invoice.receiver_name == "Cliente Ltda"
    assert invoice.link_graphic_representation == "https://dian.example/doc.pdf"


def test_asocia_cada_evento_una_sola_vez():
    invoice = dict_to_invoice("CUFE-123", SAMPLE)

    # Exactamente los eventos de entrada, sin duplicar.
    assert len(invoice.events) == 2
    assert {e.eventNumber for e in invoice.events} == {"030", "032"}
    assert all(e.invoice is invoice for e in invoice.events)


def test_factura_sin_eventos():
    data = {**SAMPLE, "events": []}

    invoice = dict_to_invoice("CUFE-999", data)

    assert invoice.events == []
