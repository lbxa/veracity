---
name: shopify-catalogue-intake
description: Use when researching, counting, qualifying, or onboarding candidate Shopify source merchants for VALUE_ALPHA. Covers Shopify-backed store URL inspection, `/products.json` pagination, alternate storefront host probing, merchant catalogue counts, failed-store triage, aggregate totals, and turning merchant research into onboarding-ready catalog sync inputs.
---

# Shopify Catalogue Intake

Use this for lightweight merchant discovery before adding or changing VALUE_ALPHA merchant config. Keep it factual, repeatable, and separate from committed repo changes unless the user explicitly asks to wire merchants into code.

## Workflow

1. Capture the input merchant table with stable fields: `tier`, `slug`, `merchant`, and `baseUrl`.
2. Run `scripts/count_shopify_catalogues.py` from the repo root or a temp directory. Prefer CSV input for larger lists; JSON arrays are also accepted.
3. Count products, not variants, by paging `base/products.json?limit=250&page=N` until the final short page.
4. Mark failures explicitly. Do not include failed or partial stores in the aggregate total.
5. If a known Shopify store fails, probe likely alternate hosts before giving up:
   - strip or add `www.`
   - try `shop.<domain>`
   - inspect redirects and canonical shop links when browsing is available
6. Return a compact table with corrected base URLs, counts, statuses, and aggregate successful total.
7. For onboarding follow-up, list missing values separately: stable slug, canonical base URL, merchant priority, and any sync caveats.

## Script

Use:

```sh
/usr/bin/python3 .agents/skills/shopify-catalogue-intake/scripts/count_shopify_catalogues.py --input /path/to/merchants.csv
```

Input CSV columns:

```csv
tier,slug,merchant,baseUrl
1,vinnies,Vinnies (pilot),https://vinniesfinds.com.au
```

For a short one-off, pass repeated `--store` values:

```sh
/usr/bin/python3 .agents/skills/shopify-catalogue-intake/scripts/count_shopify_catalogues.py \
  --store '3|-|Swop|https://www.swop.net.au' \
  --probe-alternates
```

The script prints a fixed-width table and `AGGREGATE_TOTAL=<n>`.

## Guardrails

- Network access and merchant probing may need approval; ask only for the specific public endpoints being queried.
- Keep secrets out of inputs and outputs. Public Shopify product endpoints do not require credentials.
- Do not silently reuse stale counts; include the run date when reporting results.
- Do not commit temporary count outputs unless the user asks for durable merchant onboarding docs.
