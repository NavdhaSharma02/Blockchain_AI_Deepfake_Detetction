"use client"

import { DetectionPage } from "@/components/detection/detection-page"

export default function AudioDetectionPage() {
  return (
    <DetectionPage
      mediaType="audio"
      title="Audio Deepfake Detection"
      description="Upload an audio file to detect voice cloning, speech synthesis, and audio manipulation through waveform and spectral analysis."
    />
  )
}
