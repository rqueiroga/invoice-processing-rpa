from __future__ import annotations

import html
import json
import os
from email.parser import BytesParser
from email.policy import default
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

ROOT = Path(__file__).parent
DOCS = ROOT / "sample_documents"
RUNTIME = ROOT / "runtime"
STATE = RUNTIME / "state.json"
UPLOADS = RUNTIME / "uploads"
HOST = os.getenv("DEMO_HOST", "127.0.0.1")
PORT = int(os.getenv("DEMO_PORT", "8000"))

SUPPLIER_USER = os.getenv("SUPPLIER_USER", "supplier.demo")
SUPPLIER_PASSWORD = os.getenv("SUPPLIER_PASSWORD", "demo123")
FINANCE_USER = os.getenv("FINANCE_USER", "finance.demo")
FINANCE_PASSWORD = os.getenv("FINANCE_PASSWORD", "demo123")

INVOICES = {
    "INV-1001": {
        "vendor": "BluePeak Facilities",
        "po": "PO-45001",
        "amount": "$ 4,280.00",
        "attachments": ["invoice.pdf", "service-report.pdf", "approval.pdf"],
    },
    "INV-1002": {
        "vendor": "Oakline Supplies",
        "po": "PO-45002",
        "amount": "$ 1,945.50",
        "attachments": ["invoice.pdf", "delivery-note.pdf", "approval.pdf"],
    },
    "INV-1003": {
        "vendor": "Atlas Maintenance",
        "po": "PO-99999",
        "amount": "$ 3,100.00",
        "attachments": ["invoice.pdf", "approval.pdf"],
    },
    "INV-1004": {
        "vendor": "Horizon Travel Services",
        "po": "PO-45003",
        "amount": "$ 860.00",
        "attachments": ["receipt.pdf", "manager-note.pdf", "approval.pdf"],
    },
    "INV-1005": {
        "vendor": "Northstar Events",
        "po": "PO-45004",
        "amount": "$ 2,350.00",
        "attachments": ["invoice.pdf", "approval.pdf"],
    },
}

ORDERS = {
    "PO-45001": "Facilities",
    "PO-45002": "Office Supplies",
    "PO-45003": "Travel",
    "PO-45004": "Events",
}

TEXT = {
    "en": {
        "demo": "Invoice Processing Demo",
        "subtitle": "Two fictional business systems built for an end-to-end RPA portfolio project.",
        "supplier": "Supplier Portal",
        "supplier_desc": "Search invoices and download supporting documents.",
        "finance": "Finance Portal",
        "finance_desc": "Locate purchase orders and register invoice packages.",
        "open_system": "Open system",
        "open_item": "Open",
        "status_open": "Open",
        "user": "User",
        "password": "Password",
        "sign_in": "Sign in",
        "invalid": "Invalid credentials.",
        "invoices": "Invoices",
        "invoice_hint": "Search a supplier invoice before collecting its documents.",
        "invoice_placeholder": "INV-1001",
        "search": "Search",
        "enter_invoice": "Enter an invoice ID to begin.",
        "not_found_invoice": "No invoice found.",
        "invoice": "Invoice",
        "vendor": "Vendor",
        "purchase_order": "Purchase Order",
        "amount": "Amount",
        "attachments": "Attachments",
        "file": "File",
        "download": "Download",
        "back": "Back",
        "orders": "Purchase Orders",
        "order_hint": "Locate the PO before registering an invoice package.",
        "enter_order": "Enter a purchase order to begin.",
        "not_found_order": "No purchase order found.",
        "department": "Department",
        "status": "Status",
        "workflow": "Workflow",
        "invoice_registration": "Invoice registration",
        "invoice_packages": "Invoice Packages",
        "registered": "Registered",
        "none_registered": "No invoice packages registered yet.",
        "register_invoice": "Register invoice",
        "register_package": "Register Invoice Package",
        "invoice_id": "Invoice ID",
        "document_type": "Document type",
        "processing_date": "Processing date",
        "pdf_package": "PDF package",
        "select": "Select...",
        "services": "Services",
        "goods": "Goods",
        "expenses": "Expenses",
        "save": "Save registration",
        "success": "Invoice package registered successfully.",
    },
    "pt": {
        "demo": "Demonstração de Processamento de Notas",
        "subtitle": "Dois sistemas empresariais fictícios criados para um projeto de RPA de ponta a ponta.",
        "supplier": "Portal de Fornecedores",
        "supplier_desc": "Consulte notas e baixe documentos de apoio.",
        "finance": "Portal Financeiro",
        "finance_desc": "Localize pedidos de compra e registre pacotes de notas.",
        "open_system": "Abrir sistema",
        "open_item": "Abrir",
        "status_open": "Aberto",
        "user": "Usuário",
        "password": "Senha",
        "sign_in": "Entrar",
        "invalid": "Credenciais inválidas.",
        "invoices": "Notas",
        "invoice_hint": "Consulte uma nota de fornecedor antes de coletar os documentos.",
        "invoice_placeholder": "INV-1001",
        "search": "Pesquisar",
        "enter_invoice": "Informe o ID de uma nota para começar.",
        "not_found_invoice": "Nenhuma nota encontrada.",
        "invoice": "Nota",
        "vendor": "Fornecedor",
        "purchase_order": "Pedido de Compra",
        "amount": "Valor",
        "attachments": "Anexos",
        "file": "Arquivo",
        "download": "Baixar",
        "back": "Voltar",
        "orders": "Pedidos de Compra",
        "order_hint": "Localize o pedido antes de registrar o pacote da nota.",
        "enter_order": "Informe um pedido de compra para começar.",
        "not_found_order": "Nenhum pedido de compra encontrado.",
        "department": "Departamento",
        "status": "Status",
        "workflow": "Fluxo",
        "invoice_registration": "Registro de nota",
        "invoice_packages": "Pacotes de Notas",
        "registered": "Registrado",
        "none_registered": "Nenhum pacote de nota registrado ainda.",
        "register_invoice": "Registrar nota",
        "register_package": "Registrar Pacote da Nota",
        "invoice_id": "ID da Nota",
        "document_type": "Tipo de documento",
        "processing_date": "Data de processamento",
        "pdf_package": "Pacote PDF",
        "select": "Selecione...",
        "services": "Serviços",
        "goods": "Produtos",
        "expenses": "Despesas",
        "save": "Salvar cadastro",
        "success": "Pacote da nota registrado com sucesso.",
    },
}

CSS = """
:root{font-family:Inter,Segoe UI,Arial,sans-serif;color:#172033;background:#f4f7fb}
*{box-sizing:border-box}body{margin:0}.top{background:#111827;color:white;padding:18px 28px;display:flex;justify-content:space-between;align-items:center}.top a{color:#dbeafe;text-decoration:none}.brand{font-weight:750;font-size:18px}.lang{display:flex;gap:10px;font-size:13px}.wrap{max-width:980px;margin:34px auto;padding:0 20px}.card{background:white;border:1px solid #dce3ee;border-radius:14px;padding:24px;margin-bottom:18px;box-shadow:0 7px 24px rgba(15,23,42,.05)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}.system{min-height:180px}.muted{color:#687386}.row,.links{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.links{margin-bottom:16px}input,select{width:100%;padding:11px 12px;border:1px solid #cbd5e1;border-radius:8px;margin:6px 0 14px;background:white}label{display:block;font-weight:650}button,.btn{border:0;background:#2563eb;color:white;padding:10px 15px;border-radius:8px;text-decoration:none;cursor:pointer;font-weight:650}.alt{background:#475569}.light{background:#e8eef8;color:#1e3a8a}table{width:100%;border-collapse:collapse;margin-top:12px}th,td{text-align:left;border-bottom:1px solid #e5e7eb;padding:12px 10px}th{color:#475569;font-size:13px}.pill{background:#dcfce7;color:#166534;padding:4px 8px;border-radius:999px;font-size:12px}.error{background:#fee2e2;color:#991b1b;padding:10px;border-radius:8px}.success{background:#dcfce7;color:#166534;padding:12px;border-radius:8px;margin-bottom:18px}.stat{background:#f8fafc;border-radius:10px;padding:14px;color:#64748b}.stat b{display:block;color:#172033;margin-top:5px;font-size:17px}h1,h2{margin-top:0}
"""


def load_state() -> dict:
    if not STATE.exists():
        return {"registrations": {}}
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def language_from_cookie(header: str | None) -> str:
    jar = cookies.SimpleCookie()
    if header:
        jar.load(header)
    return "pt" if jar.get("lang") and jar["lang"].value == "pt" else "en"


def layout(title: str, body: str, lang: str) -> str:
    current = quote(title)
    switch = (
        "<span>EN</span> · <a href='/language/pt'>PT-BR</a>"
        if lang == "en"
        else "<a href='/language/en'>EN</a> · <span>PT-BR</span>"
    )
    return f"""<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><style>{CSS}</style></head><body><header class='top'><a class='brand' href='/'>{TEXT[lang]['demo']}</a><div class='lang'>{switch}</div></header><main class='wrap'>{body}</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args) -> None:
        pass

    @property
    def lang(self) -> str:
        return language_from_cookie(self.headers.get("Cookie"))

    @property
    def t(self) -> dict:
        return TEXT[self.lang]

    def send_html(self, content: str, status: int = 200) -> None:
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, target: str, cookie: str | None = None) -> None:
        self.send_response(302)
        self.send_header("Location", target)
        if cookie:
            self.send_header("Set-Cookie", f"{cookie}; Path=/; SameSite=Lax")
        self.end_headers()

    def cookie(self, name: str) -> str:
        jar = cookies.SimpleCookie()
        jar.load(self.headers.get("Cookie", ""))
        return jar[name].value if name in jar else ""

    def supplier_guard(self) -> bool:
        if self.cookie("supplier_auth") == "1":
            return True
        self.redirect("/supplier/login")
        return False

    def finance_guard(self) -> bool:
        if self.cookie("finance_auth") == "1":
            return True
        self.redirect("/finance/login")
        return False

    def form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        return {key: values[0] for key, values in parse_qs(raw).items()}

    def multipart(self) -> tuple[dict[str, str], dict[str, tuple[str, bytes]]]:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        message = BytesParser(policy=default).parsebytes(
            b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + body
        )
        fields: dict[str, str] = {}
        files: dict[str, tuple[str, bytes]] = {}
        for part in message.iter_parts():
            name = part.get_param("name", header="content-disposition")
            filename = part.get_filename()
            payload = part.get_payload(decode=True) or b""
            if filename:
                files[name] = (filename, payload)
            else:
                fields[name] = payload.decode(part.get_content_charset() or "utf-8")
        return fields, files

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path
        query = parse_qs(parsed.query)
        t = self.t

        if route.startswith("/language/"):
            lang = "pt" if route.endswith("/pt") else "en"
            target = self.headers.get("Referer") or "/"
            return self.redirect(target, f"lang={lang}")

        if route == "/":
            body = f"""<section class='card'><h1>{t['demo']}</h1><p class='muted'>{t['subtitle']}</p></section><div class='grid'><section class='card system'><h2>{t['supplier']}</h2><p class='muted'>{t['supplier_desc']}</p><a class='btn' href='/supplier/login'>{t['open_system']}</a></section><section class='card system'><h2>{t['finance']}</h2><p class='muted'>{t['finance_desc']}</p><a class='btn' href='/finance/login'>{t['open_system']}</a></section></div>"""
            return self.send_html(layout(t["demo"], body, self.lang))

        if route == "/supplier/login":
            error = f"<p class='error'>{t['invalid']}</p>" if query.get("error") else ""
            body = f"""<section class='card'><h1>{t['supplier']}</h1>{error}<form method='post'><label>{t['user']}<input data-testid='user' name='user' required></label><label>{t['password']}<input data-testid='password' type='password' name='password' required></label><button data-testid='sign-in'>{t['sign_in']}</button></form></section>"""
            return self.send_html(layout(t["supplier"], body, self.lang))

        if route == "/supplier/invoices":
            if not self.supplier_guard():
                return
            invoice_id = query.get("invoice", [""])[0].strip().upper()
            result = ""
            if invoice_id:
                invoice = INVOICES.get(invoice_id)
                if invoice:
                    result = f"""<table><thead><tr><th>{t['invoice']}</th><th>{t['vendor']}</th><th>{t['purchase_order']}</th><th></th></tr></thead><tbody><tr><td>{invoice_id}</td><td>{invoice['vendor']}</td><td>{invoice['po']}</td><td><a class='btn light' data-testid='invoice-link' href='/supplier/invoice/{invoice_id}'>{t['open_item']}</a></td></tr></tbody></table>"""
                else:
                    result = f"<p class='error'>{t['not_found_invoice']}</p>"
            body = f"""<section class='card'><h1>{t['invoices']}</h1><p class='muted'>{t['invoice_hint']}</p><form class='row'><input name='invoice' value='{html.escape(invoice_id)}' placeholder='{t['invoice_placeholder']}' required><button>{t['search']}</button></form></section><section class='card'>{result or f'<p class="muted">{t["enter_invoice"]}</p>'}</section>"""
            return self.send_html(layout(t["invoices"], body, self.lang))

        if route.startswith("/supplier/invoice/"):
            if not self.supplier_guard():
                return
            invoice_id = route.rsplit("/", 1)[-1]
            invoice = INVOICES.get(invoice_id)
            if not invoice:
                return self.send_error(404)
            rows = "".join(
                f"<tr data-testid='attachment-row'><td>{html.escape(name)}</td><td><a class='btn light' data-testid='download' href='/supplier/download/{invoice_id}/{quote(name)}'>{t['download']}</a></td></tr>"
                for name in invoice["attachments"]
            )
            body = f"""<div class='links'><a class='btn alt' href='/supplier/invoices'>{t['back']}</a></div><section class='card'><h1>{invoice_id}</h1><div class='grid'><div class='stat'>{t['vendor']}<b>{invoice['vendor']}</b></div><div class='stat'>{t['purchase_order']}<b>{invoice['po']}</b></div><div class='stat'>{t['amount']}<b>{invoice['amount']}</b></div></div></section><section class='card'><h2>{t['attachments']}</h2><table><thead><tr><th>{t['file']}</th><th></th></tr></thead><tbody>{rows}</tbody></table></section>"""
            return self.send_html(layout(invoice_id, body, self.lang))

        if route.startswith("/supplier/download/"):
            if not self.supplier_guard():
                return
            _, _, _, invoice_id, encoded_name = route.split("/", 4)
            name = unquote(encoded_name)
            file = DOCS / invoice_id / name
            if not file.is_file():
                return self.send_error(404)
            data = file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="{name}"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)

        if route == "/finance/login":
            error = f"<p class='error'>{t['invalid']}</p>" if query.get("error") else ""
            body = f"""<section class='card'><h1>{t['finance']}</h1>{error}<form method='post'><label>{t['user']}<input data-testid='user' name='user' required></label><label>{t['password']}<input data-testid='password' type='password' name='password' required></label><button data-testid='sign-in'>{t['sign_in']}</button></form></section>"""
            return self.send_html(layout(t["finance"], body, self.lang))

        if route == "/finance/orders":
            if not self.finance_guard():
                return
            po = query.get("po", [""])[0].strip().upper()
            result = ""
            if po:
                department = ORDERS.get(po)
                if department:
                    result = f"""<table><thead><tr><th>PO</th><th>{t['department']}</th><th>{t['status']}</th><th></th></tr></thead><tbody><tr><td>{po}</td><td>{department}</td><td><span class='pill'>{t['status_open']}</span></td><td><a class='btn light' data-testid='order-link' href='/finance/order/{po}'>{t['open_item']}</a></td></tr></tbody></table>"""
                else:
                    result = f"<p class='error'>{t['not_found_order']}</p>"
            body = f"""<section class='card'><h1>{t['orders']}</h1><p class='muted'>{t['order_hint']}</p><form class='row'><input name='po' value='{html.escape(po)}' placeholder='PO-45001' required><button>{t['search']}</button></form></section><section class='card'>{result or f'<p class="muted">{t["enter_order"]}</p>'}</section>"""
            return self.send_html(layout(t["orders"], body, self.lang))

        if route.startswith("/finance/order/") and route.endswith("/register"):
            if not self.finance_guard():
                return
            po = route.split("/")[3]
            if po not in ORDERS:
                return self.send_error(404)
            body = f"""<div class='links'><a class='btn alt' href='/finance/order/{po}'>{t['back']}</a></div><section class='card'><h1>{t['register_package']}</h1><p class='muted'>{po} · {ORDERS[po]}</p><form method='post' enctype='multipart/form-data'><label>{t['invoice_id']}<input data-testid='invoice-id' name='invoice_id' required></label><label>{t['document_type']}<select data-testid='document-type' name='doc_type' required><option value=''>{t['select']}</option><option value='Services'>{t['services']}</option><option value='Goods'>{t['goods']}</option><option value='Expenses'>{t['expenses']}</option></select></label><label>{t['processing_date']}<input data-testid='processing-date' type='date' name='processing_date' required></label><label>{t['pdf_package']}<input data-testid='pdf-package' type='file' name='document' accept='application/pdf' required></label><button data-testid='save-registration'>{t['save']}</button></form></section>"""
            return self.send_html(layout(t["register_package"], body, self.lang))

        if route.startswith("/finance/order/"):
            if not self.finance_guard():
                return
            po = route.rsplit("/", 1)[-1]
            if po not in ORDERS:
                return self.send_error(404)
            registrations = load_state()["registrations"].get(po, [])
            rows = "".join(
                f"<tr data-invoice='{html.escape(r['invoice_id'])}'><td>{html.escape(r['invoice_id'])}</td><td>{html.escape(r['doc_type'])}</td><td>{html.escape(r['processing_date'])}</td><td><span class='pill'>{t['registered']}</span></td></tr>"
                for r in registrations
            ) or f"<tr><td colspan='4' class='muted'>{t['none_registered']}</td></tr>"
            success = f"<div class='success' data-testid='success-message'>{t['success']}</div>" if query.get("saved") else ""
            body = f"""<div class='links'><a class='btn alt' href='/finance/orders'>{t['back']}</a></div>{success}<section class='card'><h1>{po}</h1><div class='grid'><div class='stat'>{t['department']}<b>{ORDERS[po]}</b></div><div class='stat'>{t['status']}<b>{t['status_open']}</b></div><div class='stat'>{t['workflow']}<b>{t['invoice_registration']}</b></div></div></section><section class='card'><div class='links' style='justify-content:space-between'><h2>{t['invoice_packages']}</h2><a class='btn' data-testid='register-link' href='/finance/order/{po}/register'>{t['register_invoice']}</a></div><table><thead><tr><th>{t['invoice']}</th><th>{t['document_type']}</th><th>{t['processing_date']}</th><th>{t['status']}</th></tr></thead><tbody>{rows}</tbody></table></section>"""
            return self.send_html(layout(po, body, self.lang))

        self.send_error(404)

    def do_POST(self) -> None:
        route = urlparse(self.path).path

        if route == "/supplier/login":
            data = self.form()
            if data.get("user") == SUPPLIER_USER and data.get("password") == SUPPLIER_PASSWORD:
                return self.redirect("/supplier/invoices", "supplier_auth=1")
            return self.redirect("/supplier/login?error=1")

        if route == "/finance/login":
            data = self.form()
            if data.get("user") == FINANCE_USER and data.get("password") == FINANCE_PASSWORD:
                return self.redirect("/finance/orders", "finance_auth=1")
            return self.redirect("/finance/login?error=1")

        if route.startswith("/finance/order/") and route.endswith("/register"):
            if not self.finance_guard():
                return
            po = route.split("/")[3]
            fields, files = self.multipart()
            invoice_id = fields.get("invoice_id", "").strip().upper()
            document = files.get("document")
            if po not in ORDERS or not invoice_id or not document:
                return self.send_error(400)

            state = load_state()
            current = state["registrations"].setdefault(po, [])
            if any(item["invoice_id"] == invoice_id for item in current):
                return self.redirect(f"/finance/order/{po}")

            UPLOADS.mkdir(parents=True, exist_ok=True)
            filename, content = document
            saved_name = f"{invoice_id}__{Path(filename).name}"
            (UPLOADS / saved_name).write_bytes(content)
            current.append(
                {
                    "invoice_id": invoice_id,
                    "doc_type": fields.get("doc_type", ""),
                    "processing_date": fields.get("processing_date", ""),
                    "file": saved_name,
                }
            )
            save_state(state)
            return self.redirect(f"/finance/order/{po}?saved=1")

        self.send_error(404)


if __name__ == "__main__":
    print(f"Demo systems running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
