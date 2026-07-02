import React from "react";
import { motion } from "motion/react";

interface MascotProps {
  state?: "idle" | "thinking" | "success" | "error" | "winking";
  size?: number;
}

export default function Mascot({ state = "idle", size = 120 }: MascotProps) {
  // SVG proportions are 100x100
  return (
    <div style={{ width: size, height: size }} className="relative flex items-center justify-center select-none">
      <motion.svg
        viewBox="0 0 100 100"
        className="w-full h-full"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {/* Shadow */}
        <ellipse cx="50" cy="88" rx="30" ry="6" fill="rgba(0,0,0,0.06)" />

        {/* Mascot Body & Face Group */}
        <motion.g
          animate={
            state === "thinking"
              ? { y: [0, -4, 0] }
              : state === "success"
              ? { y: [0, -8, 0, -5, 0], scale: [1, 1.05, 1, 1.02, 1] }
              : { y: [0, -2, 0] }
          }
          transition={
            state === "thinking"
              ? { repeat: Infinity, duration: 1.5, ease: "easeInOut" }
              : state === "success"
              ? { duration: 0.8, ease: "easeOut" }
              : { repeat: Infinity, duration: 4, ease: "easeInOut", repeatDelay: 1 }
          }
        >
          {/* Ears */}
          {/* Left Ear */}
          <circle cx="28" cy="28" r="12" fill="#FFFFFF" stroke="#1E1E24" strokeWidth="2.5" />
          <circle cx="28" cy="28" r="7" fill="#FBCFE8" /> {/* pink inner */}

          {/* Right Ear */}
          <circle cx="72" cy="28" r="12" fill="#FFFFFF" stroke="#1E1E24" strokeWidth="2.5" />
          <circle cx="72" cy="28" r="7" fill="#FBCFE8" />

          {/* Body/Head base */}
          <rect
            x="20"
            y="28"
            width="60"
            height="54"
            rx="27"
            fill="#FFFFFF"
            stroke="#1E1E24"
            strokeWidth="2.5"
          />

          {/* Arms (cute small paws reaching out) */}
          <motion.g
            animate={
              state === "success"
                ? { rotate: [0, 15, -15, 15, -15, 0] }
                : { rotate: [0, 2, -2, 0] }
            }
            transition={{ duration: 0.8, repeat: state === "success" ? 1 : 0 }}
          >
            {/* Left Paw */}
            <rect
              x="14"
              y="54"
              width="10"
              height="14"
              rx="5"
              fill="#FFFFFF"
              stroke="#1E1E24"
              strokeWidth="2.5"
              transform="rotate(-20 19 61)"
            />
            {/* Right Paw */}
            <rect
              x="76"
              y="54"
              width="10"
              height="14"
              rx="5"
              fill="#FFFFFF"
              stroke="#1E1E24"
              strokeWidth="2.5"
              transform="rotate(20 81 61)"
            />
          </motion.g>

          {/* Eyes */}
          {/* Left Eye */}
          {state === "winking" || state === "success" ? (
            // Winking Eye (arched line)
            <path
              d="M32 48 Q40 40 44 48"
              fill="none"
              stroke="#1E1E24"
              strokeWidth="4"
              strokeLinecap="round"
            />
          ) : (
            // Big cute open eye
            <g>
              <circle cx="38" cy="48" r="7.5" fill="#1E1E24" />
              {/* Eye sparkle highlights */}
              <circle cx="36.5" cy="45" r="2.5" fill="#FFFFFF" />
              <circle cx="41" cy="51" r="1" fill="#FFFFFF" />
            </g>
          )}

          {/* Right Eye */}
          <g>
            <circle cx="62" cy="48" r="7.5" fill="#1E1E24" />
            <circle cx="60.5" cy="45" r="2.5" fill="#FFFFFF" />
            <circle cx="65" cy="51" r="1" fill="#FFFFFF" />
          </g>

          {/* Rosy Cheeks */}
          <circle cx="30" cy="56" r="4.5" fill="#FDA4AF" opacity="0.8" />
          <circle cx="70" cy="56" r="4.5" fill="#FDA4AF" opacity="0.8" />

          {/* Cute Mouth & Nose */}
          {/* Little nose */}
          <ellipse cx="50" cy="52" rx="2.5" ry="1.5" fill="#1E1E24" />

          {/* Mouth shape based on state */}
          {state === "error" ? (
            // Frowny face
            <path
              d="M46 58 Q50 55 54 58"
              fill="none"
              stroke="#1E1E24"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          ) : state === "thinking" ? (
            // Straight/neutral face
            <line x1="45" y1="57" x2="55" y2="57" stroke="#1E1E24" strokeWidth="2.5" strokeLinecap="round" />
          ) : (
            // Smiling cat-like mouth (3 shape)
            <path
              d="M44 56 Q47 59 50 56 Q53 59 56 56"
              fill="none"
              stroke="#1E1E24"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          )}

          {/* Cute heart or blush mark for Alenia's winking icon signature */}
          {(state === "winking" || state === "success") && (
            <path
              d="M50 38 C49 35 45 35 45 38 C45 41 50 43 50 43 C50 43 55 41 55 38 C55 35 51 35 50 38 Z"
              fill="#F43F5E"
            />
          )}
        </motion.g>
      </motion.svg>
    </div>
  );
}
