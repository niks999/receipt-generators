"""Base Receipt Generator"""

import os
from abc import ABC, abstractmethod
from pathlib import Path

from playwright.sync_api import sync_playwright

from utils import cleanup_output_dir, merge_pdf_files


class BaseGenerator(ABC):
    """Base class for receipt generators"""

    # Class-level metadata (to be overridden by subclasses)
    name = None  # CLI command name (e.g., 'fuel')
    display_name = None  # Display name for headers (e.g., 'FUEL RECEIPT GENERATOR')
    description = None  # Short description for help text

    def __init__(self, config: dict):
        """
        Initialize generator with configuration

        Args:
            config: Dictionary containing generator configuration
        """
        self.config = config
        self.output_folder = None
        self.result_file = "result.pdf"
        self.template_file = None
        self.merge_pdfs = True  # Whether to merge multiple PDFs

    @classmethod
    def print_header(cls):
        """Print formatted header for the generator"""
        if cls.display_name:
            print("=" * 60)
            print(cls.display_name)
            print("=" * 60)

    @abstractmethod
    def prepare_dates(self):
        """Prepare list of dates for receipt generation"""
        pass

    @abstractmethod
    def generate_single_pdf(self, date, browser):
        """Generate a single PDF for given date using existing browser instance"""
        pass

    def render_html(self, template_path: str, replacements: dict) -> str:
        """
        Read template and replace placeholders

        Args:
            template_path: Path to HTML template
            replacements: Dictionary of {placeholder: value} to replace

        Returns:
            Rendered HTML string
        """
        with open(template_path, 'r') as f:
            html = f.read()

        for placeholder, value in replacements.items():
            html = html.replace(placeholder, str(value))

        return html

    def create_pdf(self, html: str, output_path: str, browser):
        """
        Create PDF from HTML using Playwright

        Args:
            html: HTML content
            output_path: Path to save PDF
            browser: Playwright browser instance
        """
        base_url = f"file://{os.path.abspath('templates')}/"
        page = browser.new_page()
        page.goto(base_url)
        page.set_content(html, wait_until="networkidle")
        page.pdf(path=output_path, format='A4', print_background=True)
        page.close()

    def generate(self):
        """Main generation logic"""
        # Cleanup output directory
        cleanup_output_dir(self.output_folder)

        # Prepare dates
        dates = self.prepare_dates()
        print(f"Generating {len(dates)} receipts...")

        # Generate PDFs using single browser instance
        files = []
        with sync_playwright() as p:
            browser = p.chromium.launch()

            for date in dates:
                file_path = self.generate_single_pdf(date, browser)
                files.append(file_path)

            browser.close()

        # Merge all PDFs if needed
        if self.merge_pdfs and len(files) > 1:
            output_path = f"{self.output_folder}/{self.result_file}"
            merge_pdf_files(files, output_path)
            print(f"✓ Complete! Generated {len(files)} receipts")
            print(f"  Output: {output_path}")
        else:
            output_path = files[0] if files else None
            print(f"✓ Complete! Generated receipt")
            print(f"  Output: {output_path}")
