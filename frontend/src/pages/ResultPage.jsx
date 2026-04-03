import { motion } from "framer-motion";
import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ActionPanel from "../components/ActionPanel";
import AnalysisPanel from "../components/AnalysisPanel";
import ResultCard from "../components/ResultCard";
import RiskMeter from "../components/RiskMeter";
import TracePanel from "../components/TracePanel";
import { generateReport } from "../services/api";
import { getRiskColor } from "../utils/riskUtils";

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state;

  const [complaint, setComplaint] = useState("");
  const [renderedComplaint, setRenderedComplaint] = useState("");

  useEffect(() => {
    if (!data) navigate("/upload");
  }, [data, navigate]);

  useEffect(() => {
    if (!complaint) return;
    let index = 0;
    const id = setInterval(() => {
      index += 1;
      setRenderedComplaint(complaint.slice(0, index));
      if (index >= complaint.length) clearInterval(id);
    }, 8);
    return () => clearInterval(id);
  }, [complaint]);

  const verdictStyle = useMemo(
    () =>
      data?.is_fake
        ? "border-red-500 shadow-[0_0_20px_rgba(192,57,43,0.65)]"
        : "border-green-500 shadow-[0_0_20px_rgba(46,204,113,0.55)]",
    [data]
  );

  if (!data) return null;

  const requestComplaint = async () => {
    const response = await generateReport({
      case_id: data.case_id,
      verdict: data.verdict,
      risk_level: data.risk_level,
      artifacts: data.artifacts,
      victim_name: "[Victim Name]",
      platform: data.traceability?.[0]?.source || "Unknown",
    });
    setComplaint(response.complaint_text || "No complaint text generated.");
  };

  return (
    <main className="content-layer mx-auto max-w-6xl space-y-8 px-6 py-10">
      <section className="grid gap-6 md:grid-cols-2">
        <div className={`overflow-hidden border-2 p-2 ${verdictStyle}`}>
          {data.preview ? (
            <img src={data.preview} alt="uploaded evidence" className="h-full max-h-[360px] w-full object-cover" />
          ) : (
            <div className="flex h-[300px] items-center justify-center bg-black/50 font-mono text-sm">
              Preview unavailable
            </div>
          )}
        </div>
        <div className="space-y-4">
          <motion.div
            initial={{ scale: 0, rotate: -15 }}
            animate={{ scale: 1, rotate: -3 }}
            transition={{ type: "spring", stiffness: 200 }}
            className={`inline-block border-2 px-5 py-4 font-display text-5xl ${
              data.is_fake ? "border-sheild-red text-sheild-red" : "border-sheild-green text-sheild-green"
            }`}
          >
            {data.is_fake ? "DEEPFAKE DETECTED" : "VERIFIED AUTHENTIC"}
          </motion.div>

          <ResultCard verdict={data.verdict} caseId={data.case_id} analyzedAt={data.analyzed_at} />
          <RiskMeter confidence={data.confidence} riskLevel={data.risk_level} />
          <span className={`inline-block border px-3 py-1 font-mono text-xs ${getRiskColor(data.risk_level)}`}>
            {data.risk_level}
          </span>
        </div>
      </section>

      <AnalysisPanel artifacts={data.artifacts || []} />
      <TracePanel traceability={data.traceability || []} />
      <ActionPanel actionSteps={data.action_steps || []} riskLevel={data.risk_level} />

      <section className="border border-sheild-mid bg-black/50 p-5">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="font-display text-3xl">Complaint Draft</h3>
          <button
            onClick={requestComplaint}
            className="border border-white bg-sheild-red px-4 py-2 font-mono text-xs uppercase tracking-[0.15em]"
          >
            Generate
          </button>
        </div>

        <textarea
          value={renderedComplaint}
          readOnly
          rows={14}
          className="w-full border border-sheild-mid bg-[#0d0d0d] p-3 font-mono text-xs text-sheild-paper"
        />
        <button
          onClick={() => navigator.clipboard.writeText(renderedComplaint)}
          className="mt-3 border border-sheild-mid px-3 py-2 font-mono text-xs"
        >
          Copy to Clipboard
        </button>
      </section>
    </main>
  );
}

export default ResultPage;
