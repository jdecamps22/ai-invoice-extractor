import { useState } from "react";

function App() {
  const [notes, setNotes] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  async function processDocument() {
    setLoading(true);
    setSummary("");

    try {
      const response = await fetch(
        "https://ai-invoice-extractor-izxj.onrender.com/process-document",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: notes,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setSummary(data.result);
      } else {
        setSummary("Error: " + data.error);
      }

    } catch (error) {
      setSummary("Failed to fetch: " + error.message);
    }

    setLoading(false);
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Study Tool</h1>

      <textarea
        rows="10"
        cols="50"
        placeholder="Paste your notes here..."
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />

      <br />

      <button onClick={processDocument} disabled={loading}>
        {loading ? "Processing..." : "Extract Insights"}
      </button>

      <h2>Result:</h2>

      <p>{summary}</p>
    </div>
  );
}

export default App;