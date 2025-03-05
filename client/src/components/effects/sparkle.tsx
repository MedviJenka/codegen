import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface SparkleProps {
  color?: string;
}

const generateSparkles = (count: number) => {
  return Array.from({ length: count }, (_, i) => ({
    id: `sparkle-${i}`,
    scale: Math.random() * 0.6 + 0.4,
    x: (Math.random() - 0.5) * 100,
    y: (Math.random() - 0.5) * 100,
    rotation: Math.random() * 360
  }));
};

export const Sparkle = ({ color = '#FFF' }: SparkleProps) => {
  const [sparkles] = useState(() => generateSparkles(6));

  return (
    <div className="absolute inset-0 pointer-events-none">
      {sparkles.map((sparkle) => (
        <motion.div
          key={sparkle.id}
          initial={{ 
            scale: 0,
            opacity: 0,
            x: 0,
            y: 0,
            rotate: 0
          }}
          animate={{ 
            scale: [0, sparkle.scale, 0],
            opacity: [0, 1, 0],
            x: [0, sparkle.x, sparkle.x * 2],
            y: [0, sparkle.y, sparkle.y * 2],
            rotate: [0, sparkle.rotation, sparkle.rotation * 2]
          }}
          transition={{ 
            duration: 0.8,
            ease: "easeOut",
            times: [0, 0.5, 1]
          }}
          className="absolute left-1/2 top-1/2"
          style={{ originX: '50%', originY: '50%' }}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M10 0L12.2451 7.75491L20 10L12.2451 12.2451L10 20L7.75491 12.2451L0 10L7.75491 7.75491L10 0Z"
              fill={color}
            />
          </svg>
        </motion.div>
      ))}
    </div>
  );
};
