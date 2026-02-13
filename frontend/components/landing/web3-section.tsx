"use client"

import { motion } from "framer-motion"
import { Link2, ShieldCheck } from "lucide-react"

export function Web3Section() {
  return (
    <section className="relative py-16 md:py-20">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="rounded-2xl border border-primary/20 bg-primary/5 backdrop-blur-xl p-8 md:p-10"
        >
          <div className="flex flex-col items-center text-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 border border-primary/20">
              <Link2 className="h-6 w-6 text-primary" />
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold text-foreground md:text-xl">
                Web3 Blockchain Verification
              </h3>
            </div>
            <p className="max-w-2xl text-sm text-muted-foreground leading-relaxed md:text-base">
              This platform integrates Web3 blockchain technology to ensure tamper-proof verification
              and immutable authenticity tracking of media analysis results.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
