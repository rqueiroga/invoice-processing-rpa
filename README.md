# Invoice Processing RPA

[Português](README.pt-BR.md)

RPA project that simulates an Accounts Payable workflow between two fictional business systems.

All companies, credentials, records and documents used in this repository are fictional.

![Project flow](docs/architecture.svg)

# Flow

1. Reads pending invoices from an Excel queue.
2. Opens the **Supplier Portal** and searches for the invoice.
3. Downloads the first and last supporting documents.
4. Merges both files into one PDF.
5. Opens the **Finance Portal** and searches for the purchase order.
6. Checks whether the invoice was already registered.
7. Uploads the PDF and saves the registration.
8. Writes the result back to Excel.

The demo also includes cases such as a missing purchase order and an invoice type that requires manual review.

# Run

Open a terminal in the project folder and run:

```bash
py start.py
```

On the first run, the project creates its local Python environment and installs what it needs automatically. Later runs use the same command and start directly.

The demo systems open in English by default, while the terminal messages are in Portuguese.

Optional commands:

```bash
py start.py --speed 900
py start.py --pt
```

`--speed 900` makes the browser slower for recordings. `--pt` opens the demo systems in Portuguese.

# Project files

```text
invoice-processing-rpa/
├── start.py                 # starts the project and prepares the first run
├── main.py                  # RPA workflow
├── demo_server.py           # fictional Supplier and Finance portals
├── run_demo.py              # starts the portals and the automation
├── reset_demo.py            # restores the demo data
├── data/
│   └── invoice_queue.xlsx   # invoice queue
├── sample_documents/        # fictional PDF files
├── docs/
│   └── architecture.svg     # project flow diagram
└── runtime/                 # files created while the demo is running
```

# Demo cases

- `INV-1001`: service invoice processed successfully
- `INV-1002`: product invoice processed successfully
- `INV-1003`: purchase order not found
- `INV-1004`: expense reimbursement processed successfully
- `INV-1005`: invoice type without automatic mapping

# Technologies

- Python
- Playwright
- OpenPyXL
- pypdf

# Demo credentials

| System | User | Password |
| --- | --- | --- |
| Supplier Portal | `supplier.demo` | `demo123` |
| Finance Portal | `finance.demo` | `demo123` |
