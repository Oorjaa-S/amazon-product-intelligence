from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib

from schemas import (
    ReviewRequest,
    ProductRequest
)

from recommendation import (
    recommend_products
)

# ==========================
# FastAPI App
# ==========================

app = FastAPI(
    title="Amazon Product Intelligence Engine",
    description="Rating Prediction and Product Recommendation API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Load Model & Vectorizer
# ==========================

model = joblib.load(
    "models/best_rating_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)

# ==========================
# Health Check
# ==========================

@app.get("/health")
def health():

    return {
        "status": "running"
    }

# ==========================
# Rating Prediction
# ==========================

@app.post("/predict_rating")
def predict_rating(
    request: ReviewRequest
):

    review = request.review

    review_vector = vectorizer.transform(
        [review]
    )

    prediction = model.predict(
        review_vector
    )[0]

    return {
        "review": review,
        "predicted_rating": int(prediction)
    }

# ==========================
# Product Recommendation
# ==========================

@app.post("/recommend")
def recommend(
    request: ProductRequest
):

    recommendations = recommend_products(
        request.product_id
    )

    return {
        "product_id": request.product_id,
        "recommendations": recommendations
    }