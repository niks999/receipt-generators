"""Gadget Receipt Generator (Amazon)"""

import random

from utils import number_to_words, random_date_in_fy

from .base import BaseGenerator


class GadgetGenerator(BaseGenerator):
    """Generator for gadget/electronics receipts (Amazon - Appario Retail)"""

    name = "gadget"
    display_name = "GADGET RECEIPT GENERATOR"
    description = "Generate gadget receipt (Amazon)"

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/gadget"
        self.template_file = "templates/amazon.html"
        self.merge_pdfs = False  # Single PDF, no merge needed

    def prepare_dates(self):
        """Prepare a single random date in current financial year"""
        random_date = random_date_in_fy()
        print(f"Generating receipt for {random_date.strftime('%d.%m.%Y')}")
        return [random_date]

    def generate_single_pdf(self, date, browser):
        """Generate a single gadget receipt"""
        # Generate random order number (format: 4##-#######-#######)
        order_number = f"4{random.randrange(10, 99)}-{random.randrange(1000000, 9999999)}-{random.randrange(1000000, 9999999)}"

        # Generate random invoice numbers
        invoice_number = f"BOM4-{random.randrange(10000, 99999)}"
        invoice_details = f"MH-BOM4-{random.randrange(1000, 9999)}-{random.randrange(1000, 9999)}"

        # Format date as DD.MM.YYYY
        date_str = date.strftime("%d.%m.%Y")

        # Price calculation (12% tax for electronics)
        item_total = self.config['item_price']
        # Calculate net amount (price before tax)
        item_net = item_total / 1.12
        tax_amount_val = item_total - item_net

        item_unit_price = f"{item_net:,.2f}"
        item_net_amount = item_unit_price
        tax_rate = "12%"
        tax_type = "IGST"
        tax_amount = f"{tax_amount_val:,.2f}"
        item_total_price = f"{item_total:,.0f}"  # No decimals for total

        # Convert amount to words
        amount_in_words = number_to_words(int(item_total)) + " only"

        # Read and replace placeholders
        with open(self.template_file, 'r', encoding='utf-8') as file:
            html = file.read()

        replacements = {
            # Seller info
            '{seller_name}': 'Appario Retail Private Ltd',
            '{seller_address_line1}': '* WB-10/11, Renaissance logistics park,, Near vill.',
            '{seller_address_line2}': 'Padgha, Off. NH-3,, Taluka Bhiwandi,District Thane',
            '{seller_city_state_pin}': 'Thane, Maharashtra, 421302',
            '{seller_pan}': 'AALCA0171E',
            '{seller_gst}': '27AALCA0171E1ZZ',

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
        output_path = f"{self.output_folder}/gadget_receipt.pdf"
        self.create_pdf(html, output_path, browser)
