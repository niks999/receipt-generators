"""Fuel Receipt Generator"""

import math
import random
from datetime import datetime, timedelta

from .base import BaseGenerator


class FuelGenerator(BaseGenerator):
    """Generator for fuel receipts"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/fuel"
        self.template_file = "templates/fuel.html"

    def prepare_dates(self):
        """Prepare random dates for fuel receipts"""
        start_date = datetime.strptime(self.config['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(self.config['end_date'], "%Y-%m-%d")
        total_amount = self.config['total_amount']
        amount_per_bill = self.config['amount_per_bill']

        total_days = (end_date - start_date).days
        total_bills = math.ceil(total_amount / amount_per_bill)

        print(f"Processing from {start_date.date()} to {end_date.date()}")
        print(f"Total Days: {total_days} | Total Bills: {total_bills}")

        # Generate all possible dates
        dates = [start_date]
        current = start_date
        while current != end_date:
            current += timedelta(days=1)
            dates.append(current)

        # Randomly sample dates
        selected_dates = random.sample(dates, k=total_bills)
        selected_dates.sort()

        # Add random times
        return [
            date.replace(hour=random.randrange(10, 21), minute=random.randrange(60))
            for date in selected_dates
        ]

    def generate_single_pdf(self, date, browser):
        """Generate a single fuel receipt PDF"""
        print(f"Generating PDF for {date}")

        # Prepare replacements
        fuel_rate = str(self.config['fuel_rates'][date.month])
        amount = self.config['amount_per_bill']
        volume = round(amount / float(fuel_rate), 2)

        replacements = {
            "{pump_name}": self.config['pump_name'],
            "{area_name}": self.config['area_name'],
            "{receipt_number}": str(random.randrange(1000, 9999)),
            "{petrol_rate}": fuel_rate,
            "{amount}": str(amount),
            "{volume}": str(volume),
            "{vehicle_number}": self.config['vehicle_number'],
            "{customer_name}": self.config['customer_name'],
            "{date}": date.strftime("%d %b %Y"),
            "{time}": date.strftime("%H:%M"),
        }

        # Render HTML
        html = self.render_html(self.template_file, replacements)

        # Create PDF
        output_file = f"{self.output_folder}/{date}.pdf"
        self.create_pdf(html, output_file, browser)

        return output_file
