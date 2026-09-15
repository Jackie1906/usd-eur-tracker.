"""
Fetches the latest published monthly USD/EUR reference rate from the
European Central Bank and appends it to usd_eur_rates.csv (if it isn't
already there).

Runs standalone: python3 fetch_rate.py
"""

import csv
import os
import urllib.request

ECB_URL = (
    "https://data-api.ecb.europa.eu/service/data/EXR/"
    "M.USD.EUR.SP00.A?format=csvdata&lastNObservations=1"
)
CSV_FILE = "usd_eur_rates.csv"


def fetch_latest_rate():
    """Returns (period, value) e.g. ('2026-08', 1.1593)."""
    req = urllib.request.Request(ECB_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    lines = [line for line in data.strip().splitlines() if line]
    header = lines[0].split(",")
    last_row = lines[-1].split(",")

    period = last_row[header.index("TIME_PERIOD")]
    value = float(last_row[header.index("OBS_VALUE")])
    return period, value


def append_if_new(period, value):
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="") as f:
            rows = list(csv.reader(f))

    if not rows:
        rows.append(["Month", "USD_per_EUR", "EUR_per_USD"])

    existing_months = {r[0] for r in rows[1:]}
    if period in existing_months:
        print(f"{period} is already recorded — nothing to do.")
        return False

    rows.append([period, f"{value:.4f}", f"{1 / value:.4f}"])

    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"Added {period}: {value:.4f} USD per EUR")
    return True


if __name__ == "__main__":
    period, value = fetch_latest_rate()
    append_if_new(period, value)
