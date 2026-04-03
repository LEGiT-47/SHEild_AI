import { motion } from "framer-motion";
import { getConfidencePercent } from "../utils/riskUtils";

const toneMap = {
  LOW: "from-sheild-green to-emerald-400",
  MEDIUM: "from-amber-500 to-orange-500",
  HIGH: "from-red-500 to-sheild-red",
};

function RiskMeter({ confidence = 0, riskLevel = "LOW" }) {
  const width = Math.max(0, Math.min(100, Number(confidence) * 100));

  return (
    <div className="border border-sheild-mid bg-black/50 p-4">
      <div className="mb-2 flex items-center justify-between font-mono text-sm">
        <span className="border border-sheild-mid px-2 py-1">RISK: {riskLevel}</span>
        <span>{getConfidencePercent(confidence)}</span>
      </div>
      <div className="h-4 w-full overflow-hidden border border-sheild-mid bg-zinc-900">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${width}%` }}
          transition={{ duration: 1.1, ease: "easeOut" }}
          className={`h-full bg-gradient-to-r ${toneMap[riskLevel] || toneMap.LOW}`}
        />
      </div>
    </div>
  );
}

export default RiskMeter;
