# M2 · Card Default Risk Model

> The credit dataset everyone uses, done the way a bank would.

![Card Default Risk Model](../../images/m2-card-default-risk-model.jpg)
<sub>Screenshot of the project's own app.py, running on the public "Default of Credit Card Clients" data, Yeh (2009), UCI Machine Learning Repository, CC BY 4.0.</sub>

## What I built

I built a model that estimates the chance a credit card holder misses next month's payment, from six months of their bills, payments and payment status. It learns from 30,000 real card holders of a bank in Taiwan. The brief, a fictional one, was a bank that wants to call at-risk customers early and offer a payment plan. My Streamlit app scores one card holder and shows which columns moved the score most.

The credit dataset everyone uses, done the way a bank would: the cut-off chosen by what a missed default costs, and a fairness check. Most public notebooks stop at accuracy. Data: the UCI “Default of Credit Card Clients” dataset, 30,000 card holders in Taiwan, 2005, amounts in NT$.

## Tools

`Python` · `pandas` · `scikit-learn` · `Streamlit` · `Jupyter`

## Skills shown

- Logistic regression and gradient boosting
- Why accuracy misleads on rare outcomes
- Choosing a cut-off by cost
- Explaining a score; a Streamlit app

## Data

- Yeh, I. (2009). Default of Credit Card Clients. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H (CC BY 4.0)

## Interview questions this project answers

<details>
<summary><b>Tell me about the data and its licence.</b></summary>

It is the Default of Credit Card Clients dataset (Yeh, 2009) from the UCI Machine Learning Repository, under CC BY 4.0, so I can use and publish it as long as I keep the credit line. It has 30,000 card holders and 25 columns, covering April to September 2005, with amounts in New Taiwan dollars and no names or contact details. One quirk: payment status uses codes, where 1 to 8 mean months late, but some codes are not explained by the source, so my app labels them as unexplained rather than guess.
</details>

<details>
<summary><b>Why is accuracy a poor measure here, and what did you use instead?</b></summary>

Only 22.12% of card holders defaulted, so a model that always says no default is right 77.88% of the time. My model's accuracy was 80.97%, only 3.09 points better than that. So I report AUC, which measures how well the model ranks risky card holders above safe ones (0.5 is guessing, 1 is perfect), and how many defaulters it actually catches.
</details>

<details>
<summary><b>What did you let the model use, and how did you test it?</b></summary>

I used 19 features: the credit limit and six months of payment status, bills and payments. I left out sex, age, marital status and education because the brief forbids them. I kept 25% aside, 7,500 card holders, and trained on 22,500, with the split stratified so both parts have the same share of defaulters.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/m2-card-default-risk-model).

[← All projects](../../README.md)
