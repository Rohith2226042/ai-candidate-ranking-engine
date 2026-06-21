# AI Candidate Ranking Engine

An intelligent AI-powered candidate ranking system built for the India.Runs Data & AI Challenge.

## Problem

Traditional ATS systems rely heavily on keyword matching, often missing highly relevant candidates due to semantic differences.

This system solves that using:

* Semantic embeddings
* Behavioral scoring
* Trap detection
* Weighted ranking
* Reasoning generation

## Architecture

Job Description → Candidate Dataset → Parser → Feature Engineering → Semantic Ranking → Behavior Scoring → Trap Detection → Final Ranking → Export

## Tech Stack

* Python
* FastAPI
* SentenceTransformers
* Scikit-learn
* JSONL dataset
* CSV Export

## Features

* Candidate semantic ranking
* Skill scoring
* Experience scoring
* Behavioral analysis
* Honeypot detection
* API endpoint support

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```

## API Run

```bash
python -m uvicorn api:app --reload
```

Swagger Docs:

http://127.0.0.1:8000/docs

## Output

* outputs/submission.csv

## Validation

```bash
python validate_submission.py outputs/submission.csv
```

Status:
Submission Valid
