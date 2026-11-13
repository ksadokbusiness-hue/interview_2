"""Cash net journalier par produit, converti en EUR -> output/cash_daily.csv."""
from pathlib import Path

import pandas as pd

from config import DEALS_CSV, FX_CSV, OUTPUT_CSV


def compute_cash(deals: pd.DataFrame, fx: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, d in deals.iterrows():
        if d.status == "CANCELLED":
            continue
        sign = 1 if d.side == "SELL" else -1
        amount = sign * d.quantity * d.price - d.fee
        if d.currency == "EUR":
            rows.append((d.deal_date, d["product"], amount))
            continue
        r = fx[(fx.rate_date == d.deal_date) & (fx.currency == d.currency)]
        for _, x in r.iterrows():
            rows.append((d.deal_date, d["product"], amount / x.rate))
    df = pd.DataFrame(rows, columns=["deal_date", "product", "net_cash_eur"])
    return df.groupby(["deal_date", "product"], as_index=False).net_cash_eur.sum()


def run():
    deals = pd.read_csv(DEALS_CSV, parse_dates=["deal_date"])
    fx = pd.read_csv(FX_CSV, parse_dates=["rate_date", "published_at"])
    out = compute_cash(deals, fx)
    Path(OUTPUT_CSV).parent.mkdir(exist_ok=True)
    out.to_csv(OUTPUT_CSV, index=False)
    print(OUTPUT_CSV, ":", len(out), "lignes")


if __name__ == "__main__":
    run()
