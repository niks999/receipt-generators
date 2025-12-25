"""Driver Salary Receipt Generator"""

from datetime import datetime

from dateutil.relativedelta import relativedelta

from .base import BaseGenerator


class DriverGenerator(BaseGenerator):
    """Generator for driver salary receipts"""

    name = "driver"
    display_name = "DRIVER SALARY RECEIPT GENERATOR"
    description = "Generate driver salary receipts"

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_folder = "output/driver"
        self.template_file = "templates/driver.html"

    def prepare_dates(self):
        """Prepare monthly dates for driver salary receipts"""
        start_date = datetime.strptime(self.config['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(self.config['end_date'], "%Y-%m-%d").date()

        print(f"Processing from {start_date} to {end_date}")

        # Generate monthly dates
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += relativedelta(months=1)

        return dates

    def generate_single_pdf(self, date, browser):
        """Generate a single driver salary receipt PDF"""
        print(f"Generating PDF for {date}")

        # Prepare replacements
        replacements = {
            "{salary}": str(self.config['salary']),
            "{driver_name}": self.config['driver_name'],
            "{month}": date.strftime("%B"),
            "{employee_name}": self.config['employee_name'],
            "{receipt_date}": date.strftime("%d %b %Y"),
            "{vehicle}": self.config['vehicle_number'],
        }

        # Render HTML
        html = self.render_html(self.template_file, replacements)

        # Create PDF
        output_file = f"{self.output_folder}/{date}.pdf"
        self.create_pdf(html, output_file, browser)

        return output_file
