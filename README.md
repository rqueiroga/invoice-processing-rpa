# Invoice Processing RPA

[Português](README.pt-BR.md)

RPA project that simulates an Accounts Payable workflow across two fictional business systems.

All companies, credentials, records, systems and documents in this repository are fictional.

[Architecture](docs/architecture.svg)

# What the automation does

1. Reads pending invoice tasks from an Excel queue.
2. Logs into the **Supplier Portal** and searches for each invoice.
3. Downloads the first and last supporting documents.
4. Merges them into a single PDF package.
5. Opens the **Finance Portal** and locates the related purchase order.
6. Checks for duplicate registrations.
7. Maps the invoice type, uploads the PDF package and saves the registration.
8. Writes the result back to Excel after every processed row.

The demo includes successful cases and business exceptions such as a missing purchase order and an unmapped invoice type.

# Quick start

The project uses a single launcher. 

On Windows, open a terminal in the project folder and run:

```bash
py start.py
```

On the first run, `start.py` automatically:

- creates `.venv`;
- installs the Python dependencies;
- downloads the Playwright Chromium browser;
- resets the demo data;
- starts the two fictional systems;
- runs the RPA.

Later runs skip the installation and start the demo directly.

If the `py` launcher is unavailable, use:

```bash
python start.py
```

# Portuguese interface

```bash
py start.py --pt
```

The web interface also has an **EN / PT-BR** language switch.

# Demo speed

The default demo delay is `600 ms` between browser actions so the workflow can be followed visually.

```bash
py start.py --speed 300
py start.py --speed 900
```

Use `0` for near-production speed.

# Demo credentials

| System | User | Password |
| --- | --- | --- |
| Supplier Portal | `supplier.demo` | `demo123` |
| Finance Portal | `finance.demo` | `demo123` |

These credentials are intentionally public because the systems and data are local and fictional.

# Project structure

```text
invoice-processing-rpa/
├── start.py                # Single project launcher and automatic setup
├── main.py                 # RPA workflow
├── demo_server.py          # Supplier Portal + Finance Portal
├── run_demo.py             # Demo orchestration
├── reset_demo.py           # Restores the initial demo state
├── START_HERE.txt          # Minimal run instructions
├── data/
│   └── invoice_queue.xlsx  # Processing queue
├── sample_documents/       # Fictional PDF documents
├── docs/
│   └── architecture.svg
├── runtime/                # Generated local registrations/uploads
├── .gitignore
└── requirements.txt
```

# Business scenarios

- `INV-1001`: successful service invoice registration
- `INV-1002`: successful product invoice registration
- `INV-1003`: purchase order not found
- `INV-1004`: successful expense reimbursement registration
- `INV-1005`: unmapped invoice type requiring review

# Tech stack

- Python
- Playwright
- OpenPyXL
- pypdf
- HTML/CSS
- Python standard-library HTTP server

# Why this project is useful

This project simulates a real automation workflow involving Excel, two business systems, document downloads, PDF processing, business validations and automatic status updates.
