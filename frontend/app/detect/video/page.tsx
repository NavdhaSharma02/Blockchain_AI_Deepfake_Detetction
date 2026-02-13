"use client"

import { DetectionPage } from "@/components/detection/detection-page"

export default function VideoDetectionPage() {
  return (
    <DetectionPage
      mediaType="video"
      title="Video Deepfake Detection"
      description="Upload a video for frame-by-frame analysis to identify temporal inconsistencies, lip-sync mismatches, and deepfake patterns."
    />
  )
}
