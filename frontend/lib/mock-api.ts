/** Simulated deepfake analysis result */
export interface AnalysisResult {
  verdict: "ORIGINAL" | "FAKE"
  confidence: number
  riskLevel: "Low" | "Medium" | "High"
  breakdown: {
    label: string
    detected: boolean
    detail: string
  }[]
  analysisTime: string
}

/**
 * Simulates a deepfake detection check.
 * In production, this would call the actual AI backend.
 */
export function simulateDeepfakeCheck(
  mediaType: "image" | "video" | "audio"
): Promise<AnalysisResult> {
  return new Promise((resolve) => {
    const delay = 2500 + Math.random() * 1500 // 2.5-4s simulated delay

    setTimeout(() => {
      const isFake = Math.random() > 0.45
      const confidence = isFake
        ? 75 + Math.random() * 20 // 75-95% for fake
        : 80 + Math.random() * 18 // 80-98% for real

      const breakdowns: Record<string, { label: string; detail: string }[]> = {
        image: [
          { label: "Facial Inconsistency", detail: "Asymmetric facial landmarks and blending artifacts detected around jawline" },
          { label: "Compression Artifacts", detail: "Unusual JPEG compression patterns in facial region" },
          { label: "Metadata Analysis", detail: "EXIF data stripped or inconsistent with claimed source" },
          { label: "GAN Fingerprint", detail: "Spectral analysis reveals periodic artifacts common in StyleGAN output" },
        ],
        video: [
          { label: "Temporal Inconsistency", detail: "Frame-to-frame facial movements show unnatural jitter" },
          { label: "Lip Sync Mismatch", detail: "Audio-visual synchronization deviation detected at 340ms offset" },
          { label: "Frame Mismatch", detail: "Inter-frame blending artifacts found in 23% of analyzed frames" },
          { label: "Motion Analysis", detail: "Head pose trajectory shows non-physical movement patterns" },
        ],
        audio: [
          { label: "Voice Modulation Anomaly", detail: "Pitch contour shows synthetic smoothing typical of TTS systems" },
          { label: "Spectral Analysis", detail: "Missing high-frequency harmonics above 8kHz range" },
          { label: "Breath Pattern", detail: "Absence of natural breathing intervals between phrases" },
          { label: "Background Consistency", detail: "Ambient noise floor shows cut-and-splice discontinuities" },
        ],
      }

      const items = breakdowns[mediaType]
      const breakdown = items.map((item, i) => ({
        ...item,
        detected: isFake ? i < 2 || Math.random() > 0.5 : Math.random() > 0.85,
      }))

      resolve({
        verdict: isFake ? "FAKE" : "ORIGINAL",
        confidence: Math.round(confidence * 10) / 10,
        riskLevel: isFake
          ? confidence > 85
            ? "High"
            : "Medium"
          : "Low",
        breakdown,
        analysisTime: `${(delay / 1000).toFixed(1)}s`,
      })
    }, delay)
  })
}
