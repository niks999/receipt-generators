"""Internet Receipt Generator"""

import random
from datetime import datetime, timedelta

from utils import number_to_words

from .base import BaseGenerator


class InternetGenerator(BaseGenerator):
    """Generator for internet/ISP receipts"""

    name = "internet"
    display_name = "INTERNET RECEIPT GENERATOR"
    description = "Generate internet receipt"

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/internet"
        self.template_file = "templates/internet.html"
        self.merge_pdfs = False  # Single PDF, no merge needed

    def prepare_dates(self):
        """Prepare a single random date for internet receipt"""
        start_date = datetime.strptime(self.config['start_date'], "%Y-%m-%d")
        end_date = datetime.now()

        # Calculate random date between start and end
        total_seconds = int((end_date - start_date).total_seconds())
        random_seconds = random.randrange(total_seconds)
        random_date = start_date + timedelta(seconds=random_seconds)

        # Add random time during business hours
        random_date = random_date.replace(
            hour=random.randrange(9, 18),
            minute=random.randrange(60),
            second=random.randrange(60)
        )

        print(f"Generating receipt for {random_date}")
        return [random_date]

    def generate_single_pdf(self, date, browser):
        """Generate a single internet receipt PDF"""
        print(f"Generating PDF for {date}")

        # Generate random receipt and reference numbers
        receipt_number = f"R-{random.randrange(10000000, 99999999)}"
        reference_number = str(random.randrange(100000000, 999999999))

        # Get amount and convert to words
        amount = self.config.get('amount', 1000)
        amount_words = number_to_words(amount)

        replacements = {
            "{receipt_number}": receipt_number,
            "{account_number}": self.config.get('account_number', '0000000000'),
            "{reference_number}": reference_number,
            "{payment_date}": date.strftime("%d-%b-%Y %H:%M:%S"),
            "{customer_name}": self.config['customer_name'],
            "{customer_address}": self.config.get('customer_address', '# # City State - 000000 India'),
            "{amount_text}": f"₹{amount} ({amount_words} Rupees Only)",
        }

        # Render HTML
        html = self.render_html(self.template_file, replacements)

        # Create PDF
        output_file = f"{self.output_folder}/internet_receipt.pdf"
        self.create_pdf(html, output_file, browser)

        return output_file
