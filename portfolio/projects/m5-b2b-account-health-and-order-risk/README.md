# M5 · B2B Account Health and Order Risk

> Three models that tell a sales team whom to call, what to expect and which orders to confirm.

![B2B Account Health and Order Risk](../../images/m5-b2b-account-health-and-order-risk.jpg)
<sub>Screenshot of the project's own Flask dashboard (app.py), running on its made-up company data.</sub>

## What I built

It predicts three things for a B2B supplier with 304 active accounts: which accounts will reorder in the next 30 days, which are about to go quiet, and which open orders may be cancelled before dispatch. Each score comes with its top three reasons and a next step, in a dashboard for the sales head, the reps, planning and the order desk. Today it lists 44 accounts worth watching, with Rs 9.32 crore of yearly revenue at risk.

A data-cleaning layer is scored against hidden truth.

## Tools

`Python` · `pandas` · `XGBoost` · `SHAP` · `Flask` · `Jupyter`

## Skills shown

- Defining churn when customers never cancel
- Leakage-safe features and time splits with a purge gap
- XGBoost vs logistic regression vs a business rule
- SHAP reasons and a Flask dashboard

## Data

- Made by the project's own generator (seed 42); no real company (made up and owned by Compounza)
- Made by the project's own generator (seed 42); no real person (made up and owned by Compounza)

## Interview questions this project answers

<details>
<summary><b>How did you define churn when B2B customers never cancel a subscription?</b></summary>

An account has churned if it places no order for twice its usual gap between orders, with a 90-day floor and a 150-day cap. It is relative to each account’s rhythm, because 60 days of silence means trouble for a weekly buyer and nothing for a bimonthly one. The floor stops one skipped cycle counting as churn; the cap keeps recent months labelled.
</details>

<details>
<summary><b>How did you prevent data leakage?</b></summary>

At two levels. Every feature for a date T uses only facts known at T, by the date each fact became known: an order placed before T but cancelled after T still counts as live. And the split is by time with a purge gap as long as the label window (150 days for churn), so no training label looks into the test period.
</details>

<details>
<summary><b>Why not report accuracy?</b></summary>

Because the outcomes are rare: only 6.3% of test orders were cancelled, so predicting “never” scores 94% and is useless. I report PR-AUC and precision in the top 10%, because the business acts on a short list.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/m5-b2b-account-health-and-order-risk).

[← All projects](../../README.md)
