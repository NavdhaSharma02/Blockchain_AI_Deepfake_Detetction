"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Image, Video, AudioLines, ArrowRight } from "lucide-react"

const cards = [
  {
    title: "Image Detection",
    description: "Analyze photos and images for AI-generated manipulations, face swaps, and synthetic artifacts.",
    icon: Image,
    href: "/detect/image",
    gradient: "from-primary/20 to-primary/5",
  },
  {
    title: "Video Detection",
    description: "Frame-by-frame analysis of video content to identify temporal inconsistencies and deepfake patterns.",
    icon: Video,
    href: "/detect/video",
    gradient: "from-primary/20 to-primary/5",
  },
  {
    title: "Audio Detection",
    description: "Detect voice cloning, speech synthesis, and audio manipulation with waveform analysis.",
    icon: AudioLines,
    href: "/detect/audio",
    gradient: "from-primary/20 to-primary/5",
  },
]

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

export function DetectionCardsSection() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-14 text-center"
        >
          <h2 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl text-balance">
            Multi-Modal Detection
          </h2>
          <p className="mt-4 text-muted-foreground text-lg max-w-xl mx-auto">
            Choose your media type and let our AI analyze it for deepfake signatures.
          </p>
        </motion.div>

        {/* Cards grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid gap-6 md:grid-cols-3"
        >
          {cards.map((card) => (
            <motion.div key={card.title} variants={itemVariants}>
              <Link
                href={card.href}
                className="group relative flex flex-col gap-6 rounded-2xl border border-border/50 bg-card/50 backdrop-blur-xl p-8 transition-all duration-300 hover:border-primary/30 hover:glow-cyan"
              >
                {/* Icon */}
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 border border-primary/20 transition-colors group-hover:bg-primary/20">
                  <card.icon className="h-7 w-7 text-primary" />
                </div>

                {/* Content */}
                <div className="flex flex-col gap-2">
                  <h3 className="text-xl font-semibold text-foreground">{card.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{card.description}</p>
                </div>

                {/* Arrow */}
                <div className="mt-auto flex items-center gap-2 text-sm font-medium text-primary opacity-0 transition-all group-hover:opacity-100 group-hover:translate-x-1">
                  Analyze Now
                  <ArrowRight className="h-4 w-4" />
                </div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
