"""Internet Receipt Generator"""

import random
from datetime import datetime, timedelta

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

    def number_to_words(self, num):
        """Convert number to words (Indian numbering system)"""
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

        def convert_hundreds(n):
            if n == 0:
                return ""
            elif n < 10:
                return ones[n]
            elif n < 20:
                return teens[n - 10]
            elif n < 100:
                return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")
            else:
                return ones[n // 100] + " Hundred" + (" " + convert_hundreds(n % 100) if n % 100 != 0 else "")

        if num == 0:
            return "Zero"

        crore = num // 10000000
        lakh = (num % 10000000) // 100000
        thousand = (num % 100000) // 1000
        hundred = num % 1000

        result = []
        if crore > 0:
            result.append(convert_hundreds(crore) + " Crore")
        if lakh > 0:
            result.append(convert_hundreds(lakh) + " Lakh")
        if thousand > 0:
            result.append(convert_hundreds(thousand) + " Thousand")
        if hundred > 0:
            result.append(convert_hundreds(hundred))

        return " ".join(result)

    def generate_single_pdf(self, date, browser):
        """Generate a single internet receipt PDF"""
        print(f"Generating PDF for {date}")

        # Generate random receipt and reference numbers
        receipt_number = f"R-{random.randrange(10000000, 99999999)}"
        reference_number = str(random.randrange(100000000, 999999999))

        # Get amount and convert to words
        amount = self.config.get('amount', 1000)
        amount_words = self.number_to_words(amount)

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
