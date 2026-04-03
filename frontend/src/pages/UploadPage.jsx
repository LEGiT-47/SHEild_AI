import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import Upload from "../components/Upload";
import { analyzeFile } from "../services/api";

function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [logs, setLogs] = useState([]);

  const caseId = useMemo(
    () => `CASE-${Math.random().toString(16).slice(2, 10).toUpperCase()}`,
    [file]
  );

  const pushLogsSequentially = () => {
    const lines = [
      "[init] Opening case file...",
      "[scan] Extracting visual regions...",
      "[signal] Running edge and blur diagnostics...",
      "[trace] Building source propagation map...",
      "[done] Finalizing forensic verdict...",
    ];
    lines.forEach((line, idx) => {
      setTimeout(() => {
        setLogs((prev) => [...prev, line]);
      }, idx * 300);
    });
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) setFile(dropped);
  };

  const onAnalyze = async () => {
    if (!file) {
      setError("Please upload a file before analysis.");
      return;
    }

    try {
      setError("");
      setLogs([]);
      setIsAnalyzing(true);
      pushLogsSequentially();
      const result = await analyzeFile(file);
      navigate("/result", { state: { ...result, uploadedFile: file.name, preview: URL.createObjectURL(file) } });
    } catch (err) {
      setError(err?.response?.data?.detail || "Analysis failed. Ensure backend services are running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="content-layer mx-auto max-w-5xl px-6 py-12">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="font-display text-5xl text-sheild-paper">Open Case File</h1>
        <p className="font-mono text-xs tracking-[0.2em] text-sheild-paper/70">{caseId}</p>
      </div>

      <section className="relative border border-sheild-mid bg-sheild-card p-6">
        <div className="absolute left-5 top-4 flex items-center gap-2 font-mono text-xs text-sheild-red">
          <span className="h-2 w-2 animate-pulse rounded-full bg-sheild-red" />
          LIVE
        </div>
        <div className="mb-6 mt-6">
          <Upload
            isDragging={isDragging}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={onDrop}
            onSelect={setFile}
          />
        </div>

        {file && (
          <div className="mb-4 border border-sheild-mid bg-black/40 p-4 font-mono text-xs text-sheild-paper/80">
            <p>FILE: {file.name}</p>
            <p>SIZE: {(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <p>CASE OPENED: {new Date().toLocaleString()}</p>
          </div>
        )}

        <button
          onClick={onAnalyze}
          disabled={isAnalyzing}
          className="border border-white bg-sheild-red px-8 py-3 font-display text-2xl tracking-[0.18em] text-white disabled:opacity-60"
        >
          {isAnalyzing ? "ANALYZING..." : "ANALYZE"}
        </button>

        {error && <p className="mt-4 font-mono text-sm text-red-400">{error}</p>}

        {isAnalyzing && (
          <div className="mt-6 border border-sheild-mid bg-black p-4">
            {logs.map((line, idx) => (
              <p key={`${line}-${idx}`} className="font-mono text-xs text-sheild-cyan">
                {line}
              </p>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default UploadPage;
