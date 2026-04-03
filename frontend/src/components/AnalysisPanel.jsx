import { motion } from "framer-motion";

function AnalysisPanel({ artifacts = [] }) {
  return (
    <div className="border border-sheild-mid bg-black/70 p-4">
      <p className="mb-3 font-mono text-xs tracking-[0.25em] text-sheild-cyan">ARTIFACT LOG</p>
      <motion.ul
        initial="hidden"
        animate="show"
        variants={{
          hidden: { opacity: 0 },
          show: { opacity: 1, transition: { staggerChildren: 0.1 } },
        }}
        className="space-y-2"
      >
        {artifacts.map((item, idx) => (
          <motion.li
            key={`${item}-${idx}`}
            variants={{ hidden: { opacity: 0, x: -10 }, show: { opacity: 1, x: 0 } }}
            className="font-mono text-sm text-sheild-cyan"
          >
            &gt; {item}
          </motion.li>
        ))}
      </motion.ul>
      <span className="mt-2 inline-block h-4 w-2 animate-pulse bg-sheild-cyan" />
    </div>
  );
}

export default AnalysisPanel;
