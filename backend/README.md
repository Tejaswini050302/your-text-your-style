# Backend - Your Text Your Style

FastAPI backend that:
- Accepts text + .pptx template
- Calls LLM (OpenAI) for slide outline
- Generates new presentation reusing template style

Run locally:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

---

## 🔹 Frontend

### `frontend/src/App.jsx`
```jsx
import UploadForm from "./components/UploadForm";

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-lg">
        <h1 className="text-xl font-bold mb-4">Your Text → Your Style</h1>
        <UploadForm />
      </div>
    </div>
  );
}
