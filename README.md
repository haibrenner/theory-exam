# Theory Exam Practice

Practice app for the Israeli driving theory exam, built from the official question pool (data.gov.il, Ministry of Transport), in Hebrew, English and Arabic.

**Live site:** https://haibrenner.github.io/theory-exam/

> **Disclaimer:** This site is based on the official question pool of the Israeli Ministry of Transport and Road Safety, published on data.gov.il, but it is not operated by the government and its content has not been fully verified. Copyright in the question pool belongs to the State of Israel. The pool is used in accordance with the terms of use and the open license under which it was published, with attribution to the source, as fair use, and without changing the questions and answers. The data is current as of October 10, 2026. The site is free to use.

## Files

| File | Purpose |
|---|---|
| `theory_questions.txt` / `theory_answers.txt` | Hebrew question pool (1802 questions) and correct answers |
| `theory_questions_en.txt` / `theory_answers_en.txt` | English pool, same questions and numbering |
| `theory_questions_ar.txt` / `theory_answers_ar.txt` | Arabic pool, same questions and numbering |
| `build.py` | Parses the text files into `data_he.js`, `data_en.js`, `data_ar.js` |
| `data_*.js` | Generated question data, one file per language, loaded on demand by the page |
| `index.html` | The app (plain HTML/CSS/JS, no dependencies) |

The Hebrew pool is the master: the English and Arabic files use its question list, topics, license tags and image links. Each language keeps its own question text, answer order and correct answer. Arabic questions 673 and 1357 are missing from the official Arabic dataset, so they appear in Hebrew.

## Updating the questions

Edit the text files, then run:

```
python3 build.py
```

This regenerates the `data_*.js` files and updates their cache-busting versions in `index.html`. Commit and push; GitHub Pages redeploys automatically.

To use the app offline, open `index.html` directly in a browser (images still need internet).
