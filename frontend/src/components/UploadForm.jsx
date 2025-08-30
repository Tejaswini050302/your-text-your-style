import { useState } from "react";

export default function UploadForm() {
  const [text, setText] = useState("");
  const [guidance, setGuidance] = useState("");
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [template, setTemplate] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("text", text);
    formData.append("guidance", guidance);
    formData.append("provider", provider);
    formData.append("api_key", apiKey);
    formData.append("template", template);

    const resp = await fetch("http://localhost:8000/generate-pptx/", {
      method: "POST",
      body: formData,
    });

    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated.pptx";
    a.click();

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <textarea
        className="w-full border p-2 rounded"
        placeholder="Paste your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        required
      />
      <input
        className="w-full border p-2 rounded"
        placeholder="Optional guidance..."
        value={guidance}
        onChange={(e) => setGuidance(e.target.value)}
      />
      <select
        className="w-full border p-2 rounded"
        value={provider}
        onChange={(e) => setProvider(e.target.value)}
      >
        <option value="openai">OpenAI</option>
      </select>
      <input
        className="w-full border p-2 rounded"
        placeholder="Your API key"
        type="password"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        required
      />
      <input
        className="w-full"
        type="file"
        accept=".pptx,.potx"
        onChange={(e) => setTemplate(e.target.files[0])}
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-500 text-white p-2 rounded"
      >
        {loading ? "Generating..." : "Generate Presentation"}
      </button>
    </form>
  );
}
