# M1 · Mortgage Approval Model

> Find the leak that fakes a perfect score, then take a first fairness look at a lending model.

![Mortgage Approval Model](../../images/m1-mortgage-approval-model.jpg)
<sub>Screenshot of the project's own app.py, running on public HMDA mortgage records, Delaware 2024 (CFPB/FFIEC).</sub>

## What I built

I built a model that estimates the chance a home-loan application is denied, trained on 17,140 real applications made in Delaware in 2024. The brief, a fictional one, was a lender that wants to spot likely denials early so its advisers can help applicants fix what they can before they apply. I also built a Streamlit app that scores an application and says which answers moved the score most. It is for learning only, never for a real lending decision.

Real, public 2024 home-loan applications from Delaware, USA (US dollars; US lenders do not publish credit scores, so the model never sees one). A small app scores an application and says which answers moved it most.

## Tools

`Python` · `pandas` · `scikit-learn` · `Streamlit` · `Jupyter`

## Skills shown

- Spotting and removing data leakage
- Benchmarks and cross-validation
- Error rates by group, and choosing a cut-off
- Explaining a score in a Streamlit app

## Data

- CFPB/FFIEC HMDA public data, 2024 (public domain (US government work))

## Interview questions this project answers

<details>
<summary><b>Where does the data come from, and what did you keep?</b></summary>

It is public HMDA data for 2024, published by the CFPB and FFIEC for public use under US law, so it is a US government work in the public domain with no names or addresses. Of 48,786 Delaware records I kept 17,140: first-lien loans for the applicant's own single-family home, to buy or refinance, that were approved or denied. That gave 14,477 approved and 2,663 denied, or 15.54% denied. Credit scores and full credit history are not published, so my model never sees them.
</details>

<details>
<summary><b>Was there anything awkward about the data?</b></summary>

Yes: debt-to-income came as 19 different text values, a mix of bands and whole numbers, because lenders report it both ways. I turned each band into one number near its middle and kept the whole numbers, so each row has one figure. After that 16,060 of 17,140 applications had a value; the rest stay blank, and the gradient-boosting model handles blanks itself.
</details>

<details>
<summary><b>How did you know the interest rate column was a leak?</b></summary>

I grouped by decision and counted blanks: the interest rate was missing for 100.0% of denied applications and 0.1% of approved ones, because a rate is only set once a loan is approved. When I added "is the interest rate blank?" as a column the AUC became 1.0, which is perfect and useless. My rule is to ask of every column whether a lender would have it when the application arrives, and leave it out if not.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/m1-mortgage-approval-model).

[← All projects](../../README.md)
