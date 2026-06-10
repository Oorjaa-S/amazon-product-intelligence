import { useState } from "react";

function App() {

  const [review, setReview] = useState("");
  const [rating, setRating] = useState(null);

  const [productId, setProductId] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const [loadingPrediction, setLoadingPrediction] = useState(false);
  const [loadingRecommendation, setLoadingRecommendation] = useState(false);
  const [searched, setSearched] = useState(false);

  async function predictRating() {

    setLoadingPrediction(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict_rating",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            review: review
          })
        }
      );

      const data = await response.json();

      setRating(
        data.predicted_rating
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoadingPrediction(false);

    }
  }



  async function getRecommendations() {
    setSearched(true);

    setLoadingRecommendation(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/recommend",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            product_id: productId
          })
        }
      );

      const data = await response.json();

      setRecommendations(
        data.recommendations
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoadingRecommendation(false);

    }
  }

  return (
    <div className="container">

      <nav className="navbar">
        <div className="logo">
          Amazon AI
        </div>

        <div className="nav-links">
          <a href="#">
            Home
          </a>

          <a href="#tools">
            Tools
          </a>

          <a href="#about">
            About
          </a>
        </div>
      </nav>

      <section className="hero">

        <h1>
          Amazon Product
          <br />
          Intelligence Engine
        </h1>

        <p>
          AI-powered rating prediction and
          product recommendation system
          trained on 568K Amazon reviews.
        </p>

      </section>

      <section className="stats">

        <div className="stat-card">
          <h2>568K+</h2>
          <p>Reviews</p>
        </div>

        <div className="stat-card">
          <h2>74K+</h2>
          <p>Products</p>
        </div>

        <div className="stat-card">
          <h2>256K+</h2>
          <p>Users</p>
        </div>

        <div className="stat-card">
          <h2>75.6%</h2>
          <p>Accuracy</p>
        </div>

      </section>

      <section
        id="tools"
        className="tools"
      >

        <div className="card">

          <h2>⭐ Rating Prediction</h2>

          <textarea
            rows="8"
            value={review}
            onChange={(e) =>
              setReview(e.target.value)
            }
            placeholder="Paste review text..."
          />

          <button
            onClick={predictRating}
            disabled={loadingPrediction}
          >
            {
              loadingPrediction
                ? "Predicting..."
                : "Predict Rating"
            }
          </button>

          {rating && (
            <div className="result">

              <h3>Predicted Rating</h3>

              <div className="stars">
                {"⭐".repeat(rating)}
                {"☆".repeat(5 - rating)}
              </div>

            </div>
          )}

        </div>

        <div className="card">

          <h2>🛒 Product Recommendation</h2>

          <input
            type="text"
            value={productId}
            onChange={(e) =>
              setProductId(e.target.value)
            }
            placeholder="Enter Product ID"
          />

          <button
            onClick={getRecommendations}
            disabled={loadingRecommendation}
          >
            {
              loadingRecommendation
                ? "Finding Products..."
                : "Get Recommendations"
            }
          </button>

          <div className="recommendations">

            {
              searched &&
              (
                <h3>
                  Top 5 Similar Products
                </h3>
              )
            }

            {
              searched &&
              recommendations.length === 0 &&
              !loadingRecommendation &&
              (
                <p>
                  No matching product found.
                </p>
              )
            }

            {
              recommendations.map(
                (item, index) => (

                  <div
                    key={index}
                    className="recommendation-card"
                  >

                    <h4>
                      Product ID
                    </h4>

                    <p className="product-id">
                      {item.product_id}
                    </p>

                    <h5>
                      Representative Review
                    </h5>

                    <p>
                      {item.review_title}
                    </p>

                    <h5>
                      Similarity
                    </h5>

                    <p>
                      {(item.similarity_score * 100).toFixed(2)}%
                    </p>

                  </div>

                )
              )
            }

          </div>

        </div>

      </section>
      <footer className="footer">

        Built with

        <br />

        FastAPI • React • Scikit-Learn • TF-IDF

      </footer>

    </div>
  );
}

export default App;