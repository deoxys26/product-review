import { useState } from "react";
import { predictSentiment } from "../services/api";

function Analyzer() {
  const [review, setReview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!review.trim()) {
      alert("Please enter a review");
      return;
    }

    try {
      setLoading(true);
      const response = await predictSentiment(review);
      setResult(response.data);
      setReview("");
    } catch (error) {
      console.error(error);
      alert("Backend error. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1>AI Product Review Analyzer</h1>
      <p className="subtitle">
        Analyze customer reviews using a fine-tuned DistilBERT model.
      </p>

      <textarea
        rows="5"
        placeholder="Example: Battery life is amazing but heating is terrible..."
        value={review}
        onChange={(e) => setReview(e.target.value)}
      />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Review"}
      </button>

      {result && (
        <div className="result-box">
          <h2>{result.sentiment}</h2>

          <p>
            Confidence:{" "}
            <strong>{(result.confidence * 100).toFixed(2)}%</strong>
          </p>

          <h3>Detected Aspects</h3>

          {result.aspects && result.aspects.length > 0 ? (
            <div className="aspect-list">
              {result.aspects.map((aspect, index) => (
                <span className="aspect-pill" key={index}>
                  {aspect}
                </span>
              ))}
            </div>
          ) : (
            <p>No specific aspects detected.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Analyzer;