import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import useScrollReveal from "../hooks/useScrollReveal";

const steps = [
  { n: "01", title: "Upload", desc: "Submit image/video evidence securely." },
  { n: "02", title: "Analyze", desc: "Forensic AI inspects artifact signals." },
  { n: "03", title: "Act", desc: "Generate legal-ready actions and report." },
];

const statTargets = [1200000, 87, 3];

function Home() {
  const { ref: statsRef, isVisible } = useScrollReveal();
  const [counts, setCounts] = useState([0, 0, 0]);

  useEffect(() => {
    if (!isVisible) return;
    let frame = 0;
    const totalFrames = 60;
    const id = setInterval(() => {
      frame += 1;
      setCounts(statTargets.map((target) => Math.round((target * frame) / totalFrames)));
      if (frame >= totalFrames) clearInterval(id);
    }, 25);
    return () => clearInterval(id);
  }, [isVisible]);

  const stats = useMemo(
    () => [
      `${counts[0].toLocaleString()}+ deepfakes detected`,
      `${counts[1]}% victims are women`,
      `<${Math.max(1, counts[2])} min to analyze`,
    ],
    [counts]
  );

  return (
    <main className="content-layer relative overflow-hidden">
      <section className="relative flex min-h-screen items-center justify-center px-6 text-center">
        <div className="scanline-overlay" />
        <div>
          <h1 className="font-display text-[clamp(3rem,10vw,6rem)] leading-none text-sheild-paper">
            Every Pixel Lies.
          </h1>
          <p className="mt-5 font-mono text-sm uppercase tracking-[0.35em] text-sheild-paper/80">
            AI-powered deepfake forensics
          </p>
          <Link
            to="/upload"
            className="mt-10 inline-block border-2 border-white bg-sheild-red px-9 py-4 font-display text-xl tracking-[0.25em] text-white transition hover:-translate-y-1"
          >
            OPEN CASE FILE
          </Link>
          <p className="mt-10 animate-bounce font-mono text-xs tracking-[0.25em] text-sheild-paper/70">
            SCROLL TO INVESTIGATE
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-24">
        <h2 className="mb-14 font-display text-5xl">How It Works</h2>
        <div className="relative grid gap-8 md:grid-cols-3">
          <svg className="pointer-events-none absolute left-0 top-1/2 hidden w-full -translate-y-1/2 md:block" height="2">
            <line x1="0" y1="1" x2="100%" y2="1" stroke="#c0392b" strokeDasharray="8 8" />
          </svg>
          {steps.map((step, i) => (
            <motion.article
              key={step.n}
              initial={{ opacity: 0, y: 35 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: i * 0.2 }}
              viewport={{ once: true, amount: 0.4 }}
              className="relative border border-sheild-mid bg-sheild-card p-6"
            >
              <p className="font-mono text-5xl text-sheild-red">{step.n}</p>
              <h3 className="mt-4 font-display text-3xl">{step.title}</h3>
              <p className="mt-3 font-mono text-sm text-sheild-paper/80">{step.desc}</p>
            </motion.article>
          ))}
        </div>
      </section>

      <section ref={statsRef} className="bg-[#111] px-6 py-16">
        <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-3">
          {stats.map((label, i) => (
            <article key={label} className="border border-sheild-mid p-6 text-center">
              <p className="font-display text-5xl text-sheild-paper">{i === 0 ? `${counts[0].toLocaleString()}+` : i === 1 ? `${counts[1]}%` : `<${Math.max(1, counts[2])}`}</p>
              <p className="mt-3 font-mono text-xs uppercase tracking-[0.2em] text-sheild-paper/80">{label}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default Home;
