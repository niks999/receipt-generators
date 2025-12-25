"""Education Receipt Generator"""

import random
from datetime import datetime, timedelta

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
        # Financial year starts April 1st
        current_year = datetime.now().year
        current_month = datetime.now().month

        # If we're before April, FY started last year
        if current_month < 4:
            fy_start = datetime(current_year - 1, 4, 1)
        else:
            fy_start = datetime(current_year, 4, 1)

        fy_end = datetime.now()

        total_days = (fy_end - fy_start).days
        print(f"Financial Year: {fy_start.date()} to {fy_end.date()} ({total_days} days)")

        # Validate products
        if len(self.products) < 1:
            raise ValueError("At least 1 product required in config")

        # Generate one random date per product
        num_receipts = len(self.products)
        dates = []
        for _ in range(num_receipts):
            random_days = random.randrange(total_days + 1)
            random_date = fy_start + timedelta(days=random_days)
            # Add random time during business hours
            random_date = random_date.replace(
                hour=random.randrange(9, 18),
                minute=random.randrange(60),
                second=random.randrange(60)
            )
            dates.append(random_date)

        dates.sort()
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
