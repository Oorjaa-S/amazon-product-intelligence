import pandas as pd
import kagglehub
import os
import re


# ==========================
# Text Cleaning Function
# ==========================

def clean_text(text):
    text = str(text)

    # lowercase
    text = text.lower()

    # remove html tags
    text = re.sub(r"<.*?>", " ", text)

    # remove urls
    text = re.sub(r"http\S+|www\S+", " ", text)

    # remove non-alphanumeric characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ==========================
# Load Dataset
# ==========================

path = kagglehub.dataset_download(
    "arhamrumi/amazon-product-reviews"
)

df = pd.read_csv(
    os.path.join(path, "Reviews.csv")
)

print(f"\nOriginal Shape: {df.shape}")


# ==========================
# Remove Missing Values
# ==========================

df = df.dropna(subset=["Text", "Score"])

print(f"After Null Removal: {df.shape}")


# ==========================
# Remove Duplicate Reviews
# ==========================

df = df.drop_duplicates(
    subset=["UserId", "ProductId", "Text"]
)

print(f"After Duplicate Removal: {df.shape}")


# ==========================
# Remove Very Short Reviews
# ==========================

df = df[
    df["Text"].astype(str).str.len() > 20
]

print(f"After Short Review Removal: {df.shape}")


# ==========================
# Feature Engineering
# ==========================

# review length feature
df["review_length"] = (
    df["Text"]
    .astype(str)
    .apply(len)
)

# clean review text
df["clean_text"] = (
    df["Text"]
    .apply(clean_text)
)

# handle missing summaries
df["Summary"] = (
    df["Summary"]
    .fillna("")
)

# combined feature used by model
df["combined_text"] = (
    df["Summary"].astype(str)
    + " "
    + df["Text"].astype(str)
)

print("\nSample Processed Reviews:\n")

print(
    df[
        [
            "Summary",
            "Text",
            "clean_text",
            "combined_text"
        ]
    ].head()
)


# ==========================
# Save Processed Dataset
# ==========================

os.makedirs(
    "processed_data",
    exist_ok=True
)

df.to_csv(
    "processed_data/amazon_reviews_cleaned.csv",
    index=False
)

print(
    "\nCleaned dataset saved to:"
)

print(
    "processed_data/amazon_reviews_cleaned.csv"
)

print(
    "\nFinal Shape:",
    df.shape
)