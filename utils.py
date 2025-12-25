import os

from pypdf import PdfReader, PdfWriter


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
