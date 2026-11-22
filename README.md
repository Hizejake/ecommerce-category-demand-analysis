# E-Commerce Category and Demand Analysis

## Dataset
This project uses the public **Brazilian E-Commerce Public Dataset by Olist**: approximately 100,000 real, anonymized orders from 2016–2018 across multiple Brazilian marketplaces.

- Source: [Olist public dataset mirror](https://github.com/infobarbosa/dataset-olist)
- License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- Attribution: Olist, *Brazilian E-Commerce Public Dataset by Olist*, Kaggle

## Executive summary
- **Top category by delivered GMV:** health_beauty — R$1,233,131.72
- **Delivered orders analyzed:** 96,478
- **Product items analyzed:** 110,197
- **Estimated repeat-customer share:** 3.00%

## Category summary
| category              |   gross_merchandise_value |   freight_value |   order_count |   item_count |    aov |
|:----------------------|--------------------------:|----------------:|--------------:|-------------:|-------:|
| health_beauty         |                1233131.72 |       178957.81 |          8647 |         9465 | 142.61 |
| watches_gifts         |                1166176.98 |        98156.14 |          5495 |         5859 | 212.23 |
| bed_bath_table        |                1023434.76 |       201774.50 |          9272 |        10953 | 110.38 |
| sports_leisure        |                 954852.55 |       163404.36 |          7530 |         8431 | 126.81 |
| computers_accessories |                 888724.61 |       143999.16 |          6530 |         7644 | 136.10 |
| furniture_decor       |                 711927.69 |       168402.23 |          6307 |         8160 | 112.88 |
| housewares            |                 615628.69 |       142763.56 |          5743 |         6795 | 107.20 |
| cool_stuff            |                 610204.10 |        81476.79 |          3559 |         3718 | 171.45 |
| auto                  |                 578966.65 |        90488.10 |          3810 |         4140 | 151.96 |
| toys                  |                 471286.48 |        75774.58 |          3804 |         4030 | 123.89 |
| garden_tools          |                 470495.28 |        96650.40 |          3448 |         4268 | 136.45 |
| baby                  |                 400421.84 |        66305.81 |          2809 |         2982 | 142.55 |
| perfumery             |                 390144.65 |        53026.98 |          3086 |         3340 | 126.42 |
| telephony             |                 309860.23 |        69342.39 |          4093 |         4430 |  75.70 |
| office_furniture      |                 268154.31 |        67057.05 |          1254 |         1668 | 213.84 |

## Recommendations
1. Protect assortment depth and stock availability for high-GMV categories.
2. Monitor freight cost alongside GMV so category growth does not weaken delivery economics.
3. Focus retention campaigns on categories with a high repeat-customer share.
4. Track monthly GMV, order count, average order value, and freight as a category dashboard.

## Method
The analysis joins delivered orders, order items, products, category translations, and customers. It calculates category GMV, order counts, item counts, average order value, monthly demand, and repeat-customer share. No synthetic observations are used.
