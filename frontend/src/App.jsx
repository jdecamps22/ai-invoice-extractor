import { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState("");

  async function processDocument() {
    try {
      const response = await fetch("http://127.0.0.1:8000/process-document", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    }
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Invoice Processor</h1>

      <p>Extract structured invoice data instantly from documents</p>

      <textarea
        rows="12"
        cols="70"
        placeholder="Paste invoice or receipt here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        style={{ padding: "10px", fontSize: "14px" }}
      />

      <br /><br />

      <button
        onClick={processDocument}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Extract Invoice Data
      </button>

      <h2>Result:</h2>

      <pre
        style={{
          background: "#f5f5f5",
          padding: "15px",
          borderRadius: "8px",
          overflowX: "auto"
        }}
      >
        {result ? JSON.stringify(result, null, 2) : "No result yet"}
      </pre>
    </div>
  );
}

export default App;