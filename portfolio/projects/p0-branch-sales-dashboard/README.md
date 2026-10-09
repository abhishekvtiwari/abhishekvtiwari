# P0 · Branch Sales Dashboard

> Turn three years of messy sales into a clickable dashboard, and find out why goods are coming back.

![Branch Sales Dashboard](../../images/p0-branch-sales-dashboard.jpg)
<sub>Excel's own picture of the project's finished dashboard (Excel 365), on its made-up sales data.</sub>

## What I built

I took three years of sales from four West-region branches, 1,27,735 rows in six linked sheets, cleaned them in Excel with formulas, and built one Dashboard sheet a manager can click through: five headline figures with the change on the year before, twelve charts, slicers for branch, category, segment and channel, and a timeline. It answered the manager's question about returns in a few clicks, and it shows every branch against its target.

Four branches, three years, 1.27 lakh rows in six linked sheets (orders, products, customers, returns, targets, status), with nine problems planted on purpose. Made-up company, made-up data. Needs Excel 2021, 2024 or Microsoft 365 (paid), tested on Windows. The finished dashboard is included to compare with.

## Tools

`Excel 2021, 2024 or Microsoft 365 (paid)`

## Skills shown

- Cleaning nine kinds of problem with TRIM, PROPER, DATE, VALUE, XLOOKUP and IF
- Linking six tables with XLOOKUP and structured references
- Pivot tables, calculated fields, pivot charts, slicers and a timeline
- GETPIVOTDATA and IFERROR for cards that follow the filters
- Targets with SUMIFS and a forecast with FORECAST.ETS
- Finding the cause behind a number

## Data

- Riverstone Supplies sales, fictional (made up and owned by Compounza)

## Interview questions this project answers

<details>
<summary><b>What was wrong with the data, and how did you fix it?</b></summary>

Nine things: 736 rows sent twice, 78 test orders from the IT team, customer names in odd capitals with extra spaces, branch names spelled several ways, including the old "Bombay", dates stored as day-first text, 5,140 quantities stored as text, product and status codes instead of names, and 4,587 blank discounts. I gave each its own fix and kept a table of the rows it touched before and the count after. The data is fictional, made by Compounza, with the problems planted on purpose.
</details>

<details>
<summary><b>How did you find the cause of the returns?</b></summary>

I clicked Storage in the Category slicer and the return-rate line jumped in April to June 2025. The brand chart, which ranks brands by returned lines, put Pragati first: 86 of its 392 bin and crate lines sent that quarter came back, 21.9%, against 0.5–3.8% in the other quarters. The reasons chart showed 50 of them were "Quality issue", so it was the product, not the delivery. Those refunds came to Rs 6.5 lakh.
</details>

<details>
<summary><b>How is a return rate worked out, and why not just count returns?</b></summary>

Returned lines divided by lines sent. Cancelled lines were never sent, so they are left out. It is a calculated field in the pivot, Returned ÷ Shipped, so it is worked out on the totals of whatever the slicers select. A count alone misleads: a busy branch has more returns simply because it sends more.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/p0-branch-sales-dashboard).

[← All projects](../../README.md)
