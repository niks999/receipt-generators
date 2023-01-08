import random
import math
import pdfkit

from datetime import datetime, timedelta

from utils import cleanup_output_dir, merge_pdf_files

# Variables
start_date = datetime(2022, 4, 1)
end_date = datetime(2023, 1, 1)
total_amount = 10000
amount_per_bill = 1000
pump_name = '<Pump Name>'
area_name = '<Area Name>'
vehicle_number = '<Vehicle Number>'
customer_name = '<Name>'
fuel_rates = {
    1: '109.96',
    2: '109.96',
    3: '109.96',
    4: '116.70',
    5: '120.51',
    6: '111.33',
    7: '111.33',
    8: '106.29',
    9: '106.29',
    10: '106.29',
    11: '106.29',
    12: '106.29'
}

# Internal
output_folder = 'output'
result_file = 'result.pdf'


def generate_pdf(pump, area, receipt_number, petrol_rate, amount, vehicle, customer, timestamp):
    print(f'Generating PDF for {timestamp}')

    template_file = open('templates/fuel.html', 'r')
    html = template_file.read()
    template_file.close()

    html = html.replace('{pump_name}', pump)
    html = html.replace('{area_name}', area)
    html = html.replace('{receipt_number}', str(receipt_number))
    html = html.replace('{petrol_rate}', petrol_rate)
    html = html.replace('{amount}', str(amount))
    html = html.replace('{volume}', str(round(float(amount) / float(petrol_rate), 2)))
    html = html.replace('{vehicle_number}', vehicle)
    html = html.replace('{customer_name}', customer)
    html = html.replace('{date}', timestamp.strftime('%d %b %Y'))
    html = html.replace('{time}', timestamp.strftime('%H:%M'))

    output_file = f'{output_folder}/{timestamp}.pdf'
    pdfkit.from_string(html, output_file)

    return output_file


cleanup_output_dir(output_folder)

total_days = (end_date - start_date).days
total_bills = math.ceil(total_amount / amount_per_bill)

print(f'Processing from {start_date.date()} to {end_date.date()}')
print(f'Total Days: {total_days}\nTotal Bills: {total_bills}')

dates = [start_date]
while start_date != end_date:
    start_date += timedelta(days=1)
    dates.append(start_date)
dates = random.sample(dates, k=total_bills)
dates.sort()

files = []
for date in dates:
    date = date.replace(hour=random.randrange(10, 21), minute=random.randrange(60))
    file = generate_pdf(pump=pump_name,
                        area=area_name,
                        receipt_number=random.randrange(1000, 9999),
                        petrol_rate=fuel_rates[date.month],
                        amount=amount_per_bill,
                        vehicle=vehicle_number,
                        customer=customer_name,
                        timestamp=date)
    files.append(file)

merge_pdf_files(files, f'{output_folder}/{result_file}')
