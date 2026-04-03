export function getRiskColor(level) {
  if (level === "HIGH") return "text-sheild-red border-sheild-red";
  if (level === "MEDIUM") return "text-amber-400 border-amber-400";
  return "text-sheild-green border-sheild-green";
}

export function getRiskLabel(level) {
  if (!level) return "UNKNOWN";
  return level.toUpperCase();
}

export function getConfidencePercent(confidence) {
  const value = Number(confidence || 0) * 100;
  return `${value.toFixed(1)}%`;
}
