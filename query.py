"""Requêtes SQL (DuckDB, lecture seule) sur les CSV.
Usage : python query.py "select ..."   |   python query.py fichier.sql   |   python query.py  (interactif, 'exit' pour quitter)
Tables : deals, fx_rates, product_ref, currency_ref, cash_daily (si output/cash_daily.csv existe)."""
import sys
from pathlib import Path

import duckdb

from config import DEALS_CSV, FX_CSV, OUTPUT_CSV

sys.stdout.reconfigure(encoding="utf-8")  # tableaux DuckDB : la console Windows cp1252 plante sinon
con = duckdb.connect()  # en mémoire : les CSV ne sont jamais modifiés
for name, path in {"deals": DEALS_CSV, "fx_rates": FX_CSV, "product_ref": "data/product_ref.csv",
                   "currency_ref": "data/currency_ref.csv", "cash_daily": OUTPUT_CSV}.items():
    if Path(path).exists():
        con.execute(f"create view {name} as select * from read_csv_auto('{path}')")


def run(sql):
    try:
        con.sql(sql).show(max_rows=50)
    except duckdb.Error as e:
        print("Erreur :", e)


if len(sys.argv) > 1:
    arg = sys.argv[1]
    run(Path(arg).read_text(encoding="utf-8") if arg.endswith(".sql") else arg)
else:
    try:
        while (q := input("sql> ").strip()) not in ("exit", "quit"):
            if q:
                run(q)
    except (EOFError, KeyboardInterrupt):
        pass
