function TracePanel({ traceability = [] }) {
  return (
    <section>
      <h3 className="mb-3 font-display text-3xl text-sheild-paper">Reverse Trace Board</h3>
      <div className="grid gap-3 md:grid-cols-3">
        {traceability.map((item, idx) => (
          <article
            key={`${item.source}-${idx}`}
            className="border border-zinc-700 bg-[#f4ecd6] p-4 text-black shadow-[0_8px_20px_rgba(0,0,0,0.35)]"
            style={{ transform: `rotate(${idx % 2 === 0 ? -1 : 1}deg)` }}
          >
            <p className="font-display text-xl">{item.source}</p>
            <p className="mt-2 break-all font-mono text-xs">{item.url}</p>
            <p className="mt-2 font-mono text-xs">Found: {item.found_at}</p>
            <p className="mt-1 inline-block border border-black px-2 py-1 font-mono text-xs">
              {Math.round((item.confidence || 0) * 100)}% match
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default TracePanel;
