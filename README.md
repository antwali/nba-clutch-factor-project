# nba-clutch-factor-project

# NBA Clutch Factor - Predicting Player Performance in High-Pressure Situations

## Project Overview

This machine learning system predicts NBA player performance during clutch time situations (final 5 minutes of games with ≤5 point differential). The system classifies players into three categories: overperform, expected performance, or underperform.

## Features

- Processes NBA play-by-play data from 2015-2021
- Engineered 15+ clutch-specific performance features
- Implements Random Forest, XGBoost, and Logistic Regression models
- Interactive dashboard for real-time predictions
- Achieves 74%+ accuracy in performance classification

## Technology Stack

- **Python 3.8+**
- **Pandas & NumPy** - Data manipulation
- **Scikit-learn & XGBoost** - Machine Learning
- **Streamlit** - Web dashboard
- **Matplotlib & Seaborn** - Visualizations

## Installation

### Prerequisites

- Python 3.8 or higher
- 2GB+ RAM
- 1GB+ storage space

### Setup

1. Clone this repository:

```bash
git clone https://github.com/YOUR-USERNAME/nba-clutch-factor.git
cd nba-clutch-factor
```

### Reference

Dataset source: https://www.kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019?resource=download

### Dashboard Demo:

![alt text](<Screenshot 2025-08-02 at 2.56.20 PM.png>)

### FolderStructure:

nba-clutch-factor-project/
│ README.md
│ requirements.txt
│ pyproject.toml # if present; otherwise ignore
│ .env.example # if used
│
├─ data/
│ ├─ raw/ # unmodified source CSV/JSON
│ ├─ interim/ # intermediate cleaned files
│ └─ processed/ # final training-ready datasets
│
├─ src/
│ ├─ config.py # paths, constants, seed
│ ├─ utils/ # small helpers (io, metrics, timing)
│ ├─ data/ # ingestion + cleaning modules
│ ├─ features/ # feature engineering
│ ├─ models/ # training, tuning, inference
│ └─ evaluation/ # evaluation + reporting
│
├─ notebooks/
│ ├─ 01_eda.ipynb
│ ├─ 02_feature_checks.ipynb
│ └─ 03_error_analysis.ipynb
│
└─ scripts/
├─ make_dataset.py
├─ build_features.py
├─ train_model.py
└─ evaluate.py
