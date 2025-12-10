// App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [responseType, setResponseType] = useState("");
  const [interactiveHtml, setInteractiveHtml] = useState("");
  const [codeContent, setCodeContent] = useState("");
  const [explanation, setExplanation] = useState("");
  const [source, setSource] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e && e.preventDefault();
    if (!query.trim()) return;
    setStatus("Loading...");
    setResponseType("");
    setInteractiveHtml("");
    setCodeContent("");
    setExplanation("");
    setSource("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/ask", { query });
      const data = res.data;
      if (data.type === "interactive") {
        setResponseType("interactive");
        setInteractiveHtml(data.html || "");
      } else if (data.type === "code") {
        setResponseType("code");
        setCodeContent(data.code || "");
        setExplanation(data.explanation || "");
        setSource((data.metadata && data.metadata.source) || "");
      } else {
        setStatus("Unknown response type from server.");
      }
    } catch (err) {
      console.error(err);
      setStatus("Error contacting server.");
    } finally {
      setStatus("");
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f1222",
      color: "#fff",
      fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
      padding: 24,
      display: "flex",
      flexDirection: "column",
      alignItems: "center"
    }}>
      <div style={{ width: "100%", maxWidth: 1000 }}>
        <h1 style={{ color: "#ffd54a" }}>DSA RAG + Interactive Demos</h1>

        <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., help me learn linked list OR give python code for stack"
            style={{
              flex: 1,
              padding: "12px 14px",
              borderRadius: 8,
              border: "1px solid #333",
              background: "#181825",
              color: "#fff"
            }}
          />
          <button type="submit" style={{
            padding: "12px 18px",
            background: "#ffd54a",
            border: "none",
            borderRadius: 8,
            cursor: "pointer"
          }}>
            Submit
          </button>
        </form>

        {status && <div style={{ color: "#ffd54a", marginBottom: 12 }}>{status}</div>}

        <div style={{
          background: "#11121a",
          borderRadius: 12,
          padding: 16,
          minHeight: 320,
          boxShadow: "0 8px 30px rgba(0,0,0,0.6)"
        }}>
          {responseType === "interactive" && interactiveHtml && (
            <div>
              <div style={{ color: "#ffd54a", marginBottom: 8 }}>Interactive demo (sandboxed)</div>
              <iframe
                title="interactive-demo"
                srcDoc={interactiveHtml}
                sandbox="allow-scripts allow-same-origin"
                style={{ width: "100%", height: 620, border: "1px solid #222", borderRadius: 8 }}
              />
              <div style={{ color: "#9aa0b4", marginTop: 8 }}>
                Note: iframe is sandboxed. If your HTML needs external assets from your server, consider serving it as a URL.
              </div>
            </div>
          )}

          {responseType === "code" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h3 style={{ color: "#ffd54a" }}>Code from Vector DB:</h3>
                {source && <div style={{ color: "#9aa0b4" }}>Source: {source}</div>}
              </div>

              <pre style={{
                background: "#0b0b0f",
                padding: 12,
                borderRadius: 8,
                overflowX: "auto",
                whiteSpace: "pre-wrap",
                color: "#dbe7ff",
                maxHeight: 420
              }}>{codeContent || "No code retrieved."}</pre>

              <h3 style={{ color: "#ffd54a", marginTop: 12 }}>Explanation (LLM):</h3>
              <div style={{ color: "#cfe2ff", background: "#0b0c12", padding: 12, borderRadius: 8 }}>
                {explanation || "No explanation available."}
              </div>
            </div>
          )}

          {!responseType && (
            <div style={{ color: "#9aa0b4" }}>
              Ask something to get an interactive demo or code + explanation.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
