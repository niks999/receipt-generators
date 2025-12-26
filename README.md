# Receipt Generators

Modern, scalable receipt generator system supporting multiple receipt types using Playwright.

## Features

✅ **Multiple Generator Types** - Fuel, Driver, Internet, Education, Book, Gadget receipts
✅ **Registry Pattern** - Easily extensible architecture for adding new generators
✅ **Shared Utilities** - DRY codebase with common date/number helpers
✅ **Zero External Dependencies** - All images local, no CDN links
✅ **Configuration File** - Edit `config.yaml` without git commits
✅ **Modern PDF Generation** - Uses Playwright (no deprecated wkhtmltopdf)
✅ **Perfect Font & Image Rendering** - Chrome rendering engine
✅ **Minimal Dependencies** - Only 4 packages required
✅ **Fast Generation** - Reuses browser instance for all PDFs

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Install Chromium browser (one-time only)
playwright install chromium
```

### 2. Configure

```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit config.yaml with your values
# (This file is gitignored - safe to update)
```

### 3. Generate Receipts

```bash
# Generate fuel receipts
python generate.py fuel

# Generate driver salary receipts
python generate.py driver

# Generate internet/ISP receipt
python generate.py internet

# Generate education receipts (Coursera-style)
python generate.py education

# Generate book receipt (Amazon)
python generate.py book

# Generate gadget receipt (Amazon)
python generate.py gadget
```

## Configuration

Edit `config.yaml` to customize:

### Fuel Receipts
- Date range (start_date, end_date)
- Total amount and amount per bill
- Pump name, area, vehicle number
- Customer name
- Monthly fuel rates

### Driver Salary Receipts
- Date range (monthly receipts)
- Salary amount
- Driver name, employee name
- Vehicle number

### Internet/ISP Receipts
- Start date for randomization
- Customer name and account number
- Amount
- Customer address

### Education Receipts (Coursera-style)
- Customer name
- Products list with name and price
- Generates 1 page per product with dynamic date randomization (Financial Year)

### Book Receipts (Amazon - India Book Distributors)
- Customer details (name, address, state)
- Book name with ISBN
- Price (0% tax for books)
- Random order/invoice numbers with FY date randomization

### Gadget Receipts (Amazon - Appario Retail)
- Customer details (name, address, state)
- Item name with HSN code
- Price (includes 12% IGST)
- Random order/invoice numbers with FY date randomization

## Project Structure

```
receipt-generators/
├── config.yaml              # Your configuration (gitignored)
├── config.example.yaml      # Template config
├── generate.py              # Main entry point with registry pattern
├── generators/              # Receipt generators package
│   ├── __init__.py         # Generator registry
│   ├── base.py             # Base generator class with metadata
│   ├── fuel.py             # Fuel receipt generator
│   ├── driver.py           # Driver salary generator
│   ├── internet.py         # Internet/ISP receipt generator
│   ├── education.py        # Education receipt generator (dynamic)
│   ├── book.py             # Book receipt generator (Amazon)
│   └── gadget.py           # Gadget receipt generator (Amazon)
├── templates/               # HTML templates
│   ├── fuel.html
│   ├── driver.html
│   ├── internet.html
│   ├── education.html
│   ├── amazon.html          # Shared template for book/gadget
│   ├── fonts/               # Local fonts
│   └── images/              # Local images
│       ├── hp.png
│       ├── bank-side-logo.png
│       ├── revenue-stamp.jpg
│       ├── hathway.png
│       ├── amazon_logo.png
│       └── amazon_signature.png
├── output/                  # Generated PDFs
│   ├── fuel/
│   ├── driver/
│   ├── internet/
│   ├── education/
│   ├── book/
│   └── gadget/
├── utils.py                 # Shared utility functions
│   └── number_to_words()   # Indian numbering system
│   └── random_date_in_fy() # Financial year date generation
│   └── add_business_hours()
└── requirements.txt         # Dependencies
```

## Output

Generated PDFs are saved in:
- `output/fuel/result.pdf` - All fuel receipts merged
- `output/driver/result.pdf` - All driver salary receipts merged
- `output/internet/internet_receipt.pdf` - Single internet receipt
- `output/education/result.pdf` - All education receipts merged
- `output/book/book_receipt.pdf` - Single book receipt
- `output/gadget/gadget_receipt.pdf` - Single gadget receipt

Individual receipt PDFs are also available in their respective folders.

## Architecture

### Registry Pattern
New generators are automatically discovered via the `GENERATOR_REGISTRY`. To add a new generator:

1. Create a new class inheriting from `BaseGenerator`
2. Set class-level metadata (`name`, `display_name`, `description`)
3. Implement `prepare_dates()` and `generate_single_pdf()` methods
4. Add to `generators/__init__.py` imports and registry

No changes needed to `generate.py` - the registry handles discovery automatically.

### Shared Utilities
Common functionality extracted to `utils.py`:
- **number_to_words()** - Convert numbers to Indian numbering words (Crore, Lakh, Thousand)
- **get_financial_year_start()** - Calculate current FY start date (April 1)
- **random_date_in_fy()** - Generate random date(s) in current financial year
- **add_business_hours()** - Add random business hours (9-18) to dates

## Dependencies

- **playwright** - Modern browser automation for PDF generation
- **pypdf** - PDF merging
- **pyyaml** - Configuration file parsing
- **python-dateutil** - Date manipulation utilities

## Troubleshooting

### Fonts not rendering
If custom fonts don't load, Playwright automatically falls back to system fonts. The Google Fonts CDN link is included in templates for optimal rendering.

### Images not showing
Ensure all image files are present in `templates/images/`:
- `hp.png` (Fuel)
- `bank-side-logo.png` (Driver)
- `revenue-stamp.jpg` (Driver)
- `hathway.png` (Internet)
- `amazon_logo.png` (Book/Gadget)
- `amazon_signature.png` (Book/Gadget)

### Browser not found
Run `playwright install chromium` to download the browser.

## License

MIT
