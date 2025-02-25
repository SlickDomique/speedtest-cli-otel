import os
import json
import schedule
import time
import datetime

from otel import send_logs, send_error

def run_speedtest():
    print("Running speedtest ", datetime.datetime.now().isoformat())
    speedtest_result = ""
    try:
        speedtest_result = os.popen("speedtest-cli --secure --json").read()
    except Exception as e:
        send_error("Error running speedtest-cli", e)
        print("Fail sending running speedtest-cli")
        return

    if not speedtest_result:
        send_error("No result from speedtest-cli")

    try:
        send_logs(json.loads(speedtest_result))
    except Exception as e:
        print("Fail sending logs")
        send_error("Error parsing logs", e)
        return
    print("Success")

every_seconds_from = int(os.environ.get("every_seconds_from") or 1500)
every_seconds_to = int(os.environ.get("every_seconds_to") or 2100)
schedule.every(every_seconds_from).to(every_seconds_to).seconds.do(run_speedtest)

print("Starting speedtest every", every_seconds_from, "to", every_seconds_to, "seconds")
run_speedtest()

while True:
    schedule.run_pending()
    time.sleep(1)
