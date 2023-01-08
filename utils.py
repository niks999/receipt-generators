import os
from pypdf import PdfMerger


def cleanup_output_dir(path):
    print('========== Performing Cleanup ==========')

    if not os.path.exists(path):
        print(f'Creating folder: "{path}"')
        os.makedirs(path)

    print(f'Removing all files inside "{path}"')
    for f in os.listdir(path):
        os.remove(f'{path}/{f}')

    print('========== Cleanup complete ==========')


def merge_pdf_files(input_files, output_file):
    print('========== Starting Merge ==========')
    print(f'Input Files: {input_files}\nOutput File: {output_file}')

    merger = PdfMerger()
    for file in input_files:
        merger.append(file)
    merger.write(output_file)
    merger.close()

    print('========== Merge complete ==========')
