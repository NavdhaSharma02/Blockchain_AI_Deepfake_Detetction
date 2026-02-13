import { Shield } from "lucide-react"
import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-card/30">
      <div className="mx-auto max-w-7xl px-4 py-12 lg:px-8">
        <div className="grid gap-8 md:grid-cols-3">
          {/* Brand */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
                <Shield className="h-4 w-4 text-primary" />
              </div>
              <span className="text-lg font-semibold text-foreground">
                Deep<span className="text-primary">Shield</span> AI
              </span>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed max-w-xs">
              Advanced AI-powered deepfake detection platform for images, videos, and audio content.
            </p>
          </div>

          {/* Links */}
          <div className="flex flex-col gap-3">
            <h3 className="text-sm font-semibold text-foreground">Platform</h3>
            <nav className="flex flex-col gap-2">
              <Link href="/detect/image" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Image Detection
              </Link>
              <Link href="/detect/video" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Video Detection
              </Link>
              <Link href="/detect/audio" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Audio Detection
              </Link>
              <Link href="/plugins" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Plugins
              </Link>
            </nav>
          </div>

          {/* Contact */}
          <div className="flex flex-col gap-3">
            <h3 className="text-sm font-semibold text-foreground">Team</h3>
            <p className="text-sm text-muted-foreground">Built by Team DeepShield</p>
            <p className="text-sm text-muted-foreground">National AI Hackathon 2026</p>
            <a
              href="https://github.com/NavdhaSharma02/Blockchain_AI_Deepfake_Detetction"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              GitHub Repository
            </a>
            <a
              href="mailto:team@deepshield.ai"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              team@deepshield.ai
            </a>
          </div>
        </div>

        <div className="mt-10 border-t border-border/40 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} DeepShield AI. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground">
            Powered by Neural Network Analysis
          </p>
        </div>
      </div>
    </footer>
  )
}
