# Credit_Card_Fraud_Detection
# Credit Card Fraud Detection — End-to-End MLOps Pipeline

## Project Overview

This is a hands-on MLOps learning and portfolio project focused on building a reproducible pipeline to detect fraudulent credit card transactions. It follows my [House Prices MLOps project](https://github.com/kumarjukanti/house-prices-advanced-regression-techniques/blob/main/README.md) and applies the same engineering workflow to a rare-event classification problem.

**Project status** · Initial planning. The pipeline, model training, and deployment are planned.

## Machine Learning Problem

Credit card fraud detection is a supervised binary classification problem. The model will assign each transaction a fraud score. A decision threshold will determine which transactions are flagged for review.

Lowering the threshold can catch more fraud and increase the number of legitimate transactions flagged. The project will report both effects so that the threshold can be evaluated against a review capacity or an acceptable false-alert rate.

## Kaggle Dataset

The dataset contains 284,807 transactions made by European cardholders over two days in September 2013. Of these, 492 are labeled fraudulent, approximately 0.172% of all transactions. The labeled data is provided in a single file, `creditcard.csv`. [Kaggle dataset and data dictionary](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data)

| Field | Description |
| --- | --- |
| `V1`–`V28` | Anonymized principal components |
| `Time` | Seconds elapsed since the first transaction in the dataset |
| `Amount` | Transaction amount |
| `Class` | Target label, with `1` for fraud and `0` for legitimate transactions |

The dataset was collected and analyzed through a collaboration between Worldline and the Machine Learning Group at Université Libre de Bruxelles. [Dataset acknowledgments and citations](https://www.kaggle.com/mlg-ulb/creditcardfraud/)

## Model Evaluation

- **Primary metric** · Use average precision (AP) to summarize the precision–recall curve. Kaggle recommends precision–recall evaluation for this dataset. [Kaggle dataset guidance](https://www.kaggle.com/mlg-ulb/creditcardfraud/)
- **Operating threshold** · Use validation data to choose a threshold and report precision, recall, and the confusion matrix at that threshold.
- **Final evaluation** · Evaluate the selected model and threshold on a held-out test set with the original fraud prevalence. Report the transaction and fraud counts for each split.
- **Time-based evaluation** · Assess whether a chronological holdout has enough fraud cases for a meaningful estimate and use it to check how a model trained on earlier transactions performs on later ones.

A classifier that labels every transaction legitimate would achieve about 99.83% accuracy while catching zero fraud cases.

## Technology Stack

| Area | Planned tools |
| --- | --- |
| Programming and environment | Python, uv |
| Data processing and visualization | pandas, NumPy, Matplotlib, Seaborn |
| Modeling | scikit-learn |
| Source control and testing | Git, GitHub, pytest |
| Data and pipeline versioning | DVC, Amazon S3 |
| Experiment tracking | MLflow |
| Model serving and packaging | FastAPI, Docker |
| Container registry and deployment | Amazon ECR, Kubernetes on Amazon EKS |
| CI/CD | GitHub Actions |

## MLOps Architecture

```text
Kaggle CSV → DVC (S3 remote) → Data validation → Train / validation / test split
  → Preprocessing and training → Evaluation and threshold selection
  → Model package → FastAPI → Docker → Amazon ECR → Amazon EKS
```

MLflow will record the dataset version, Git commit, split configuration, model parameters, metrics, threshold, and artifacts. GitHub Actions will run tests, build the image, push it to Amazon ECR, and verify the deployment on Amazon EKS.

## Implementation Progress

| Phase | Status | Scope |
| --- | --- | --- |
| 1. Data ingestion and validation | Planned | Download the CSV and check column names, types, missing values, duplicate rows, and valid class labels. |
| 2. Exploratory data analysis | Planned | Inspect class balance, transaction amounts, and fraud counts over time. |
| 3. Model training | Planned | Establish a logistic regression baseline and compare class weighting and tree-based models. |
| 4. Evaluation and threshold selection | Planned | Compare precision–recall curves and select a review threshold using validation data. |
| 5. Reproducible pipelines | Planned | Define DVC stages, configure the S3 remote, and log runs in MLflow. |
| 6. Model packaging and serving | Planned | Package preprocessing, the classifier, and the threshold together. Add prediction and health endpoints in FastAPI and build a Docker image. |
| 7. Deployment and CI/CD | Planned | Run pytest in GitHub Actions, publish commit-tagged images to ECR, and verify deployment on EKS. |
| 8. Monitoring | Planned | Track service health, input drift, score distributions, and alert volume. Measure precision and recall when confirmed labels become available. |

## Data Quality and Leakage

- Inspect repeated rows before deciding how to handle them. The anonymized schema has no transaction identifier, so identical rows alone cannot establish that two records represent the same transaction.
- Create the evaluation splits before fitting preprocessing or applying any resampling. During cross-validation, fit these steps within each training fold.
- Use validation results to select the model and threshold, then apply both as selected to the held-out test set.

## Project Structure

The planned layout follows the house-prices project.

```text
Credit_Card_Fraud_Detection/
├── .github/workflows/      # CI and deployment
├── data/raw/               # Local Kaggle download
├── notebooks/              # Exploratory analysis and experiments
├── src/
│   ├── data/               # Ingestion and validation
│   ├── features/           # Preprocessing
│   ├── models/             # Training, evaluation, and inference
│   └── api/                # FastAPI service
├── tests/
├── deployment/kubernetes/
├── dvc.yaml
├── params.yaml
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Getting Started

1. Download [`creditcard.csv` from Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data).
2. From the repository root, run `mkdir -p data/raw` and place the extracted file at `data/raw/creditcard.csv`.
3. Keep the raw CSV out of Git commits. DVC tracking is planned for the data pipeline.

## Current Limitations

The dataset covers two days, which limits what a holdout can tell us about changes in fraud patterns over time. The original inputs behind the PCA features are unavailable, so the planned API will serve records in the Kaggle feature schema. Scoring raw transactions would require access to compatible feature transformations.

## Project Goal

Build a fraud detection pipeline that can reproduce a training run, explain why a transaction was flagged at a given threshold, and trace a deployed model back to the code, data, and evaluation that produced it.
