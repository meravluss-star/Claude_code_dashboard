#!/usr/bin/env python3
"""Daily data update for the Market Movers dashboard (stocks/).

Runs once per trading day after the US market close (GitHub Actions, see
.github/workflows/update-stocks.yml). Uses only the Python standard library.

Alpha Vantage free tier: 25 requests per day. This script never makes more
than MAX_CALLS (default 20) requests per run, waits DELAY seconds between
requests, and skips the run entirely (1 request) when the trading day is
already saved. See stocks/spec.md section 2 for the full budget.

Environment variables:
  ALPHA_VANTAGE_KEY  API key (required unless AV_FIXTURES is set)
  AV_MAX_CALLS       hard limit on requests per run (default 20)
  AV_DELAY           seconds between requests (default 13 -> under 5 per minute)
  AV_DATA_DIR        folder with latest.json / cache.json (default stocks/data)
  AV_FIXTURES        folder with saved API responses, for tests (no network)
  FORCE              "1" = refresh even if this trading day is already saved
"""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("AV_DATA_DIR") or os.path.join(os.path.dirname(HERE), "data")
LATEST = os.path.join(DATA_DIR, "latest.json")
CACHE = os.path.join(DATA_DIR, "cache.json")

API = "https://www.alphavantage.co/query"
KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
FIXTURES = os.environ.get("AV_FIXTURES", "")
MAX_CALLS = int(os.environ.get("AV_MAX_CALLS", "20"))
DELAY = float(os.environ.get("AV_DELAY", "13"))
FORCE = os.environ.get("FORCE", "") in ("1", "true", "True")

TOP_N = 10                 # stocks shown on the dashboard
MIN_PRICE = 0.50           # skip sub-50-cent shares
NEWS_PER_STOCK = 3         # headlines per stock
MIN_RELEVANCE = 0.2        # Alpha Vantage ticker relevance score (0-1)
LISTING_MAX_AGE_DAYS = 7   # refresh the stock/ETF list weekly
PROFILE_MAX_AGE_DAYS = 30  # refresh company profiles monthly


class BudgetExceeded(Exception):
    """The per-run request limit was reached."""


class ApiError(Exception):
    """Alpha Vantage returned an error, a limit message or no data."""


calls = 0


def call(function, **params):
    """One Alpha Vantage request. Counts against the per-run budget."""
    global calls
    if calls >= MAX_CALLS:
        raise BudgetExceeded(function)
    calls += 1
    if FIXTURES:
        suffix = "".join("_" + params[k] for k in ("symbol", "tickers") if k in params)
        ext = ".csv" if function == "LISTING_STATUS" else ".json"
        path = os.path.join(FIXTURES, function + suffix + ext)
        if not os.path.exists(path):
            raise ApiError(f"{function}{suffix}: no fixture")
        with open(path, encoding="utf-8") as f:
            text = f.read()
    else:
        if calls > 1:
            time.sleep(DELAY)
        query = urllib.parse.urlencode({"function": function, **params, "apikey": KEY})
        req = urllib.request.Request(API + "?" + query, headers={"User-Agent": "market-movers-dashboard"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
    label = function + "".join(" " + params[k] for k in ("symbol", "tickers") if k in params)
    print(f"  request {calls}/{MAX_CALLS}: {label}")
    if function == "LISTING_STATUS":
        if not text.lstrip().lower().startswith("symbol"):
            raise ApiError(f"{label}: {text[:200]}")
        return text
    data = json.loads(text)
    if isinstance(data, dict):
        for k in ("Note", "Information", "Error Message"):
            if k in data:
                raise ApiError(f"{label}: {str(data[k])[:200]}")
    return data


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save(path, obj, pretty):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        if pretty:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        else:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def is_stale(iso_date, max_age_days):
    if not iso_date:
        return True
    try:
        return (dt.date.today() - dt.date.fromisoformat(iso_date[:10])).days >= max_age_days
    except ValueError:
        return True


def to_float(value, default=None):
    try:
        return float(str(value).replace("%", ""))
    except (TypeError, ValueError):
        return default


def parse_listing(csv_text):
    """symbol -> [assetType, name] for active US listings."""
    out = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        sym = (row.get("symbol") or "").strip()
        if sym:
            out[sym] = [(row.get("assetType") or "").strip(), (row.get("name") or "").strip()]
    return out


def is_candidate(item, listing):
    """Common stocks only: no ETFs, warrants, rights, units or sub-50-cent shares."""
    sym = item.get("ticker", "")
    price = to_float(item.get("price"), 0)
    if price < MIN_PRICE:
        return False
    if not re.fullmatch(r"[A-Z]{1,5}", sym):          # skips BRK.A, EONR+, etc.
        return False
    entry = listing.get(sym)
    if entry and entry[0].upper() == "ETF":
        return False
    if len(sym) == 5 and sym[-1] in "WRU" and sym[:-1] in listing:  # warrant/right/unit
        return False
    return True


def short_description(text, max_len=300):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if not text or text.lower() == "none":
        return ""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    out = ""
    for s in sentences[:2]:
        if len(out) + len(s) + 1 > max_len and out:
            break
        out = (out + " " + s).strip()
    if len(out) > max_len:
        out = out[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return out


def news_time(stamp):
    """'20261113T153000' -> '2026-11-13T15:30:00'."""
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})?", stamp or "")
    if not m:
        return ""
    y, mo, d, h, mi, s = m.groups()
    return f"{y}-{mo}-{d}T{h}:{mi}:{s or '00'}"


def pick_news(feed, sym):
    items = []
    for a in feed or []:
        ts = next((t for t in a.get("ticker_sentiment", []) if t.get("ticker") == sym), None)
        relevance = to_float(ts.get("relevance_score"), 0) if ts else 0
        if relevance < MIN_RELEVANCE or not a.get("title") or not a.get("url"):
            continue
        summary = re.sub(r"\s+", " ", a.get("summary") or "").strip()
        if len(summary) > 280:
            summary = summary[:279].rsplit(" ", 1)[0] + "…"
        items.append({
            "title": a["title"].strip(),
            "url": a["url"],
            "source": a.get("source", ""),
            "time": news_time(a.get("time_published", "")),
            "summary": summary,
            "sentiment": (ts.get("ticker_sentiment_label") if ts else "") or "",
            "relevance": round(relevance, 3),
        })
    items.sort(key=lambda n: (-n["relevance"], n["time"]), reverse=False)
    top = items[:NEWS_PER_STOCK]
    top.sort(key=lambda n: n["time"], reverse=True)
    return top


def profile_from_overview(o):
    if not isinstance(o, dict) or not o.get("Symbol"):
        return None
    return {
        "name": o.get("Name", ""),
        "exchange": o.get("Exchange", ""),
        "sector": o.get("Sector", ""),
        "industry": o.get("Industry", ""),
        "marketCap": to_float(o.get("MarketCapitalization")),
        "description": short_description(o.get("Description", "")),
        "updated": dt.date.today().isoformat(),
    }


def main():
    if not FIXTURES and not KEY:
        print("ERROR: ALPHA_VANTAGE_KEY is not set (add it as a repository secret).")
        return 1
    os.makedirs(DATA_DIR, exist_ok=True)
    latest = load(LATEST, {})
    cache = load(CACHE, {})
    cache.setdefault("listing", {})
    cache.setdefault("listingUpdated", None)
    cache.setdefault("profiles", {})
    warnings = []

    # 1. Most actively traded tickers (1 request).
    try:
        movers = call("TOP_GAINERS_LOSERS")
    except (ApiError, BudgetExceeded, OSError, ValueError) as e:
        print(f"ERROR: could not load market movers: {e}")
        return 1
    active = movers.get("most_actively_traded") if isinstance(movers, dict) else None
    if not active:
        print("ERROR: no 'most_actively_traded' data in the response.")
        return 1
    last_updated = movers.get("last_updated", "")
    trading_date = last_updated[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", trading_date):
        print(f"ERROR: unexpected last_updated value: {last_updated!r}")
        return 1

    if latest.get("tradingDate") == trading_date and not latest.get("seed") and not FORCE:
        print(f"Trading day {trading_date} is already saved (market closed or holiday). "
              f"Used {calls} request. Nothing to do.")
        return 0

    # 2. Stock/ETF list, refreshed weekly (0-1 request).
    if is_stale(cache["listingUpdated"], LISTING_MAX_AGE_DAYS):
        try:
            cache["listing"] = parse_listing(call("LISTING_STATUS"))
            cache["listingUpdated"] = dt.date.today().isoformat()
        except (ApiError, BudgetExceeded, OSError) as e:
            warnings.append(f"Listing not refreshed: {e}")
    listing = cache["listing"]

    picked = [m for m in active if is_candidate(m, listing)]
    picked.sort(key=lambda m: to_float(m.get("volume"), 0), reverse=True)
    picked = picked[:TOP_N]

    # 3. News for each stock (up to 10 requests).
    day = dt.date.fromisoformat(trading_date)
    time_from = (day - dt.timedelta(days=1)).strftime("%Y%m%dT0000")
    news = {}
    for m in picked:
        sym = m["ticker"]
        try:
            data = call("NEWS_SENTIMENT", tickers=sym, time_from=time_from, sort="LATEST", limit="50")
            news[sym] = pick_news(data.get("feed"), sym)
        except BudgetExceeded:
            warnings.append(f"News skipped for {sym}: request limit reached")
            news[sym] = []
        except (ApiError, OSError, ValueError) as e:
            warnings.append(f"News failed for {sym}: {e}")
            news[sym] = []

    # 4. Company profiles: only missing or older than 30 days (uses what is left of the budget).
    profiles = cache["profiles"]
    for m in picked:
        sym = m["ticker"]
        current = profiles.get(sym)
        if current and not is_stale(current.get("updated"), PROFILE_MAX_AGE_DAYS):
            continue
        try:
            p = profile_from_overview(call("COMPANY_OVERVIEW", symbol=sym))
            if p:
                profiles[sym] = p
            elif not current:
                warnings.append(f"No company profile for {sym}")
        except BudgetExceeded:
            warnings.append(f"Profile for {sym} postponed: request limit reached")
            break
        except (ApiError, OSError, ValueError) as e:
            warnings.append(f"Profile failed for {sym}: {e}")

    stocks = []
    for rank, m in enumerate(picked, start=1):
        sym = m["ticker"]
        p = profiles.get(sym, {})
        name = p.get("name") or (listing.get(sym) or ["", ""])[1] or sym
        stocks.append({
            "rank": rank,
            "ticker": sym,
            "name": name,
            "price": to_float(m.get("price")),
            "change": to_float(m.get("change_amount")),
            "changePercent": to_float(m.get("change_percentage")),
            "volume": int(to_float(m.get("volume"), 0)),
            "exchange": p.get("exchange", ""),
            "sector": p.get("sector", ""),
            "industry": p.get("industry", ""),
            "marketCap": p.get("marketCap"),
            "description": p.get("description", ""),
            "news": news.get(sym, []),
        })

    out = {
        "tradingDate": trading_date,
        "lastUpdated": last_updated,
        "generatedAt": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Alpha Vantage",
        "apiCalls": calls,
        "seed": False,
        "stocks": stocks,
    }
    save(LATEST, out, pretty=True)
    save(CACHE, cache, pretty=False)
    for w in warnings:
        print("  warning:", w)
    print(f"Saved {len(stocks)} stocks for {trading_date} using {calls} of {MAX_CALLS} requests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
