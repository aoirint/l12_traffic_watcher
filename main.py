import requests
from bs4 import BeautifulSoup
import schedule
import os
from urllib.parse import urljoin
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import time


def do_task():
    router_root_url = os.environ['ROUTER_ROOT_URL']
    output_file = os.environ['OUTPUT_FILE']
    output_timezone = os.environ['OUTPUT_TIMEZONE']

    router_url = urljoin(router_root_url, 'cgi-bin/luci/')
    tz = ZoneInfo(output_timezone)

    r = requests.get(router_url)
    bs = BeautifulSoup(r.text, 'html5lib')

    daily_usage_bytes = bs.find(id='Traffic_Counter_daily_Lbl').attrs.get('value')
    monthly_usage_bytes = bs.find(id='Traffic_Counter_monthly_Lbl').attrs.get('value')

    daily_usage_gigabytes = int(daily_usage_bytes) / (10 ** 9)
    monthly_usage_gigabytes = int(monthly_usage_bytes) / (10 ** 9)

    now = datetime.now(tz=tz)

    print(f'{now.isoformat()} Daily: {daily_usage_gigabytes:.02f}, Monthly: {monthly_usage_gigabytes:.02f}')

    if not os.path.exists(output_file):
        with open(output_file, 'w') as fp:
            writer = csv.writer(fp)
            writer.writerow([
                'timestamp',
                'daily_usage_bytes',
                'monthly_usage_bytes',
            ])

    with open(output_file, 'a') as fp:
        writer = csv.writer(fp)
        writer.writerow([
            now.isoformat(),
            daily_usage_bytes,
            monthly_usage_bytes,
        ])


def main():
    output_interval = int(os.environ['OUTPUT_INTERVAL'])

    schedule.every(output_interval).seconds.do(do_task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
