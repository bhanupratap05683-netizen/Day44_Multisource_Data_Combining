# Day 44 — Multi-Source Data Combining

**Phase 3 | 84-Day Python & Excel Roadmap**
**Topic:** Merge Excel + CSV + API (JSON) data into a unified dataset

---

## Files

| File | Type | Description |
|---|---|---|
| `company_financials.xlsx` | Excel | Source 1 — Revenue, Net Income, EPS, Debt for 7 companies |
| `sector_data.csv` | CSV | Source 2 — Sector, Cap category, Dividend Yield |
| `api_stock_prices.json` | JSON | Source 3 — Simulated API: Price, PE Ratio, 52W High/Low |
| `Day44_MultiSource_Combining.py` | Python | Main practice script — all 10 steps |
| `Day44_Unified_Dataset.xlsx` | Output | 4-sheet export: Unified, Inner Join, Outer Join, NaN Filled |

---

## Concepts Covered

- `pd.merge()` with `how='inner'`, `'left'`, `'right'`, `'outer'`
- Merging on a single key and multiple keys (`on=[...]`)
- `pd.concat()` for vertical row-stacking
- Handling NaN values after merge
- Three-source chained merge pipeline
- `pd.ExcelWriter` multi-sheet export

---

## Run

```bash
python Day44_MultiSource_Combining.py
```

---

## Key Takeaway

Real-world data always comes from multiple systems — financial data from Excel, reference data from CSVs, live prices from APIs. `pd.merge()` is the core tool for combining them. Always use `how='left'` when you want to preserve your primary dataset and enrich it with additional columns.

---

*Author: Bhanu Pratap Singh | Date: Day 44 | Phase 3 — Data Cleaning & Processing*
