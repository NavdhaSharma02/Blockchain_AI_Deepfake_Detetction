"use client"

import { motion } from "framer-motion"
import { Chrome, Globe, Shield, Zap, Eye, Puzzle } from "lucide-react"
import Link from "next/link"

const platforms = [
  { name: "Instagram", icon: "IG" },
  { name: "YouTube", icon: "YT" },
  { name: "X (Twitter)", icon: "X" },
  { name: "WhatsApp Web", icon: "WA" },
]

export default function PluginsPage() {
  return (
    <div className="relative min-h-[calc(100vh-4rem)]">
      {/* Ambient glow */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div className="absolute left-1/2 top-1/4 h-[500px] w-[600px] -translate-x-1/2 rounded-full bg-primary/3 blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-4xl px-4 py-16 lg:px-8 lg:py-24">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5">
            <Puzzle className="h-3.5 w-3.5 text-primary" />
            <span className="text-xs font-medium text-primary">Coming Soon</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-5xl text-balance">
            Browser & Social Media Extension
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-lg text-muted-foreground leading-relaxed">
            Real-time deepfake detection directly in your browser. No uploads needed -- our extension analyzes media as you browse.
          </p>
        </motion.div>

        {/* Mock Extension Preview Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl overflow-hidden mb-12"
        >
          {/* Browser chrome mockup */}
          <div className="flex items-center gap-2 border-b border-border/40 bg-secondary/30 px-4 py-3">
            <div className="flex items-center gap-1.5">
              <div className="h-3 w-3 rounded-full bg-destructive/40" />
              <div className="h-3 w-3 rounded-full bg-chart-4/40" />
              <div className="h-3 w-3 rounded-full bg-success/40" />
            </div>
            <div className="flex-1 flex justify-center">
              <div className="flex items-center gap-2 rounded-lg bg-secondary/50 px-4 py-1.5 text-xs text-muted-foreground max-w-sm w-full">
                <Globe className="h-3 w-3" />
                <span>socialmedia.com/post/12345</span>
              </div>
            </div>
            <Chrome className="h-4 w-4 text-muted-foreground" />
          </div>

          {/* Extension popup mockup */}
          <div className="p-8 md:p-12">
            <div className="mx-auto max-w-sm">
              <div className="rounded-xl border border-primary/20 bg-background/80 p-6 glow-cyan">
                <div className="flex items-center gap-3 mb-5">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                    <Shield className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-foreground">DeepShield Extension</p>
                    <p className="text-xs text-primary">Active - Monitoring</p>
                  </div>
                </div>

                {/* Status items */}
                <div className="flex flex-col gap-3">
                  <div className="flex items-center justify-between rounded-lg bg-success/5 border border-success/20 p-3">
                    <div className="flex items-center gap-2">
                      <Eye className="h-4 w-4 text-success" />
                      <span className="text-xs text-foreground">Images scanned</span>
                    </div>
                    <span className="text-xs font-mono text-success">12 Clear</span>
                  </div>
                  <div className="flex items-center justify-between rounded-lg bg-destructive/5 border border-destructive/20 p-3">
                    <div className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-destructive" />
                      <span className="text-xs text-foreground">Deepfake detected</span>
                    </div>
                    <span className="text-xs font-mono text-destructive">1 Flagged</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Platform Support */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          className="mb-12"
        >
          <h2 className="text-lg font-semibold text-foreground text-center mb-6">
            Platform Support
          </h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {platforms.map((platform) => (
              <div
                key={platform.name}
                className="flex flex-col items-center gap-3 rounded-2xl border border-border/50 bg-card/30 p-6 backdrop-blur-xl"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-secondary text-sm font-bold text-foreground">
                  {platform.icon}
                </div>
                <span className="text-sm text-muted-foreground">{platform.name}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Features list */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
          className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 mb-12"
        >
          <h2 className="text-lg font-semibold text-foreground mb-6">What to Expect</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {[
              "Real-time deepfake detection as you scroll",
              "Works on images, videos, and audio",
              "No file uploads required",
              "Privacy-first -- analysis happens locally",
              "Instant visual warnings on detected fakes",
              "Detailed reports with one click",
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-primary/10">
                  <Zap className="h-3 w-3 text-primary" />
                </div>
                <span className="text-sm text-muted-foreground">{feature}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.55 }}
          className="text-center"
        >
          <p className="text-muted-foreground mb-6">
            Want to try deepfake detection now? Use our web platform.
          </p>
          <Link
            href="/detect/image"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-6 py-3.5 text-sm font-semibold text-primary-foreground transition-all hover:brightness-110 hover:glow-cyan"
          >
            Try Detection Now
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
