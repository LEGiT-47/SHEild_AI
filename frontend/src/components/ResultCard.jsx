function ResultCard({ verdict, caseId, analyzedAt }) {
  return (
    <div className="border border-sheild-red bg-sheild-card p-5">
      <p className="font-mono text-xs tracking-[0.2em] text-sheild-paper/70">CASE FILE</p>
      <h2 className="mt-3 font-display text-4xl tracking-wide text-sheild-paper">{verdict}</h2>
      <p className="mt-4 font-mono text-xs text-sheild-paper/70">{caseId}</p>
      <p className="font-mono text-xs text-sheild-paper/70">
        {new Date(analyzedAt).toLocaleString()}
      </p>
    </div>
  );
}

export default ResultCard;
