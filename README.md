# Theory Exam Practice

Practice app for the Israeli driving theory exam, built from the official question pool (data.gov.il, Ministry of Transport).

**Live site:** https://haibrenner.github.io/theory-exam/

## Files

| File | Purpose |
|---|---|
| `theory_questions.txt` | Full question pool (1802 questions), each tagged with topic and license types |
| `theory_answers.txt` | Correct answer for every question |
| `build.py` | Parses the two text files into `data.js` |
| `data.js` | Generated question data loaded by the page |
| `index.html` | The app (plain HTML/CSS/JS, no dependencies) |

## Updating the questions

Edit the text files, then run:

```
python3 build.py
```

This regenerates `data.js` and updates its cache-busting version in `index.html`. Commit and push; GitHub Pages redeploys automatically.

To use the app offline, open `index.html` directly in a browser (images still need internet).
