# M4 · Rupee Forecast Reality Check

> Put a rupee forecast to the test: catch the leak that fakes 84%, and prove whether 51% beats luck.

![Rupee Forecast Reality Check](../../images/m4-rupee-forecast-reality-check.jpg)
<sub>Screenshot of the project's own app.py, running on US Federal Reserve H.10 rupee-dollar rates and public market series (listed in the project’s data sources).</sub>

## What I built

I built a model that predicts whether tomorrow's rupees-per-dollar rate will be higher than today's, and an app that replays its calls month by month. Tested on 1,683 trading days it never saw, it was right 51.3% of the time, against 49.8% for always guessing the usual direction. That is barely better than a coin, and proving it properly was the real work.

Not a trading tool. The result is 51.3% right, which cannot be told apart from a coin, and one look-ahead mistake that makes it look 84% right. A small app replays any month.

## Tools

`Python` · `pandas` · `scikit-learn` · `Streamlit` · `Jupyter`

## Skills shown

- Time-series features without look-ahead
- Time-based testing and baselines
- Telling skill from luck with a binomial test
- Linking economic drivers; a Streamlit app

## Data

- Board of Governors of the Federal Reserve System, H.10 (public domain)
- Federal Reserve Board H.15 and H.10; U.S. Energy Information Administration (via FRED) (public domain)
- OECD Financial market and International trade datasets (CC BY 4.0)

## Interview questions this project answers

<details>
<summary><b>What data did you use?</b></summary>

6,702 days of real exchange rates from the US Federal Reserve's H.10 release, 2000-01-03 to 2026-09-25, going from 43.55 to 95.81 rupees per dollar; it is public domain. For drivers I added US policy and bond rates, the dollar index, Brent oil and US gas, all public domain, and India's call money rate, 10-year yield, exports and imports from the OECD under CC BY 4.0. On 46.8% of days the rate went up the next day.
</details>

<details>
<summary><b>Why not split the days at random?</b></summary>

A random split lets the model learn from days after the ones it is tested on, which it could never do in real use. So I learned from 2000 to 2019, 4,998 days, and tested on 2020 onwards, 1,683 days, exactly as the model would be used: past to learn, future to test.
</details>

<details>
<summary><b>How did you build the features, and which models did you try?</b></summary>

Every feature uses only what was known by the end of the day: today's change, the four changes before it, the gap to the 5-day and 20-day averages, and 20-day volatility. A logistic regression on scaled features scored 51.3% with an AUC of 0.537. Gradient boosting, a more powerful model, did no better: 51.2% and AUC 0.516. A stronger model cannot find a pattern that is not there.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/m4-rupee-forecast-reality-check).

[← All projects](../../README.md)
