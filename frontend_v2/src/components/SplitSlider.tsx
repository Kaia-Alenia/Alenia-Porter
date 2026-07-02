import React, { useState, useRef, useEffect } from "react";
import { Play, Pause, RefreshCw, Volume2, Maximize2 } from "lucide-react";

interface SplitSliderProps {
  mediaType: "video" | "audio" | "image";
  mediaSrc: string;
  quality: number; // CRF (18-51, lower is better) or Quality score (1-100, higher is better)
  compressedSizeText: string;
  originalSizeText: string;
}

export default function SplitSlider({
  mediaType,
  mediaSrc,
  quality,
  compressedSizeText,
  originalSizeText,
}: SplitSliderProps) {
  const [sliderPosition, setSliderPosition] = useState(50); // percentage
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.8);
  const containerRef = useRef<HTMLDivElement>(null);
  const mediaRef = useRef<HTMLVideoElement | HTMLAudioElement | null>(null);

  // Drag logic for split handle
  const handleMove = (clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPosition(percentage);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.touches.length > 0) {
      handleMove(e.touches[0].clientX);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (e.buttons === 1) {
      handleMove(e.clientX);
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    handleMove(e.clientX);
  };

  // Synchronize audio element state
  const togglePlay = () => {
    if (!mediaRef.current) return;
    if (isPlaying) {
      mediaRef.current.pause();
      setIsPlaying(false);
    } else {
      mediaRef.current.play().then(() => {
        setIsPlaying(true);
      }).catch(err => {
        console.error("Audio/Video play error:", err);
      });
    }
  };

  useEffect(() => {
    if (mediaRef.current) {
      mediaRef.current.volume = volume;
    }
  }, [volume]);

  // Reset play state if media changes
  useEffect(() => {
    setIsPlaying(false);
    if (mediaRef.current) {
      mediaRef.current.pause();
    }
  }, [mediaSrc, mediaType]);

  // Determine degradation CSS filters based on quality settings
  // If CRF is 18-23: perfect. If 24-28: mild. If 29-35: medium. If 36-51: severe.
  const getFilterStyle = () => {
    if (mediaType === "audio") return {};

    // Assuming scale is CRF-like: higher is lower quality (crf: 18 to 51)
    // Or image-like: 0 to 100 (where lower is lower quality)
    const isImageMode = quality > 51;
    const resolvedQuality = isImageMode ? (100 - quality) : quality; // normalize (higher is worse)

    let blur = "0px";
    let contrast = "100%";
    let saturate = "100%";
    let pixelated = false;

    const badness = isImageMode
      ? (100 - quality) / 100 // 0 to 1, higher is worse quality
      : Math.max(0, (quality - 18) / 33); // 0 to 1, higher is worse quality

    if (badness > 0.8) {
      blur = "1.5px";
      contrast = "85%";
      saturate = "80%";
      pixelated = true;
    } else if (badness > 0.5) {
      blur = "1.0px";
      contrast = "90%";
      saturate = "90%";
      pixelated = true;
    } else if (badness > 0.2) {
      blur = "0.5px";
      contrast = "96%";
      saturate = "97%";
    }

    return {
      filter: `blur(${blur}) contrast(${contrast}) saturate(${saturate})`,
      imageRendering: pixelated ? "pixelated" as const : "auto" as const,
    };
  };

  return (
    <div className="flex flex-col bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
      {/* Top Title Bar of Previewer */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-b border-gray-200 text-xs text-gray-600 font-mono">
        <span className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
          PREVISUALIZACIÓN DE COMPRESIÓN EN TIEMPO REAL
        </span>
        <div className="flex items-center gap-3">
          <span className="text-gray-400 text-[10px]">Arrastra la barra para comparar</span>
        </div>
      </div>

      {/* Media Stage Canvas */}
      <div
        ref={containerRef}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onTouchMove={handleTouchMove}
        className="relative w-full h-[320px] bg-gradient-to-br from-gray-900 to-black flex items-center justify-center overflow-hidden cursor-ew-resize select-none"
      >
        {mediaType === "video" && (
          <div className="relative w-full h-full">
            {/* Base (Original / Left Half Side) */}
            <video
              ref={mediaRef as any}
              src={mediaSrc}
              loop
              muted
              playsInline
              className="absolute inset-0 w-full h-full object-cover pointer-events-none"
            />

            {/* Overlay (Optimized / Right Side under clip-path) */}
            <video
              src={mediaSrc}
              loop
              muted
              playsInline
              style={{
                clipPath: `polygon(${sliderPosition}% 0, 100% 0, 100% 100%, ${sliderPosition}% 100%)`,
                ...getFilterStyle(),
              }}
              className="absolute inset-0 w-full h-full object-cover pointer-events-none"
              ref={(el) => {
                // Keep the second video in sync with the primary
                if (el && mediaRef.current) {
                  el.currentTime = (mediaRef.current as HTMLVideoElement).currentTime;
                  if (isPlaying && el.paused) el.play().catch(() => {});
                  if (!isPlaying && !el.paused) el.pause();
                }
              }}
            />
          </div>
        )}

        {mediaType === "image" && (
          <div className="relative w-full h-full">
            {/* Original Left */}
            <img
              src={mediaSrc}
              alt="Original"
              className="absolute inset-0 w-full h-full object-cover pointer-events-none"
              referrerPolicy="no-referrer"
            />

            {/* Optimized Right */}
            <img
              src={mediaSrc}
              alt="Optimized"
              style={{
                clipPath: `polygon(${sliderPosition}% 0, 100% 0, 100% 100%, ${sliderPosition}% 100%)`,
                ...getFilterStyle(),
              }}
              className="absolute inset-0 w-full h-full object-cover pointer-events-none"
              referrerPolicy="no-referrer"
            />
          </div>
        )}

        {mediaType === "audio" && (
          <div className="w-full h-full flex flex-col items-center justify-center px-8 relative bg-gradient-to-br from-slate-900 to-black overflow-hidden">
            <audio ref={mediaRef as any} src={mediaSrc} loop />

            {/* Simulated interactive audio wavelengths */}
            <div className="flex items-end justify-center gap-1.5 h-36 w-full max-w-md">
              {Array.from({ length: 28 }).map((_, i) => {
                const badness = Math.max(0, (quality - 1) / 9); // audio quality is 1-10 (lower is worse)
                const heightMult = isPlaying ? (badness < 0.4 ? 0.35 : 1) : 0.05;
                const randomOffset = isPlaying ? Math.sin(i * 0.4 + Date.now() * 0.01) * 35 + 40 : 10;
                const heightVal = Math.max(8, randomOffset * heightMult);

                // Simulate audio spectrum compression visually (cutting high frequencies on the right side of the visual wave)
                const isRightHalf = i > 14;
                const cutFactor = isRightHalf && badness < 0.5 ? (badness < 0.2 ? 0.15 : 0.45) : 1;
                const finalHeight = heightVal * cutFactor;

                return (
                  <div
                    key={i}
                    style={{ height: `${finalHeight}%` }}
                    className={`w-3 rounded-full transition-all duration-75 ${
                      isRightHalf
                        ? "bg-blue-500/80 shadow-[0_0_10px_rgba(59,130,246,0.3)]"
                        : "bg-indigo-400"
                    }`}
                  />
                );
              })}
            </div>

            {/* Left and Right Audio Mode Label */}
            <div className="absolute inset-x-8 top-6 flex justify-between font-mono text-[10px] text-gray-500">
              <span>Original (No Lossless Cut)</span>
              <span>Comprimido (Corte de Frecuencias)</span>
            </div>
          </div>
        )}

        {/* Vertical Sliding Divider Handle */}
        {mediaType !== "audio" && (
          <div
            style={{ left: `${sliderPosition}%` }}
            className="slider-handle"
          >
            <div className="slider-button !bg-blue-600">
              <span className="text-xs font-bold font-sans">↔</span>
            </div>
          </div>
        )}

        {/* Overlay Badges for Original / Compressed */}
        <div className="absolute top-4 left-4 z-20 pointer-events-none">
          <span className="px-3 py-1.5 text-[10px] font-mono font-medium rounded-lg bg-white/95 backdrop-blur-md shadow-sm border border-gray-200 text-gray-700">
            Original: {originalSizeText}
          </span>
        </div>
        <div className="absolute top-4 right-4 z-20 pointer-events-none">
          <span className="px-3 py-1.5 text-[10px] font-mono font-bold rounded-lg bg-blue-50/95 backdrop-blur-md shadow-sm border border-blue-200 text-blue-700">
            Optimizado: {compressedSizeText}
          </span>
        </div>

        {/* Sliding Help Labels on Canvas */}
        {mediaType !== "audio" && (
          <div className="absolute bottom-4 left-4 z-20 pointer-events-none select-none opacity-40 font-mono text-[10px] text-white bg-black/30 px-1.5 py-0.5 rounded">
            Izquierda: ORIGINAL
          </div>
        )}
        {mediaType !== "audio" && (
          <div className="absolute bottom-4 right-4 z-20 pointer-events-none select-none opacity-40 font-mono text-[10px] text-white bg-black/30 px-1.5 py-0.5 rounded">
            Derecha: ENCODED
          </div>
        )}
      </div>

      {/* Control Bar (Play, Volume, Pause, Progress info) */}
      {(mediaType === "video" || mediaType === "audio") && (
        <div className="flex items-center gap-4 px-4 py-3 bg-gray-50 border-t border-gray-200">
          <button
            onClick={togglePlay}
            className="p-2 bg-black hover:bg-gray-800 text-white rounded-full transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black cursor-pointer"
          >
            {isPlaying ? <Pause size={16} /> : <Play size={16} className="ml-0.5" />}
          </button>

          <div className="flex items-center gap-2">
            <Volume2 size={15} className="text-gray-500" />
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={volume}
              onChange={(e) => setVolume(parseFloat(e.target.value))}
              className="w-20 h-1 rounded-lg bg-gray-200 cursor-pointer accent-blue-600"
            />
          </div>

          <div className="ml-auto flex items-center gap-2 font-mono text-xs text-gray-500">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            <span>{isPlaying ? "Reproduciendo previsualización..." : "Listo para reproducir"}</span>
          </div>
        </div>
      )}
    </div>
  );
}
