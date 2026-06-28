#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

LIMIT = 250
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json,text/plain,*/*",
}


@dataclass(frozen=True)
class Store:
    tier: str
    slug: str
    merchant: str
    base_url: str


def normalize_base_url(base_url: str) -> str:
    base = base_url.strip().rstrip("/")
    if not base:
        raise ValueError("empty baseUrl")
    if "://" not in base:
        base = f"https://{base}"
    return base


def products_url(base_url: str, page: int) -> str:
    return f"{normalize_base_url(base_url)}/products.json?{urlencode({'limit': LIMIT, 'page': page})}"


def fetch_json(url: str) -> Any:
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset, errors="replace")
            return json.loads(body)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(0.75 * attempt)
    assert last_error is not None
    raise RuntimeError(str(last_error)) from last_error


def count_base_url(base_url: str) -> int:
    total = 0
    page = 1
    while True:
        data = fetch_json(products_url(base_url, page))
        if not isinstance(data, dict) or not isinstance(data.get("products"), list):
            raise RuntimeError("JSON did not contain products array")
        products = data["products"]
        total += len(products)
        if len(products) < LIMIT:
            return total
        page += 1


def alternate_bases(base_url: str) -> list[str]:
    parsed = urlparse(normalize_base_url(base_url))
    host = parsed.netloc
    if not host:
        return []
    candidates: list[str] = []
    if host.startswith("www."):
        candidates.append(f"{parsed.scheme}://{host[4:]}")
    else:
        candidates.append(f"{parsed.scheme}://www.{host}")
    root = host[4:] if host.startswith("www.") else host
    if not root.startswith("shop."):
        candidates.append(f"{parsed.scheme}://shop.{root}")
    return [candidate for candidate in candidates if candidate != normalize_base_url(base_url)]


def count_store(store: Store, probe_alternates: bool) -> tuple[int | None, str, str]:
    candidates = [normalize_base_url(store.base_url)]
    if probe_alternates:
        candidates.extend(alternate_bases(store.base_url))

    errors: list[str] = []
    for candidate in candidates:
        try:
            return count_base_url(candidate), "OK", candidate
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
    return None, "ERROR: " + " | ".join(errors), normalize_base_url(store.base_url)


def read_stores(path: Path | None, inline_stores: list[str]) -> list[Store]:
    stores: list[Store] = []
    if path:
        if path.suffix.lower() == ".json":
            data = json.loads(path.read_text())
            rows = data if isinstance(data, list) else data.get("stores", [])
            for row in rows:
                stores.append(Store(str(row.get("tier", "")), row.get("slug", "-"), row["merchant"], row["baseUrl"]))
        else:
            with path.open(newline="") as fh:
                for row in csv.DictReader(fh):
                    stores.append(Store(row.get("tier", ""), row.get("slug", "-"), row["merchant"], row["baseUrl"]))
    for value in inline_stores:
        parts = value.split("|", 3)
        if len(parts) != 4:
            raise ValueError("--store must use 'tier|slug|merchant|baseUrl'")
        stores.append(Store(*parts))
    return stores


def print_table(rows: list[dict[str, str]]) -> None:
    headers = ["tier", "slug", "merchant", "baseUrl", "count", "status"]
    widths = {header: max(len(header), *(len(row[header]) for row in rows)) for header in headers}
    print("  ".join(header.ljust(widths[header]) for header in headers))
    print("  ".join("-" * widths[header] for header in headers))
    for row in rows:
        print("  ".join(row[header].ljust(widths[header]) for header in headers))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count Shopify products for candidate merchants.")
    parser.add_argument("--input", type=Path, help="CSV or JSON merchant list")
    parser.add_argument("--store", action="append", default=[], help="Inline 'tier|slug|merchant|baseUrl' store")
    parser.add_argument("--probe-alternates", action="store_true", help="Try www/root/shop host variants after a failure")
    args = parser.parse_args()

    stores = read_stores(args.input, args.store)
    if not stores:
        parser.error("provide --input or at least one --store")

    rows: list[dict[str, str]] = []
    aggregate_total = 0
    for store in stores:
        count, status, effective_base = count_store(store, args.probe_alternates)
        if count is not None:
            aggregate_total += count
        rows.append(
            {
                "tier": store.tier,
                "slug": store.slug,
                "merchant": store.merchant,
                "baseUrl": effective_base,
                "count": str(count) if count is not None else "-",
                "status": status,
            }
        )

    print_table(rows)
    print(f"\nAGGREGATE_TOTAL={aggregate_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
