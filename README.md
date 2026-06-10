| Model                                |   Accuracy |
| ------------------------------------ | ---------: |
| Logistic Regression (Text)           |     73.91% |
| Logistic Regression (Summary + Text) | **75.62%** |
| Linear SVM                           |     71.43% |
| Multinomial Naive Bayes              |     66.25% |
## Dataset

The dataset used for this project is the Amazon Product Reviews dataset from Kaggle.

Due to GitHub file size limitations, the processed dataset is not included in this repository.

To recreate the dataset:

1. Install dependencies from `requirements.txt`
2. Run `preprocess.py`
3. The cleaned dataset will be generated automatically inside `backend/processed_data/`
