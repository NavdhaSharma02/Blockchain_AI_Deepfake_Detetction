"use client"

import { AnimatedBackground } from "@/components/animated-background"
import { HeroSection } from "@/components/landing/hero-section"
import { DetectionCardsSection } from "@/components/landing/detection-cards-section"
import { FeaturesSection } from "@/components/landing/features-section"
import { Web3Section } from "@/components/landing/web3-section"

export default function HomePage() {
  return (
    <>
      <AnimatedBackground />
      <div className="relative z-10">
        <HeroSection />
        <DetectionCardsSection />
        <Web3Section />
        <FeaturesSection />
      </div>
    </>
  )
}
