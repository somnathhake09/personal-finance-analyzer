# Personal Finance Analyzer

A command-line personal finance tracker built in Python, developed as part of a structured Python → Data Analysis learning journey. The project evolves version by version as new concepts (functions, file handling, OOP, and eventually NumPy/Pandas) are learned and applied.

## Features (current version — v5)

- Add and track expense transactions interactively
- Automatic classification of expenses as Essential / Discretionary / Unknown
- Persistent storage using JSON — data survives between runs
- Monthly summary: total spent, remaining balance, % of income spent
- Category-wise spending breakdown with highest-spending category detection
- Input validation and error handling (invalid amounts, empty fields)
- Built using Object-Oriented Programming (`Transaction` and `FinanceTracker` classes)

## Tech Stack

- Python 3
- `json` — data persistence
- `pathlib` — file path handling

## How to Run

```bash
python Finance_Tracker.py
```

Follow the prompts to enter your monthly income and transactions. Type `done` when finished entering transactions to see your summary.

## Project Roadmap

This project is being built incrementally as part of a Python-to-Data-Analysis curriculum:

- [x] v1–v3: Core Python (variables, loops, data structures, functions)
- [x] v4: File handling with JSON persistence
- [x] v5: Object-Oriented Programming refactor
- [ ] v6: NumPy integration
- [ ] v7: Pandas integration
- [ ] v8: Data cleaning on real financial data
- [ ] v9: Exploratory Data Analysis (EDA)
- [ ] v10: Data visualization (Matplotlib/Seaborn) + final portfolio version

## Author

Built by [somnathhake09](https://github.com/somnathhake09) as a hands-on learning project on the path toward a Data Analyst role.