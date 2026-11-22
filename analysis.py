import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent
DATA = OUT / "data"


def main():
    orders = pd.read_csv(DATA / "olist_orders_dataset.csv.gz")
    items = pd.read_csv(DATA / "olist_order_items_dataset.csv.gz")
    products = pd.read_csv(DATA / "olist_products_dataset.csv.gz")
    translations = pd.read_csv(DATA / "product_category_name_translation.csv.gz")
    customers = pd.read_csv(DATA / "olist_customers_dataset.csv.gz")

    delivered = orders.loc[orders["order_status"] == "delivered"].copy()
    delivered["order_purchase_timestamp"] = pd.to_datetime(delivered["order_purchase_timestamp"])
    delivered["month"] = delivered["order_purchase_timestamp"].dt.to_period("M").astype(str)

    category = (items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
                     .merge(translations, on="product_category_name", how="left")
                     .rename(columns={"product_category_name_english": "category"}))
    category["category"] = category["category"].fillna("unknown")

    fact = (delivered.merge(category, on="order_id", how="inner")
                     .merge(customers[["customer_id", "customer_unique_id"]], on="customer_id", how="left"))

    summary = fact.groupby("category", as_index=False).agg(
        gross_merchandise_value=("price", "sum"),
        freight_value=("freight_value", "sum"),
        order_count=("order_id", "nunique"),
        item_count=("order_item_id", "count")
    )
    summary["aov"] = summary["gross_merchandise_value"] / summary["order_count"]
    summary = summary.sort_values("gross_merchandise_value", ascending=False).head(15)
    summary.to_csv(OUT / "category_summary.csv", index=False)

    ax = summary.plot(x="category", y="gross_merchandise_value", kind="bar", figsize=(11, 6), legend=False, color="#4285F4")
    ax.set_title("Olist Delivered-Order GMV by Product Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Gross merchandise value (BRL)")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "gmv_by_category.png", dpi=180)
    plt.close()

    monthly = fact.groupby("month", as_index=False).agg(gmv=("price", "sum"), orders=("order_id", "nunique"))
    monthly.to_csv(OUT / "monthly_demand.csv", index=False)
    ax = monthly.plot(x="month", y="gmv", marker="o", figsize=(11, 5), legend=False, color="#0F9D58")
    ax.set_title("Monthly Delivered-Order GMV")
    ax.set_xlabel("Month")
    ax.set_ylabel("GMV (BRL)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "monthly_gmv_trend.png", dpi=180)
    plt.close()

    repeat_customer_orders = (fact.groupby("customer_unique_id")["order_id"].nunique()
                                  .gt(1).sum())
    repeat_rate = repeat_customer_orders / fact["customer_unique_id"].nunique() * 100
    leader = summary.iloc[0]

    report = f"""# E-Commerce Category and Demand Analysis

## Dataset
This project uses the public **Brazilian E-Commerce Public Dataset by Olist**: approximately 100,000 real, anonymized orders from 2016–2018 across multiple Brazilian marketplaces.

- Source: [Olist public dataset mirror](https://github.com/infobarbosa/dataset-olist)
- License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- Attribution: Olist, *Brazilian E-Commerce Public Dataset by Olist*, Kaggle

## Executive summary
- **Top category by delivered GMV:** {leader['category']} — R${leader['gross_merchandise_value']:,.2f}
- **Delivered orders analyzed:** {fact['order_id'].nunique():,.0f}
- **Product items analyzed:** {len(fact):,.0f}
- **Estimated repeat-customer share:** {repeat_rate:.2f}%

## Category summary
{summary.to_markdown(index=False, floatfmt='.2f')}

## Recommendations
1. Protect assortment depth and stock availability for high-GMV categories.
2. Monitor freight cost alongside GMV so category growth does not weaken delivery economics.
3. Focus retention campaigns on categories with a high repeat-customer share.
4. Track monthly GMV, order count, average order value, and freight as a category dashboard.

## Method
The analysis joins delivered orders, order items, products, category translations, and customers. It calculates category GMV, order counts, item counts, average order value, monthly demand, and repeat-customer share. No synthetic observations are used.
"""
    (OUT / "README.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
