"use client"

import { motion } from "framer-motion"
import { Shield, Brain, Lock, Users, Github, Mail, Link2, Fingerprint, Layers, Globe, Database } from "lucide-react"
import Link from "next/link"

const team = [
  { name: "Riddhi Poddar" },
  { name: "Lakshmi Aneesha Ambati" },
  { name: "Navdha Sharma" },
  { name: "Mihika Manish" },
]

const values = [
  {
    title: "AI-First Approach",
    description: "We leverage cutting-edge neural networks and deep learning models to achieve state-of-the-art detection accuracy.",
    icon: Brain,
  },
  {
    title: "Privacy by Design",
    description: "Your media is analyzed in real-time and never stored. We believe in privacy-preserving AI that respects user data.",
    icon: Lock,
  },
  {
    title: "Open Research",
    description: "We contribute to the broader research community by sharing our findings and collaborating with academic institutions.",
    icon: Users,
  },
]

const trustLevels = [
  {
    label: "Verified Authentic",
    description: "Cryptographically proven original via blockchain provenance record.",
    color: "text-emerald-400",
    border: "border-emerald-400/30",
    bg: "bg-emerald-400/10",
  },
  {
    label: "AI Detected Fake",
    description: "Manipulation patterns detected through AI forensic analysis.",
    color: "text-red-400",
    border: "border-red-400/30",
    bg: "bg-red-400/10",
  },
  {
    label: "Unverified",
    description: "No provenance record and no strong manipulation evidence found.",
    color: "text-amber-400",
    border: "border-amber-400/30",
    bg: "bg-amber-400/10",
  },
]

export default function AboutPage() {
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
            <Shield className="h-3.5 w-3.5 text-primary" />
            <span className="text-xs font-medium text-primary">About DeepShield</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-5xl text-balance">
            Protecting Authenticity in the Age of AI
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-lg text-muted-foreground leading-relaxed">
            DeepShield AI is a next-generation deepfake detection platform built to combat the growing threat of synthetic media manipulation.
          </p>
        </motion.div>

        {/* Mission */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="rounded-2xl border border-primary/20 bg-primary/5 p-8 md:p-10 mb-12 text-center"
        >
          <h2 className="text-xl font-semibold text-foreground mb-4">Our Mission</h2>
          <p className="text-muted-foreground leading-relaxed max-w-2xl mx-auto">
            As generative AI becomes increasingly powerful, the ability to create convincing fake media grows exponentially.
            Our mission is to provide accessible, accurate, and fast deepfake detection tools that empower individuals,
            journalists, and organizations to verify the authenticity of digital media.
          </p>
        </motion.div>

        {/* Values */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="grid gap-6 md:grid-cols-3 mb-16"
        >
          {values.map((value) => (
            <div
              key={value.title}
              className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-6"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 border border-primary/20 mb-4">
                <value.icon className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">{value.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{value.description}</p>
            </div>
          ))}
        </motion.div>

        {/* ===== Innovation & System Novelty ===== */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-16"
        >
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-3xl">
              Innovation &amp; System Novelty
            </h2>
            <p className="mt-3 text-muted-foreground max-w-xl mx-auto">
              A hybrid architecture that goes beyond traditional AI-only detection.
            </p>
          </div>

          {/* Hybrid Trust Architecture */}
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 mb-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                <Layers className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">Hybrid Trust Architecture (AI + Blockchain)</h3>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {/* Layer 1 */}
              <div className="rounded-xl border border-border/40 bg-background/50 p-5">
                <div className="flex items-center gap-2 mb-3">
                  <Link2 className="h-4 w-4 text-primary" />
                  <h4 className="text-sm font-semibold text-foreground">Layer 1 -- Cryptographic Provenance (Web3)</h4>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Media is registered on blockchain using SHA-256 fingerprinting. If a match exists, authenticity is
                  mathematically proven -- not predicted.
                </p>
              </div>

              {/* Layer 2 */}
              <div className="rounded-xl border border-border/40 bg-background/50 p-5">
                <div className="flex items-center gap-2 mb-3">
                  <Brain className="h-4 w-4 text-primary" />
                  <h4 className="text-sm font-semibold text-foreground">Layer 2 -- AI Forensic Detection</h4>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  If no blockchain record exists, AI analyzes manipulation patterns in image, video, or audio
                  using deep neural networks trained on millions of samples.
                </p>
              </div>
            </div>

            <p className="mt-5 text-sm text-muted-foreground leading-relaxed border-t border-border/30 pt-5">
              Unlike traditional systems that only predict whether media looks fake, DeepShield first attempts
              cryptographic authenticity verification before applying AI analysis. This shifts detection from
              probability-based judgment to evidence-based validation.
            </p>
          </div>

          {/* Trust Classification Model */}
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 mb-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                <Fingerprint className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">Trust Classification Model</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed mb-5">
              Instead of a binary Real/Fake output, DeepShield uses a three-tier trust classification that
              reduces false accusations and improves reliability.
            </p>
            <div className="grid gap-3 sm:grid-cols-3">
              {trustLevels.map((level) => (
                <div
                  key={level.label}
                  className={`rounded-xl border ${level.border} ${level.bg} p-4`}
                >
                  <p className={`text-sm font-semibold ${level.color} mb-1`}>{level.label}</p>
                  <p className="text-xs text-muted-foreground leading-relaxed">{level.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Plugin-Based Protection */}
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                <Globe className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">Plugin-Based Real-World Protection</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              We are developing a universal browser extension that scans media directly on social platforms and webpages,
              automatically verifies blockchain fingerprints, and applies AI detection in real time. This converts
              deepfake detection from a manual tool into an ambient safety layer.
            </p>
          </div>

          {/* Persistent Authenticity Records */}
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                <Database className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">Persistent Authenticity Records</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Each registered media item creates a permanent, tamper-proof blockchain record enabling lifetime
              traceability from creator to redistribution.
            </p>
          </div>
        </motion.div>

        {/* Team */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 mb-12"
        >
          <h2 className="text-lg font-semibold text-foreground mb-6 text-center">The Team</h2>
          <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-4">
            {team.map((member) => (
              <div key={member.name} className="flex flex-col items-center gap-3 p-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 border border-primary/20">
                  <Shield className="h-6 w-6 text-primary" />
                </div>
                <p className="text-sm font-semibold text-foreground text-center">{member.name}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-muted-foreground mt-6 text-center max-w-md mx-auto">
            Built for the National AI Hackathon 2026. Our team combines expertise in computer vision, deep learning, blockchain, and cybersecurity.
          </p>
        </motion.div>

        {/* Contact */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
          className="flex flex-col items-center gap-6 text-center"
        >
          <h2 className="text-lg font-semibold text-foreground">Get in Touch</h2>
          <div className="flex gap-4">
            <a
              href="https://github.com/NavdhaSharma02/Blockchain_AI_Deepfake_Detetction"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border border-border/60 bg-secondary/50 px-5 py-3 text-sm font-medium text-foreground transition-colors hover:bg-secondary"
            >
              <Github className="h-4 w-4" />
              GitHub
            </a>
            <a
              href="mailto:team@deepshield.ai"
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-medium text-primary-foreground transition-all hover:brightness-110 hover:glow-cyan"
            >
              <Mail className="h-4 w-4" />
              Contact Us
            </a>
          </div>
          <Link
            href="/detect"
            className="text-sm text-muted-foreground hover:text-primary transition-colors"
          >
            Or try the detection platform now
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
