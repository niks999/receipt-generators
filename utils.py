"""Utility functions for receipt generators"""

import os
import random
from datetime import datetime, timedelta

from pypdf import PdfReader, PdfWriter

# ============================================================================
# File and PDF Utilities
# ============================================================================

def cleanup_output_dir(path):
    """Clean up output directory by removing all files"""
    print('========== Performing Cleanup ==========')

    if not os.path.exists(path):
        print(f'Creating folder: "{path}"')
        os.makedirs(path)

    print(f'Removing all files inside "{path}"')
    for f in os.listdir(path):
        os.remove(f'{path}/{f}')

    print('========== Cleanup complete ==========')


def merge_pdf_files(input_files, output_file):
    """
    Merge PDF files with compression to reduce file size

    Args:
        input_files: List of PDF file paths to merge
        output_file: Output path for merged PDF
    """
    print('========== Starting Merge ==========')
    print(f'Merging {len(input_files)} PDFs...')

    writer = PdfWriter()

    # Add all pages with compression
    for file in input_files:
        reader = PdfReader(file)
        for page in reader.pages:
            # Compress content streams for smaller file size
            page.compress_content_streams()
            writer.add_page(page)

    # Write compressed PDF
    with open(output_file, 'wb') as f:
        writer.write(f)

    # Get file size for reporting
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f'Output File: {output_file} ({size_mb:.2f} MB)')
    print('========== Merge complete ==========')


# ============================================================================
# Date and Number Utilities
# ============================================================================

def number_to_words(num):
    """
    Convert number to words using Indian numbering system.

    Args:
        num: Integer number to convert

    Returns:
        String representation in words (e.g., "One Lakh Twenty Three Thousand")
    """
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

    def convert_hundreds(n):
        """Convert a number less than 1000 to words"""
        if n == 0:
            return ""
        elif n < 10:
            return ones[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")
        else:
            return ones[n // 100] + " Hundred" + (" And " + convert_hundreds(n % 100) if n % 100 != 0 else "")

    if num == 0:
        return "Zero"

    # Indian numbering: Crore, Lakh, Thousand, Hundred
    crore = num // 10000000
    num %= 10000000
    lakh = num // 100000
    num %= 100000
    thousand = num // 1000
    num %= 1000
    hundred = num

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


def get_financial_year_start():
    """
    Get the start date of current financial year (April 1).

    Returns:
        datetime object representing April 1 of current FY
    """
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Financial year starts April 1st
    # If we're before April, FY started last year
    if current_month < 4:
        return datetime(current_year - 1, 4, 1)
    else:
        return datetime(current_year, 4, 1)


def random_date_in_fy(count=1):
    """
    Generate random date(s) in current financial year (April 1 to today).

    Args:
        count: Number of random dates to generate (default: 1)

    Returns:
        Single datetime if count=1, otherwise list of datetime objects sorted chronologically
    """
    fy_start = get_financial_year_start()
    fy_end = datetime.now()

    total_days = (fy_end - fy_start).days

    dates = []
    for _ in range(count):
        random_days = random.randrange(total_days + 1)
        random_date = fy_start + timedelta(days=random_days)
        dates.append(random_date)

    dates.sort()
    return dates[0] if count == 1 else dates


def add_business_hours(date):
    """
    Add random business hours (9-18) to a datetime object.

    Args:
        date: datetime object

    Returns:
        datetime object with random hour/minute/second during business hours
    """
    return date.replace(
        hour=random.randrange(9, 18),
        minute=random.randrange(60),
        second=random.randrange(60)
    )
