import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent
DATA = OUT / "data" / "category_sales.csv"


def generate_data():
    import numpy as np
    DATA.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    rows = []
    categories = ["Women Western", "Men Casual", "Kids", "Beauty", "Sportswear"]
    for month in range(1, 13):
        for category in categories:
            base = {"Women Western": 160, "Men Casual": 145, "Kids": 95, "Beauty": 110, "Sportswear": 125}[category]
            seasonality = 1 + 0.12 * np.sin((month - 1) / 12 * 2 * np.pi)
            orders = int(base * seasonality * rng.uniform(0.90, 1.10))
            aov = rng.uniform(1450, 2400)
            revenue = orders * aov
            margin_rate = rng.uniform(0.18, 0.32)
            conversion = rng.uniform(0.025, 0.065)
            repeat_rate = rng.uniform(0.18, 0.38)
            discount = rng.uniform(0.08, 0.28)
            rows.append([month, category, orders, round(revenue), round(revenue * margin_rate), round(conversion * 100, 2), round(repeat_rate * 100, 2), round(discount * 100, 2), round(aov, 2)])
    pd.DataFrame(rows, columns=["month", "category", "orders", "revenue", "margin", "conversion_pct", "repeat_rate_pct", "discount_pct", "aov"]).to_csv(DATA, index=False)


def main():
    if not DATA.exists():
        generate_data()
    df = pd.read_csv(DATA)

    summary = df.groupby("category", as_index=False).agg(
        revenue=("revenue", "sum"), margin=("margin", "sum"),
        orders=("orders", "sum"), conversion_pct=("conversion_pct", "mean"),
        repeat_rate_pct=("repeat_rate_pct", "mean"), discount_pct=("discount_pct", "mean")
    )
    summary["margin_pct"] = summary["margin"] / summary["revenue"] * 100
    summary["aov"] = summary["revenue"] / summary["orders"]
    summary = summary.sort_values("revenue", ascending=False)
    summary.to_csv(OUT / "category_summary.csv", index=False)

    ax = summary.plot(x="category", y="revenue", kind="bar", figsize=(9, 5), legend=False, color="#4285F4")
    ax.set_title("Annual Revenue by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "revenue_by_category.png", dpi=180)
    plt.close()

    ax = df.groupby("month")["revenue"].sum().plot(marker="o", figsize=(9, 5), color="#0F9D58")
    ax.set_title("Monthly Revenue Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(OUT / "monthly_revenue_trend.png", dpi=180)
    plt.close()

    leader = summary.iloc[0]
    report = f"""# E-Commerce Category and Demand Analysis

## Executive summary
- **Top revenue category:** {leader['category']} — ₹{leader['revenue']:,.0f}
- **Average conversion:** {df['conversion_pct'].mean():.2f}%
- **Average repeat-purchase rate:** {df['repeat_rate_pct'].mean():.2f}%
- **Average discount:** {df['discount_pct'].mean():.2f}%

## Category summary
{summary.to_markdown(index=False, floatfmt='.2f')}

## Recommendations
1. Protect availability and assortment depth for top-revenue categories.
2. Test lower-discount, higher-margin bundles in categories with strong repeat rates.
3. Improve paid and organic discovery for categories with lower conversion.
4. Track revenue, margin, conversion, repeat rate, and inventory health together.

## Method
Synthetic monthly category data is used for a reproducible Myntra-style business analysis. KPI summaries and charts are generated with Python, Pandas, and Matplotlib.
"""
    (OUT / "README.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
