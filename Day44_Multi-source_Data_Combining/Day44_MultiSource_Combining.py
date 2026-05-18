"""
Day 44 - Multi-Source Data Combining
Topic: Merge Excel + CSV + API (JSON) data → Build Unified Dataset
Author: Bhanu Pratap Singh
Phase 3 | 84-Day Python & Excel Roadmap
"""

import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

print("=" * 65)
print("  DAY 44 — MULTI-SOURCE DATA COMBINING")
print("  Sources: Excel  |  CSV  |  API (JSON)")
print("=" * 65)

# ══════════════════════════════════════════════════════════════════
# STEP 1 — Load Data from Each Source
# ══════════════════════════════════════════════════════════════════
print("\n📂 STEP 1: Loading All Sources")
print("-" * 40)

# Source 1: Excel
df_excel = pd.read_excel("company_financials.xlsx")
print(f"✅ Excel loaded   → {df_excel.shape[0]} rows, {df_excel.shape[1]} cols")
print(f"   Tickers: {list(df_excel['Ticker'])}")

# Source 2: CSV
df_csv = pd.read_csv("sector_data.csv")
print(f"✅ CSV loaded     → {df_csv.shape[0]} rows, {df_csv.shape[1]} cols")
print(f"   Tickers: {list(df_csv['Ticker'])}")

# Source 3: Simulated API (JSON file standing in for a real API call)
with open("api_stock_prices.json", "r") as f:
    api_raw = json.load(f)
df_api = pd.DataFrame(api_raw)
print(f"✅ API loaded     → {df_api.shape[0]} rows, {df_api.shape[1]} cols")
print(f"   Tickers: {list(df_api['Ticker'])}")

# ══════════════════════════════════════════════════════════════════
# STEP 2 — INNER JOIN: Only rows that exist in BOTH DataFrames
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 2: INNER JOIN — Excel + CSV (only common Tickers)")
print("-" * 55)
# how='inner' → keeps ONLY rows where Ticker exists in BOTH
df_inner = pd.merge(df_excel, df_csv, on="Ticker", how="inner")
print(f"Excel rows: {len(df_excel)} | CSV rows: {len(df_csv)} | After INNER: {len(df_inner)}")
print("Kept Tickers:", list(df_inner["Ticker"]))
print("⚠️  WIPRO & BAJAJFIN dropped (not in CSV). MARUTI & SUNPHARMA dropped (not in Excel).")
print(df_inner[["Ticker", "Company_Name", "Sector", "Revenue_Cr"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 3 — LEFT JOIN: Keep ALL rows from LEFT (Excel), fill NaN where CSV has no match
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 3: LEFT JOIN — Excel (left) + CSV (right)")
print("-" * 55)
# how='left' → keeps ALL rows from df_excel; CSV columns are NaN if no match
df_left = pd.merge(df_excel, df_csv, on="Ticker", how="left")
print(f"After LEFT JOIN: {len(df_left)} rows  (same as Excel — no rows lost)")
print("Tickers with NaN in Sector column:")
missing_sector = df_left[df_left["Sector"].isna()]["Ticker"].tolist()
print(" ", missing_sector if missing_sector else "None")
print(df_left[["Ticker", "Company_Name", "Sector", "Dividend_Yield_Pct"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 4 — RIGHT JOIN: Keep ALL rows from RIGHT (CSV), fill NaN where Excel has no match
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 4: RIGHT JOIN — Excel (left) + CSV (right)")
print("-" * 55)
# how='right' → keeps ALL rows from df_csv; Excel columns NaN if no match
df_right = pd.merge(df_excel, df_csv, on="Ticker", how="right")
print(f"After RIGHT JOIN: {len(df_right)} rows  (same as CSV — no rows lost)")
print("Rows with NaN Revenue_Cr (in CSV but not Excel):")
print(df_right[df_right["Revenue_Cr"].isna()][["Ticker", "Sector", "Revenue_Cr"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 5 — OUTER JOIN: Keep ALL rows from BOTH DataFrames (union)
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 5: OUTER JOIN — Excel + CSV (everything from both)")
print("-" * 55)
# how='outer' → union of both. Missing values filled with NaN
df_outer = pd.merge(df_excel, df_csv, on="Ticker", how="outer")
print(f"Excel: {len(df_excel)} + CSV: {len(df_csv)} unique. After OUTER: {len(df_outer)} rows")
print(df_outer[["Ticker", "Company_Name", "Sector", "Revenue_Cr"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 6 — MERGING ON MULTIPLE KEYS
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 6: MERGE ON MULTIPLE KEYS")
print("-" * 55)
# Adding Exchange column to Excel df to demonstrate multi-key merge
df_excel_copy = df_excel.copy()
df_excel_copy["Exchange"] = "NSE"   # simulate a second key

df_multikey = pd.merge(
    df_excel_copy,
    df_csv,
    on=["Ticker", "Exchange"],  # ← TWO keys must match
    how="inner"
)
print(f"Multi-key merge (Ticker + Exchange): {len(df_multikey)} rows")
print(df_multikey[["Ticker", "Exchange", "Sector", "Revenue_Cr"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 7 — THREE-SOURCE MERGE (Excel + CSV + API)
# ══════════════════════════════════════════════════════════════════
print("\n\n🔗 STEP 7: THREE-SOURCE MERGE — Excel + CSV + API")
print("-" * 55)
# Step A: Merge Excel + CSV (left join to keep all financials)
step_a = pd.merge(df_excel, df_csv, on="Ticker", how="left")
print(f"Step A (Excel + CSV, left): {len(step_a)} rows")

# Step B: Merge result with API (left join again)
df_unified = pd.merge(step_a, df_api, on="Ticker", how="left")
print(f"Step B (+ API, left):       {len(df_unified)} rows, {df_unified.shape[1]} columns")
print("\nUnified Dataset Preview:")
print(df_unified[["Ticker", "Sector", "Revenue_Cr", "Current_Price", "PE_Ratio"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 8 — pd.concat(): Stack DataFrames vertically (row-wise)
# ══════════════════════════════════════════════════════════════════
print("\n\n📚 STEP 8: pd.concat() — Stack DataFrames Row-Wise")
print("-" * 55)
# Split unified df into two halves, then stack them back
df_part1 = df_unified.iloc[:3].copy()   # rows 0,1,2
df_part2 = df_unified.iloc[3:].copy()   # rows 3,4,5,6

df_stacked = pd.concat([df_part1, df_part2], ignore_index=True)
print(f"Part1: {len(df_part1)} rows | Part2: {len(df_part2)} rows | Stacked: {len(df_stacked)} rows")
print(df_stacked[["Ticker", "Company_Name", "Revenue_Cr"]].to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# STEP 9 — Handle NaN After Merge (fill missing values)
# ══════════════════════════════════════════════════════════════════
print("\n\n🧹 STEP 9: Handle NaN in Merged Data")
print("-" * 55)
print("NaN count per column BEFORE filling:")
print(df_unified.isna().sum()[df_unified.isna().sum() > 0].to_string())

df_filled = df_unified.copy()
# Fill numeric NaN with 0 (or use median, mean depending on context)
numeric_cols = df_filled.select_dtypes(include="number").columns
df_filled[numeric_cols] = df_filled[numeric_cols].fillna(0)
# Fill string NaN with "Unknown"
str_cols = df_filled.select_dtypes(include="object").columns
df_filled[str_cols] = df_filled[str_cols].fillna("Unknown")

print("\nNaN count AFTER filling:", df_filled.isna().sum().sum())

# ══════════════════════════════════════════════════════════════════
# STEP 10 — Export Unified Dataset to Excel (multi-sheet)
# ══════════════════════════════════════════════════════════════════
print("\n\n💾 STEP 10: Export to Excel — Multiple Sheets")
print("-" * 55)

with pd.ExcelWriter("Day44_Unified_Dataset.xlsx", engine="openpyxl") as writer:
    df_unified.to_excel(writer, sheet_name="Unified_All", index=False)
    df_inner.to_excel(writer, sheet_name="Inner_Join", index=False)
    df_outer.to_excel(writer, sheet_name="Outer_Join", index=False)
    df_filled.to_excel(writer, sheet_name="NaN_Filled", index=False)

print("✅ Day44_Unified_Dataset.xlsx saved with 4 sheets")

# ══════════════════════════════════════════════════════════════════
# QUICK REFERENCE SUMMARY
# ══════════════════════════════════════════════════════════════════
print("\n")
print("=" * 65)
print("  JOIN TYPE CHEATSHEET")
print("=" * 65)
print("  INNER  → Only rows where key exists in BOTH  (intersection)")
print("  LEFT   → ALL rows from LEFT + matching from RIGHT")
print("  RIGHT  → ALL rows from RIGHT + matching from LEFT")
print("  OUTER  → ALL rows from BOTH (union) — NaN where no match")
print("  concat → Stack DataFrames row-wise (same columns needed)")
print("=" * 65)
print("\n✅ Day 44 Complete!")
