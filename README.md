# Receipt Generators

Modern, clean receipt generator for fuel bills and driver salary receipts using Playwright.

## Features

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

## Project Structure

```
receipt-generators/
├── config.yaml              # Your configuration (gitignored)
├── config.example.yaml      # Template config
├── generate.py             # Main entry point
├── generators/             # Receipt generators package
│   ├── __init__.py
│   ├── base.py            # Base generator class
│   ├── fuel.py            # Fuel receipt generator
│   └── driver.py          # Driver salary generator
├── templates/              # HTML templates
│   ├── fuel.html
│   ├── driver.html
│   ├── fonts/             # Local fonts
│   └── images/            # Local images
├── output/                 # Generated PDFs
│   ├── fuel/
│   └── driver/
├── utils.py               # Utility functions
└── requirements.txt       # Dependencies
```

## Output

Generated PDFs are saved in:
- `output/fuel/result.pdf` - All fuel receipts merged
- `output/driver/result.pdf` - All driver salary receipts merged

Individual receipt PDFs are also available in their respective folders.

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
- `hp.png`
- `bank-side-logo.png`
- `revenue-stamp.jpg`

### Browser not found
Run `playwright install chromium` to download the browser.

## License

MIT
