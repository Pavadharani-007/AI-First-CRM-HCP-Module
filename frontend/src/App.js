import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    hcp_name: "",
    date: "",
    sentiment: "",
    product: "",
    brochure: false,
  });

  const [summary, setSummary] = useState("");
  const [insight, setInsight] = useState("");
  const [history, setHistory] = useState([]);

  // ---------------- SEND MESSAGE ----------------
  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: message,
      });

      console.log("FULL RESPONSE:", res.data);

      // 🔥 SAFE MERGE (prevents overwriting issues)
      setForm((prev) => ({
        ...prev,
        ...res.data.form_data,
      }));

      setSummary(res.data.summary || "");
      setInsight(res.data.insight || "");

      setHistory((prev) => [
        ...prev,
        {
          text: message,
          response: res.data.form_data || {},
        },
      ]);

      setMessage("");
    } catch (err) {
      console.log(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  // ---------------- UPDATE INTERACTION ----------------
  const updateInteraction = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/edit", form);

      console.log("EDIT RESPONSE:", res.data);

      // 🔥 SAFE MERGE instead of full replace
      setForm((prev) => ({
        ...prev,
        ...res.data,
      }));
    } catch (err) {
      console.log(err);
      alert("Update failed");
    }
  };

  return (
    <div className="container">

      {/* LEFT SIDE */}
      <div className="left">
        <h2>HCP Interaction Form</h2>

        <div className="card">

          <input
            value={form.hcp_name}
            placeholder="HCP Name"
            onChange={(e) =>
              setForm({ ...form, hcp_name: e.target.value })
            }
          />

          <input
            value={form.date}
            placeholder="Date"
            onChange={(e) =>
              setForm({ ...form, date: e.target.value })
            }
          />

          <select
            value={form.sentiment}
            onChange={(e) =>
              setForm({ ...form, sentiment: e.target.value })
            }
          >
            <option value="">Select Sentiment</option>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>

          <input
            value={form.product}
            placeholder="Product"
            onChange={(e) =>
              setForm({ ...form, product: e.target.value })
            }
          />

          <label>
            <input
              type="checkbox"
              checked={form.brochure}
              onChange={(e) =>
                setForm({ ...form, brochure: e.target.checked })
              }
            />
            Brochure Given
          </label>

          <button className="btn" onClick={updateInteraction}>
            Update Interaction
          </button>
        </div>

        {/* SUMMARY */}
        <div className="card">
          <h3>Summary</h3>
          <p>{summary || "-"}</p>
        </div>

        {/* INSIGHT */}
        <div className="card">
          <h3>Insight</h3>
          <p>{insight || "-"}</p>
        </div>
      </div>

      {/* RIGHT SIDE */}
      <div className="right">
        <h2>AI Chat Assistant</h2>

        {/* CHAT HISTORY */}
        <div className="history">
          {history.map((item, index) => (
            <div key={index} className="historyItem">
              <b>You:</b> {item.text}
              <br />
              <small>
                → {item.response?.hcp_name || "No Name"} |{" "}
                {item.response?.sentiment || "N/A"}
              </small>
            </div>
          ))}
        </div>

        <textarea
          className="chatBox"
          placeholder="Type interaction like: I met Dr Smith, positive, gave brochure"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button
          className="btn"
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? "Processing..." : "Send"}
        </button>
      </div>

    </div>
  );
}

export default App;