# Receipt Generators

## Prerequisites

- [WkHTMLtoPDF](https://wkhtmltopdf.org) - `brew install wkhtmltopdf`

## List of Generators

- Fuel receipt
- Driver Salary receipt

## Steps to Run

1. `python3 -m venv venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`
4. Update the variables in respective file - `fuel.py` / `driver.py`
5. `python fuel.py` / `python driver.py`