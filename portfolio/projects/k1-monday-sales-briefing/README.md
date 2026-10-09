# K1 · Monday Sales Briefing

> One command turns a sales file into a weekly briefing, ready to email.

![Monday Sales Briefing](../../images/k1-monday-sales-briefing.jpg)
<sub>The first page of the briefing PDF the project's briefing.py writes, from its made-up sales data.</sub>

## What I built

Every Monday someone built the same sales report by hand. My Python tool does it with one command: it takes the latest full week, compares it with the week before, and writes an Excel report and a one-page PDF. It can then email both from the classic Outlook app or from Gmail, so the Sales Head gets the numbers without anyone spending their morning on it.

A Python tool picks the latest full week, compares it with the week before, and writes an Excel report and a one-page PDF, and sends them through the classic Outlook app on Windows, with no password in the code.

## Tools

`Python` · `pandas` · `openpyxl` · `matplotlib` · `Outlook (Gmail optional)` · `Jupyter`

## Skills shown

- Automating a weekly report in Python
- Writing Excel files with charts (openpyxl)
- Drawing a one-page PDF (matplotlib)
- Sending email safely: Outlook automation or an app password in .env

## Data

- Riverstone Supplies sales, fictional (made up and owned by Compounza)

## Interview questions this project answers

<details>
<summary><b>What data does it use, and what did you have to watch out for?</b></summary>

It reads a CSV of every 2025 order line for all branches, 87,011 rows up to 28 December 2025, one row per line with region, category, customer and revenue. The data is fictional, made by Compounza. Cancelled orders are kept in the file and marked, so the tool drops them when it loads the data; otherwise revenue would be overstated.
</details>

<details>
<summary><b>How does it choose "last week"?</b></summary>

It starts from the last date in the file, goes back six days, then back to that Monday. If the Sunday of that week is later than the last date, the week is not complete, so it steps back one more week. The file ends on Sunday 28 December 2025, so it picked the week of 22 Dec 2025. You can also ask for a week with --week, and anything that is not a Monday is refused with a clear message.
</details>

<details>
<summary><b>Which figures are in the briefing, and how are they built?</b></summary>

One small function works out four figures for any slice of data: revenue, orders as unique order IDs, average order and unique customers. It runs on this week and on the week before, and the change is this week over last week minus one. The Excel file has a Summary sheet, then By region, By category and Top customers (the top 10), and the PDF shows the four figures with two charts.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/k1-monday-sales-briefing).

[← All projects](../../README.md)
