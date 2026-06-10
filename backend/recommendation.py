import pandas as pd
import kagglehub
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================
# Load Dataset
# ==========================

path = kagglehub.dataset_download(
    "arhamrumi/amazon-product-reviews"
)

df = pd.read_csv(
    os.path.join(path, "Reviews.csv")
)

# ==========================
# Create Product Documents
# ==========================

product_reviews = (
    df.groupby("ProductId")["Text"]
    .apply(lambda x: " ".join(x.astype(str)))
    .reset_index()
)

product_names = (
    df.groupby("ProductId")["Summary"]
    .first()
)

# ==========================
# TF-IDF
# ==========================

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000
)

tfidf_matrix = vectorizer.fit_transform(
    product_reviews["Text"]
)

# ==========================
# Recommendation Function
# ==========================

def recommend_products(product_id, top_n=5):

    matches = product_reviews[
        product_reviews["ProductId"] == product_id
    ]

    if matches.empty:
        return []

    idx = matches.index[0]

    similarities = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    similar_indices = similarities.argsort()[-(top_n + 10):][::-1]

    recommendations = []

    for i in similar_indices:

        if i == idx:
            continue

        pid = product_reviews.iloc[i]["ProductId"]

        recommendations.append(
            {
                "product_id": pid,
                "review_title": product_names.get(
                    pid,
                    "Unknown Product"
                ),
                "similarity_score": round(
                    float(similarities[i]),
                    4
                )
            }
        )

        if len(recommendations) == top_n:
            break

    return recommendations


# ==========================
# Test
# ==========================

if __name__ == "__main__":

    print("Dataset Shape:", df.shape)
    print(
        "Unique Products:",
        len(product_reviews)
    )

    sample_product = (
        product_reviews["ProductId"]
        .iloc[0]
    )

    print("\nSample Product:")
    print(sample_product)

    print("\nRecommendations:\n")

    for rec in recommend_products(
        sample_product
    ):
        print(rec)