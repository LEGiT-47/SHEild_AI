function ActionPanel({ actionSteps = [], riskLevel = "LOW" }) {
  return (
    <section className="border border-sheild-mid bg-black/40 p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-3xl text-sheild-paper">Recommended Actions</h3>
        <span className="border border-sheild-red px-3 py-1 font-mono text-xs">{riskLevel}</span>
      </div>
      <ol className="space-y-3">
        {actionSteps.map((step, idx) => (
          <li key={`${step}-${idx}`} className="border-l-4 border-sheild-red pl-3">
            <span className="mr-3 font-display text-2xl text-sheild-red">{idx + 1}.</span>
            <span className="font-mono text-sm text-sheild-paper">{step}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}

export default ActionPanel;
