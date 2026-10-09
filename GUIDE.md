# How to update your profile

Your profile page (github.com/abhishekvtiwari) is **built automatically** from one file: **`profile.yml`**. You never edit `README.md` directly. Change `profile.yml` (or upload a file), and about a minute later the page, the banner and the cards are rebuilt.

```
profile.yml   ──►  automatic rebuild (about 1 min)  ──►  README.md · banner · whoami card · stats · heatmap
resume/       ──►  the Résumé button
certificates/ ──►  links in "Achievements and certificates"
```

---

## How to edit, on github.com (phone or computer)

1. Open **github.com/abhishekvtiwari/abhishekvtiwari**.
2. Tap **`profile.yml`**, then the **pencil icon ✏️** (Edit).
3. Make your change. Keep the spaces at the start of each line exactly as they are.
4. Tap **Commit changes** (green button), then **Commit changes** again.
5. Wait about a minute, then refresh your profile. To watch it work: **Actions** tab → **Refresh profile** (yellow = running, green = done, red = see "If something goes wrong").

---

## What to change, and where

| You want to… | In `profile.yml`, change… | Example |
|---|---|---|
| Change your job title | `role:` | `role: Business Analyst · PMO (CEO's Office)` |
| Change your company | `company:` | `company: JJ Plastalloy` |
| Change the line under your name | `tagline:` | `tagline: I turn data into decisions.` |
| Rewrite "About me" | the lines under `about:` (each starts with `  - `) | `  - Led the monthly MIS for the CEO's office.` |
| Update email, LinkedIn or website | `email:` · `linkedin:` · `website:` | `email: you@example.com` |
| Add or remove a skill | the lists under `skills:` | `Data: [SQL, Python, Power BI, Tableau]` |
| Add a new skill group | a new line under `skills:` | `Tools: [Jira, Confluence]` |
| Show or hide Compounza | `compounza:` → `show:` | `show: false` hides it |
| Add, remove or reorder featured projects | the entries under `projects:` | see below |
| Add HackerRank stars or a certificate | `achievements:` | see below |

**Text with a colon ( : ) inside it must go in double quotes**, for example `tagline: "Data: decisions"`.

---

## Your résumé

**Best: upload the PDF to this repository.**
1. Open the **`resume`** folder → **Add file → Upload files**.
2. Upload your PDF, e.g. `Abhishek-Tiwari-Resume.pdf`, and commit.
3. In `profile.yml` set: `resume: resume/Abhishek-Tiwari-Resume.pdf`

**Or use a link:** `resume: "https://drive.google.com/…"` (quotes needed).
**To hide the button:** `resume: ""`

When you have a new version, upload it with the **same file name** and the button keeps working with no other change.

---

## HackerRank stars, certificates and courses

In `profile.yml`, replace `achievements: []` with entries like these:

```yaml
achievements:
  - title: HackerRank SQL
    detail: 5 stars
    link: https://www.hackerrank.com/profile/YOUR-USERNAME
  - title: HackerRank Python
    detail: 4 stars
    link: https://www.hackerrank.com/profile/YOUR-USERNAME
  - title: Google Data Analytics Certificate
    detail: Coursera, 2024
    link: certificates/google-data-analytics.pdf
```

- `link:` can be a web address **or** a file you uploaded to the **`certificates`** folder.
- The **🏆 Achievements and certificates** section appears on its own as soon as there is at least one entry.

---

## Featured projects

Each project in `profile.yml`:

```yaml
  - name: IPL Performance Dashboard        # shown in bold, links to the repository
    repo: Power-BI-IPL                     # the repository name after github.com/abhishekvtiwari/
    what: Team win rates, run rate over time and batsman trends
    stack: Power BI · DAX
```

The order in the file is the order on the page. To remove one, delete its 4 lines.

---

## What updates by itself

| Thing | When |
|---|---|
| Contribution heatmap and stats card | **Every morning at 06:00 India time**, from your public contribution calendar |
| Everything else | **Whenever you change `profile.yml`, `resume/` or `certificates/`** |
| Run it now | **Actions** tab → **Refresh profile** → **Run workflow** |

**Your private work can count too.** GitHub → **Settings → Public profile → Contributions & activity → tick "Include private contributions on my profile"**. Only the number of contributions is shown, never what they were.

---

## If something goes wrong

- **The Actions run is red:** almost always a spacing or quotes mistake in `profile.yml`. Open the run, read the last lines, fix that line in `profile.yml` and commit again. Your previous profile stays online until the fix.
- **A picture didn't change:** GitHub caches images for a few minutes. Wait, then hard-refresh (Ctrl + F5).
- **Undo a change:** open `profile.yml` → **History** → pick the earlier version → copy it back.

---

## Files in this repository

| File | What it is | Edit it? |
|---|---|---|
| `profile.yml` | Everything on your profile | **Yes, this is the one** |
| `resume/` | Your résumé PDF | Upload into it |
| `certificates/` | Certificate files | Upload into it |
| `GUIDE.md` | This guide | No need |
| `README.md` | The page itself, rebuilt from `profile.yml` | **No**, your edits would be overwritten |
| `assets/` | Banner, cards, heatmap, logo (rebuilt automatically) | No |
| `scripts/build_profile.py` | The program that builds the page | No |
| `.github/workflows/profile.yml` | The schedule that runs it | No |
