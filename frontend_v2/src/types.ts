export type MediaType = "video" | "audio" | "image";

export interface DemoFile {
  id: string;
  name: string;
  type: MediaType;
  originalSize: number; // in bytes
  duration?: string; // e.g. "0:15"
  resolution?: string; // e.g. "1920x1080"
  src: string; // fallback or simulated stream URL
  simulatedDataUrl?: string; // visual content
  path?: string; // relative path if uploaded recursively
  isDirectory?: boolean; // true when path points to a folder
  status?: "pending" | "processing" | "completed" | "failed";
  hash?: string; // MD5/SHA representation for smart caching
  errorContext?: string; // Context details in case of errors
}

export interface CompressionSettings {
  format: string; // e.g., "mp4", "webm", "ogg", "opus", "mp3", "jpg", "png"
  codec: string; // e.g. "libx264", "libvpx", "libopus", "libvorbis", "libmp3lame"
  quality: number; // CRF for video (e.g. 18-35), quality score for audio (1-10) or quality for images (1-100)
  audioBitrate: number; // in kbps, e.g., 64, 96, 128, 192, 320
  scale: string; // e.g., "1920x1080", "1280x720", "854x480", "original"
  fps: number; // frame rate, e.g. 24, 30, 60, "original"
  speedPreset: string; // e.g. "ultrafast", "faster", "medium", "slow"
  customArgs: string; // any extra flags
}

export interface TerminalLog {
  id: string;
  timestamp: string;
  text: string;
  type: "info" | "stdout" | "stderr" | "success" | "error";
}

export interface OptimizationResult {
  fileName: string;
  mediaType: MediaType;
  originalSize: number;
  compressedSize: number;
  savingsPercent: number;
  format: string;
  commandUsed: string;
  timestamp: string;
}
