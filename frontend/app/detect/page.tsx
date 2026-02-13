"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Image, Video, AudioLines, ArrowRight, Shield } from "lucide-react"
import { AnimatedBackground } from "@/components/animated-background"

const detectionTypes = [
  {
    title: "Detect Image Deepfake",
    description:
      "Analyze photos and images for AI-generated manipulations, face swaps, and synthetic artifacts.",
    icon: Image,
    href: "/detect/image",
  },
  {
    title: "Detect Video Deepfake",
    description:
      "Frame-by-frame analysis of video content to identify temporal inconsistencies and deepfake patterns.",
    icon: Video,
    href: "/detect/video",
  },
  {
    title: "Detect Audio Deepfake",
    description:
      "Detect voice cloning, speech synthesis, and audio manipulation with waveform analysis.",
    icon: AudioLines,
    href: "/detect/audio",
  },
]

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.12 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

export default function DetectPage() {
  return (
    <>
      <AnimatedBackground />
      <div className="relative z-10 min-h-[calc(100vh-4rem)]">
        {/* Ambient glow */}
        <div
          className="pointer-events-none absolute inset-0 overflow-hidden"
          aria-hidden="true"
        >
          <div className="absolute left-1/2 top-1/4 h-[500px] w-[600px] -translate-x-1/2 rounded-full bg-primary/5 blur-[120px]" />
        </div>

        <div className="relative mx-auto max-w-5xl px-4 py-16 lg:px-8 lg:py-24">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-14 text-center"
          >
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5">
              <Shield className="h-3.5 w-3.5 text-primary" />
              <span className="text-xs font-medium text-primary">
                Choose Detection Type
              </span>
            </div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-5xl text-balance">
              What would you like to{" "}
              <span className="text-primary">analyze</span>?
            </h1>
            <p className="mt-4 text-lg text-muted-foreground max-w-xl mx-auto">
              Select a media type below to start deepfake detection.
            </p>
          </motion.div>

          {/* Selection Cards */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid gap-6 md:grid-cols-3"
          >
            {detectionTypes.map((type) => (
              <motion.div key={type.title} variants={itemVariants}>
                <Link
                  href={type.href}
                  className="group relative flex flex-col gap-6 rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 transition-all duration-300 hover:border-primary/30 hover:glow-cyan h-full"
                >
                  {/* Icon */}
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 border border-primary/20 transition-colors group-hover:bg-primary/20">
                    <type.icon className="h-7 w-7 text-primary" />
                  </div>

                  {/* Content */}
                  <div className="flex flex-col gap-2">
                    <h2 className="text-xl font-semibold text-foreground">
                      {type.title}
                    </h2>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {type.description}
                    </p>
                  </div>

                  {/* Arrow */}
                  <div className="mt-auto flex items-center gap-2 text-sm font-medium text-primary opacity-0 transition-all group-hover:opacity-100 group-hover:translate-x-1">
                    Start Analysis
                    <ArrowRight className="h-4 w-4" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </>
  )
}
