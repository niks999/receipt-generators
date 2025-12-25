"""Education Receipt Generator"""

import random
from datetime import datetime

from utils import (add_business_hours, get_financial_year_start,
                   random_date_in_fy)

from .base import BaseGenerator


class EducationGenerator(BaseGenerator):
    """Generator for education/course receipts (Coursera)"""

    name = "education"
    display_name = "EDUCATION RECEIPT GENERATOR"
    description = "Generate education receipts (dynamic multi-page PDF)"

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/education"
        self.template_file = "templates/education.html"
        self.merge_pdfs = True  # Merge all PDFs into one
        self.products = config.get('products', [])  # All products from config
        self.current_receipt_index = 0  # Track current receipt being generated

    def prepare_dates(self):
        """Prepare random dates in current financial year (one per product)"""
        fy_start = get_financial_year_start()
        fy_end = datetime.now()

        total_days = (fy_end - fy_start).days
        print(f"Financial Year: {fy_start.date()} to {fy_end.date()} ({total_days} days)")

        # Validate products
        if len(self.products) < 1:
            raise ValueError("At least 1 product required in config")

        # Generate random dates with business hours
        num_receipts = len(self.products)
        dates = random_date_in_fy(count=num_receipts)

        # Add business hours to each date
        dates = [add_business_hours(date) for date in dates]

        return dates

    def generate_single_pdf(self, date, browser):
        """Generate a single education receipt PDF"""
        # Get the product for this receipt using the index
        product = self.products[self.current_receipt_index]

        print(f"Generating PDF {self.current_receipt_index + 1}/{len(self.products)}: {product['name']} - INR {product['price']}")

        # Generate random order number (7 digits)
        order_number = random.randrange(1000000, 9999999)

        # Prepare replacements
        replacements = {
            "{customer_name}": self.config['customer_name'],
            "{date}": date.strftime("%d-%m-%Y"),
            "{order_number}": str(order_number),
            "{product_name}": product['name'],
            "{price}": f"{product['price']:.2f}",
        }

        # Render HTML
        html = self.render_html(self.template_file, replacements)

        # Create PDF
        output_file = f"{self.output_folder}/{date.strftime('%Y%m%d_%H%M%S')}.pdf"
        self.create_pdf(html, output_file, browser)

        # Increment index for next receipt
        self.current_receipt_index += 1

        return output_file
