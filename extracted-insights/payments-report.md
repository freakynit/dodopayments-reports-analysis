# Analysis - Payments Report

Generated: 2025-09-24T05:05:19.751801 UTC

**Dataset Summary:** 59 transactions analyzed

## Customer Analysis

Analyzes customer behavior and transaction patterns.

| Customer Email               |   Total Transactions |   Total Amount |   Average Transaction |   Successful Payments |   Total Fees Paid |   Success Rate (%) |
|:-----------------------------|---------------------:|---------------:|----------------------:|----------------------:|------------------:|-------------------:|
| nitinbansal85@gmail.com      |                   27 |       46147.36 |               1709.16 |                    18 |           1302.74 |              66.67 |
| nitin@gmail.com              |                    9 |       15430.76 |               1714.53 |                     5 |            362.94 |              55.56 |
| nitin1@gmail.com             |                    8 |       13754.13 |               1719.27 |                     8 |            582.18 |             100.00 |
| nitin2@gmail.com             |                    7 |       12004.56 |               1714.94 |                     4 |            290.73 |              57.14 |
| nitin3@gmail.com             |                    3 |        5148.76 |               1716.25 |                     3 |            217.96 |             100.00 |
| nitin4@gmail.com             |                    3 |        5147.39 |               1715.80 |                     3 |            217.91 |             100.00 |
| nitinbansal85.v2.1@gmail.com |                    2 |        3434.48 |               1717.24 |                     2 |            145.38 |             100.00 |

## Daily Transaction Volume

Shows daily transaction volume and revenue trends.

| Date       |   Transaction Count |   Total Amount |   Successful Amount |
|:-----------|--------------------:|---------------:|--------------------:|
| 2025-05-29 |                  27 |       46147.36 |            30765.84 |
| 2025-06-05 |                   7 |       12012.44 |             6866.66 |
| 2025-06-08 |                   2 |        3429.20 |             3429.20 |
| 2025-06-09 |                   5 |        8561.33 |             1712.21 |
| 2025-06-10 |                   1 |        1711.55 |             1711.55 |
| 2025-06-11 |                   2 |        3417.39 |             3417.39 |
| 2025-06-15 |                  11 |       18916.59 |            18916.59 |
| 2025-06-16 |                   4 |        6871.58 |             6871.58 |

## Failed Payment Analysis

Analyzes failed payments to identify patterns.

| Payment Method   |   Failed Count |   Lost Revenue |   Average Failed Amount |   Affected Customers |
|:-----------------|---------------:|---------------:|------------------------:|---------------------:|
| card             |              7 |       11963.90 |                 1709.13 |                    1 |
| upi              |              9 |       15412.52 |                 1712.50 |                    3 |

## Fee Analysis

Analyzes payment processing fees and their impact.

| Metric                      | Value      |
|:----------------------------|:-----------|
| Total Successful Revenue    | ₹73,691.02 |
| Total Processing Fees       | ₹3,119.84  |
| Average Fee per Transaction | ₹72.55     |
| Fee as % of Revenue         | 4.23%      |
| Net Revenue (After Fees)    | ₹70,571.18 |

## Hourly Transaction Pattern

Analyzes transaction patterns by hour of day.

|   Hour |   Transaction Count |   Average Amount |   Success Rate (%) |
|-------:|--------------------:|-----------------:|-------------------:|
|   4.00 |                1.00 |          1711.55 |             100.00 |
|   5.00 |                1.00 |          1718.75 |             100.00 |
|   6.00 |                4.00 |          1711.86 |              50.00 |
|   7.00 |                1.00 |          1719.86 |             100.00 |
|   8.00 |                1.00 |          1709.71 |             100.00 |
|   9.00 |                4.00 |          1710.62 |             100.00 |
|  10.00 |                6.00 |          1709.89 |             100.00 |
|  11.00 |                8.00 |          1711.72 |              75.00 |
|  12.00 |               17.00 |          1713.16 |              52.94 |
|  13.00 |                2.00 |          1717.14 |             100.00 |
|  14.00 |               10.00 |          1714.67 |              70.00 |
|  15.00 |                2.00 |          1719.69 |             100.00 |
|  17.00 |                1.00 |          1712.49 |               0.00 |
|  18.00 |                1.00 |          1708.01 |             100.00 |

## Payment Method Analysis

Analyzes performance by payment method (card vs UPI).

| Payment Method   |   Total Transactions |   Total Amount |   Average Amount |   Total Fees |   Average Fee |   Success Rate (%) |
|:-----------------|---------------------:|---------------:|-----------------:|-------------:|--------------:|-------------------:|
| card             |                   13 |       22261.73 |          1712.44 |       435.92 |         33.53 |              46.15 |
| upi              |                   46 |       78805.71 |          1713.17 |      2683.92 |         58.35 |              80.43 |

## Payment Status Summary

Summarizes successful vs failed payments with amounts and counts.

| Payment Status   |   Transaction Count |   Total Amount |   Average Amount |   Total Fees |
|:-----------------|--------------------:|---------------:|-----------------:|-------------:|
| failed           |                  16 |       27376.42 |          1711.03 |         0.00 |
| succeeded        |                  43 |       73691.02 |          1713.74 |      3119.84 |

## Settlement Analysis

Analyzes settlement amounts vs original amounts.

| Settlement Currency   |   Original Amount |   Settlement Amount |   Total Amount Diff |   Avg Amount Diff |   Original Tax |   Settlement Tax |   Total Tax Diff |   Avg Tax Diff |   Transaction Count |
|:----------------------|------------------:|--------------------:|--------------------:|------------------:|---------------:|-----------------:|-----------------:|---------------:|--------------------:|
| INR                   |          73691.02 |            73691.02 |                0.00 |              0.00 |       11241.00 |         11241.00 |             0.00 |           0.00 |                  43 |

## Tax Analysis

Analyzes tax collection and rates across transactions.

| Payment Method   |   Total Tax Collected |   Average Tax per Transaction |   Average Tax Rate (%) |   Total Gross Amount |
|:-----------------|----------------------:|------------------------------:|-----------------------:|---------------------:|
| card             |               1570.86 |                        261.81 |                  18.00 |             10297.83 |
| upi              |               9670.14 |                        261.36 |                  18.00 |             63393.19 |
| TOTAL            |              11241.00 |                        261.42 |                  18.00 |             73691.02 |

## Wallet Balance Trend

Tracks wallet balance changes over time (only for successful payments).

| Transaction               | Date             |   Wallet Balance |   Balance Change |
|:--------------------------|:-----------------|-----------------:|-----------------:|
| pay_pZEHCsPxv0DFtiqwMOPHI | 2025-06-15 12:55 |         46874.82 |          1384.57 |
| pay_wLnybo60uUgy2aNThGgFd | 2025-06-15 13:07 |         48259.39 |          1384.57 |
| pay_31GHfNgxXbAR7rNEkLTux | 2025-06-15 14:41 |         49643.96 |          1384.57 |
| pay_7kpLlu7LPKf6QqUcIxAml | 2025-06-15 14:43 |         51028.53 |          1384.57 |
| pay_jiFZiOPp3NJ65DEX5Vkec | 2025-06-15 15:00 |         52413.10 |          1384.57 |
| pay_0rW0qhCjA7lJQ38XqvzJz | 2025-06-15 15:54 |         53797.67 |          1384.57 |
| pay_IrRHWVbcDonOKAkAPwsk2 | 2025-06-16 07:30 |         55182.38 |          1384.71 |
| pay_6PWukSmCvYOEDNggpyd0d | 2025-06-16 14:12 |         56564.98 |          1382.60 |
| pay_prFr6lR83TnvovLwkBNFH | 2025-06-16 14:17 |         57947.58 |          1382.60 |
| pay_BKzyQ6IHGwpQSGPyoLkyx | 2025-06-16 14:26 |         59330.18 |          1382.60 |

