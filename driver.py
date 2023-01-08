import pdfkit

from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils import cleanup_output_dir, merge_pdf_files

# Variables
start_date = datetime(2022, 4, 1).date()
end_date = datetime(2023, 3, 1).date()
salary = 10000
driver_name = '<Driver Name>'
vehicle_number = '<Vehicle Number>'
employee_name = '<Name>'

# Internal
output_folder = 'output'
result_file = 'result.pdf'


def generate_pdf(salary, driver_name, employee_name, timestamp, vehicle):
    print(f'Generating PDF for {timestamp}')

    template_file = open('templates/driver.html', 'r')
    html = template_file.read()
    template_file.close()

    html = html.replace('{salary}', str(salary))
    html = html.replace('{driver_name}', driver_name)
    html = html.replace('{month}', timestamp.strftime('%B'))
    html = html.replace('{employee_name}', employee_name)
    html = html.replace('{receipt_date}', timestamp.strftime('%d %b %Y'))
    html = html.replace('{vehicle}', vehicle)

    output_file = f'{output_folder}/{timestamp}.pdf'
    pdfkit.from_string(html, output_file)

    return output_file


cleanup_output_dir(output_folder)

print(f'Processing from {start_date} to {end_date}')

dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += relativedelta(months=1)

files = []
for date in dates:
    file = generate_pdf(salary=salary,
                        driver_name=driver_name,
                        employee_name=employee_name,
                        timestamp=date,
                        vehicle=vehicle_number)
    files.append(file)

merge_pdf_files(files, f'{output_folder}/{result_file}')
