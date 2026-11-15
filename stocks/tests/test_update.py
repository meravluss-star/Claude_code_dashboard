#!/usr/bin/env python3
"""Tests for update_stocks.py using saved responses (no network, no API key).

Run: python stocks/tests/test_update.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(HERE), "scripts", "update_stocks.py")
FIXTURES = os.path.join(HERE, "fixtures")
failures = []


def run(data_dir, **env):
    full = dict(os.environ, AV_FIXTURES=FIXTURES, AV_DATA_DIR=data_dir, AV_DELAY="0")
    full.pop("ALPHA_VANTAGE_KEY", None)
    full.update(env)
    p = subprocess.run([sys.executable, SCRIPT], env=full, capture_output=True, text=True)
    print(p.stdout + p.stderr)
    return p.returncode, p.stdout


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


def read(data_dir):
    with open(os.path.join(data_dir, "latest.json"), encoding="utf-8") as f:
        return json.load(f)


# 1. Full run with an empty data folder.
d = tempfile.mkdtemp()
code, out = run(d)
check(code == 0, "full run exits 0")
latest = read(d)
tickers = [s["ticker"] for s in latest["stocks"]]
check(tickers == ["NVDA", "ONFO", "NU", "RAIN", "FCUV", "INTC", "CRWV", "AKAN", "SPCX", "FRMI"],
      f"top 10 by volume, ETFs and sub-$0.50 shares removed: {tickers}")
check(latest["tradingDate"] == "2026-11-13", "trading date read from last_updated")
check(latest["apiCalls"] <= 20, f"stays within 20 requests (used {latest['apiCalls']})")
check(latest["seed"] is False, "seed flag is false after a real run")
nvda = latest["stocks"][0]
check(nvda["name"] == "NVIDIA Corporation" and nvda["sector"] == "TECHNOLOGY", "profile merged from COMPANY_OVERVIEW")
check(nvda["description"] == "Test company description, first sentence. Second sentence here.",
      f"description cut to two sentences: {nvda['description']!r}")
check([n["url"] for n in nvda["news"]] == ["https://example.com/c", "https://example.com/a"],
      "low-relevance news removed, newest first")
check(nvda["change"] == -3.34 and nvda["changePercent"] == -2.0097, "change and percent parsed")
check(latest["stocks"][1]["name"] == "Onfolio Holdings Inc", "name falls back to the listing when no profile")
check(latest["stocks"][5]["news"] == [], "rate-limit message for one stock does not stop the run")
with open(os.path.join(d, "cache.json"), encoding="utf-8") as f:
    cache = json.load(f)
check(cache["listing"]["SOXL"][0] == "ETF" and cache["listingUpdated"], "listing cached")

# 2. Second run for the same trading day: only 1 request, data unchanged.
code, out = run(d)
check(code == 0 and "already saved" in out and "request 2/" not in out, "same-day rerun uses only 1 request")

# 3. FORCE rerun: listing and NVDA profile come from cache.
code, out = run(d, FORCE="1")
check(code == 0 and "LISTING_STATUS" not in out and "COMPANY_OVERVIEW NVDA" not in out,
      "cached listing and fresh profiles are not requested again")
check(read(d)["apiCalls"] <= 20, "forced run stays within budget")

# 4. Tight budget: never more requests than AV_MAX_CALLS.
d2 = tempfile.mkdtemp()
code, out = run(d2, AV_MAX_CALLS="5")
check(code == 0, "run with a 5-request budget still saves data")
check(read(d2)["apiCalls"] == 5 and "request 6/" not in out, "never goes over AV_MAX_CALLS")

# 5. Missing key outside test mode fails clearly.
d3 = tempfile.mkdtemp()
env = dict(os.environ, AV_DATA_DIR=d3)
env.pop("AV_FIXTURES", None)
env.pop("ALPHA_VANTAGE_KEY", None)
p = subprocess.run([sys.executable, SCRIPT], env=env, capture_output=True, text=True)
check(p.returncode == 1 and "ALPHA_VANTAGE_KEY" in p.stdout, "missing key gives a clear error")
check(not os.path.exists(os.path.join(d3, "latest.json")), "no data written when the key is missing")

for x in (d, d2, d3):
    shutil.rmtree(x, ignore_errors=True)
print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
