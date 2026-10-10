# P0.5 · Monthly Sales Report Automation

> One click imports three years of messy monthly files and refreshes a monthly report you can turn to any month; you write four parts of the macro.

![Monthly Sales Report Automation](../../images/p05-monthly-sales-report-automation.jpg)
<sub>Excel's own picture of the monthly report the project's macro refreshes, on its made-up sales data.</sub>

## What I built

Every month the branch system sends a CSV file with the same problems, and someone cleans it by hand. With one click the macro imports every new file from an inbox folder, fixes its problems, adds the rows to an Excel table, moves the file to an imported folder, refreshes a monthly report that can be turned to any month (with a trends sheet behind it) and writes a log line of what it found. In the test it read 37 files, 1,13,231 rows, and kept 1,10,456, in about 26 seconds.

Four branches send 37 monthly sales files (1.13 lakh rows, 2023–2025) with ten problems planted on purpose: rows and a whole month sent twice, repeated headers, total lines, misspelt branches, text dates and quantities, codes and blanks. A VBA macro fixes and counts every one and refreshes a monthly report (any month, against last month and a year earlier, with the branches ranked and what needs attention) and a trends sheet. Made-up company, made-up data. Windows Excel 2021, 2024 or Microsoft 365 only (paid).

## Tools

`Excel on Windows (2021, 2024 or Microsoft 365, paid)` · `VBA`

## Skills shown

- Writing VBA: a duplicate-row skip, DateSerial, TRIM and PROPER, a repeat-month guard
- Reading a folder of files with Dir, and lookups with Scripting.Dictionary
- Writing rows to a table in one block
- Error handling that tells the user what failed
- A monthly report turned to any month with one drop-down: SUMIFS, SORTBY and a branch league table against target
- A trends sheet: pivots with slicers, a timeline, targets and a forecast

## Data

- Riverstone Supplies sales, fictional (made up and owned by Compounza)

## Interview questions this project answers

<details>
<summary><b>What was wrong with the files, and how did you know the fixes worked?</b></summary>

Ten things, planted on purpose: 2,745 rows sent twice, one month sent again under a new name, the header line repeated in 13 files, a TOTAL line in 17, 6,502 branch names like Bangalore or Madras, names in odd capitals, day-first text dates, 4,388 quantities stored as text, codes instead of names and 4,754 blank discounts. The macro counts each one in its log, and the four checks prove the result. The data is made up.
</details>

<details>
<summary><b>How does it avoid importing a month twice?</b></summary>

Before importing a file it reads the month of its first order line and looks it up in a dictionary of the months already in the table. If the month is there, the file is moved aside as skipped. Checking the month, not the file name, matters: the test inbox had south_sales_2024_06_resent.csv, a copy of June 2024 under a new name, and a name check would have let it in.
</details>

<details>
<summary><b>How does it skip rows sent twice?</b></summary>

Each line of the file goes into a Scripting.Dictionary as it is read. A line already in the dictionary is the same row sent twice, so it is counted and skipped. A dictionary lookup is fast, so this stays quick on a file with thousands of rows.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/p05-monthly-sales-report-automation).

[← All projects](../../README.md)
