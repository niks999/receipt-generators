"""Book Receipt Generator (Amazon)"""

import random

from utils import number_to_words, random_date_in_fy

from .base import BaseGenerator


class BookGenerator(BaseGenerator):
    """Generator for book receipts (Amazon - India Book Distributors)"""

    name = "book"
    display_name = "BOOK RECEIPT GENERATOR"
    description = "Generate book receipt (Amazon)"

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/book"
        self.template_file = "templates/amazon.html"
        self.merge_pdfs = False  # Single PDF, no merge needed

    def prepare_dates(self):
        """Prepare a single random date in current financial year"""
        random_date = random_date_in_fy()
        print(f"Generating receipt for {random_date.strftime('%d.%m.%Y')}")
        return [random_date]

    def generate_single_pdf(self, date, browser):
        """Generate a single book receipt"""
        # Generate random order number (format: 5##-#######-#######)
        order_number = f"5{random.randrange(10, 99)}-{random.randrange(1000000, 9999999)}-{random.randrange(1000000, 9999999)}"

        # Generate random invoice numbers
        invoice_number = f"QSIS-{random.randrange(100000, 999999)}"
        invoice_details = f"KA-QSIS-{random.randrange(10000000, 99999999)}-{random.randrange(1000, 9999)}"

        # Format date as DD.MM.YYYY
        date_str = date.strftime("%d.%m.%Y")

        # Price calculation (0% tax for books)
        item_price = self.config['item_price']
        item_unit_price = f"{item_price:,.2f}"
        item_net_amount = item_unit_price
        tax_rate = "0%"
        tax_type = "IGST"
        tax_amount = "0.00"
        item_total_price = item_unit_price

        # Convert amount to words
        amount_in_words = number_to_words(item_price) + " only"

        # Read and replace placeholders
        with open(self.template_file, 'r', encoding='utf-8') as file:
            html = file.read()

        replacements = {
            # Seller info
            '{seller_name}': 'India Book Distributors (Bombay) Limited',
            '{seller_address_line1}': '* Budhigere cross,Plot no 128,Mandur village',
            '{seller_address_line2}': 'Bangalore, Karnataka, 560049',
            '{seller_city_state_pin}': '',  # Already included in line2
            '{seller_pan}': 'AAACI1048K',
            '{seller_gst}': 'NotApplicable',

            # Customer info
            '{customer_name}': self.config['customer_name'],
            '{customer_address_line1}': self.config['customer_address_line1'],
            '{customer_city_state_pin}': self.config['customer_city_state_pin'],
            '{customer_state_code}': self.config['customer_state_code'],
            '{customer_state}': self.config['customer_state'],

            # Order info
            '{order_number}': order_number,
            '{order_date}': date_str,
            '{invoice_number}': invoice_number,
            '{invoice_details}': invoice_details,
            '{invoice_date}': date_str,

            # Item info
            '{item_description}': self.config['item_name'],
            '{item_unit_price}': item_unit_price,
            '{item_net_amount}': item_net_amount,
            '{tax_rate}': tax_rate,
            '{tax_type}': tax_type,
            '{tax_amount}': tax_amount,
            '{item_total_price}': item_total_price,
            '{amount_in_words}': amount_in_words,
        }

        for placeholder, value in replacements.items():
            html = html.replace(placeholder, str(value))

        # Generate PDF
        output_path = f"{self.output_folder}/book_receipt.pdf"
        self.create_pdf(html, output_path, browser)
