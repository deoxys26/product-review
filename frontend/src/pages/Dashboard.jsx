import { useEffect, useState } from "react";
import { getStats, getAspectStats, getReviews } from "../services/api";

import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [aspects, setAspects] = useState([]);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const statsRes = await getStats();
      const aspectRes = await getAspectStats();
      const reviewsRes = await getReviews();

      setStats(statsRes.data);

      const aspectData = Object.entries(aspectRes.data).map(
        ([name, count]) => ({
          name,
          count,
        })
      );

      setAspects(aspectData);
      setReviews(reviewsRes.data.slice(-10).reverse());
    } catch (error) {
      console.error(error);
    }
  };

  const pieData = stats
    ? [
        { name: "Positive", value: stats.positive },
        { name: "Negative", value: stats.negative },
      ]
    : [];

  return (
    <div className="card">
      <h1>Review Intelligence Dashboard</h1>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Reviews</h3>
            <p>{stats.total}</p>
          </div>

          <div className="stat-card">
            <h3>Positive</h3>
            <p>{stats.positive}</p>
          </div>

          <div className="stat-card">
            <h3>Negative</h3>
            <p>{stats.negative}</p>
          </div>
        </div>
      )}

      <div className="charts-grid">
        <div className="chart-card">
          <h2>Sentiment Distribution</h2>

          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                outerRadius={90}
                label
              >
                {pieData.map((entry, index) => (
                  <Cell key={index} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Top Mentioned Aspects</h2>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={aspects}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <h2>Recent Reviews</h2>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Review</th>
              <th>Sentiment</th>
              <th>Confidence</th>
            </tr>
          </thead>

          <tbody>
            {reviews.map((review) => (
              <tr key={review.id}>
                <td>{review.review_text}</td>
                <td>{review.sentiment}</td>
                <td>{(review.confidence * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;