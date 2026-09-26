import json
def manage_invoice(data, title, order_id, phone_number, invoice_type):
    # if any(x is None or len(x) == 0 for x in [title, order_id, phone_number, invoice_type]):
    #     return data, "Incomplete parameter information, please enter again"
    invoice = {
        'invoice_title': title,
        'invoice_type': invoice_type,
        'order_id': order_id,
        'Phone number': phone_number,
    }
    if not data.get("invoices"):
        data["invoices"] = {}
    data["invoices"][order_id] = invoice
    return data, f"Invoice issued successfully. Invoice details: {json.dumps(invoice, ensure_ascii=False)}"