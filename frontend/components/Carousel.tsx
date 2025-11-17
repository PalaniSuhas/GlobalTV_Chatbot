// components/Carousel.tsx
'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const slides = [
  {
    title: 'Premium Original Series',
    description: 'Exclusive content you can only watch on Global TV',
    gradient: 'from-blue-600/90 to-purple-600/90',
    image: '🎭'
  },
  {
    title: 'Live Sports Coverage',
    description: 'Never miss a game with our comprehensive sports channels',
    gradient: 'from-green-600/90 to-teal-600/90',
    image: '⚽'
  },
  {
    title: 'Breaking News 24/7',
    description: 'Stay informed with real-time news from around the world',
    gradient: 'from-red-600/90 to-orange-600/90',
    image: '📰'
  },
  {
    title: 'Kids & Family',
    description: 'Safe, entertaining content for the whole family',
    gradient: 'from-pink-600/90 to-rose-600/90',
    image: '👨‍👩‍👧‍👦'
  }
];

export default function Carousel() {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <section className="py-20 px-6">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-white text-center mb-16">
          What's On Global TV
        </h2>

        <div className="relative h-[500px] rounded-3xl overflow-hidden">
          <AnimatePresence mode="wait">
            <motion.div
              key={current}
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ duration: 0.5 }}
              className={`absolute inset-0 bg-gradient-to-br ${slides[current].gradient} backdrop-blur-xl`}
            >
              <div className="h-full flex items-center justify-between px-12">
                <div className="max-w-xl">
                  <motion.h3
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-5xl font-bold text-white mb-6"
                  >
                    {slides[current].title}
                  </motion.h3>
                  <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="text-xl text-white/90"
                  >
                    {slides[current].description}
                  </motion.p>
                </div>
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                  className="text-9xl hidden md:block"
                >
                  {slides[current].image}
                </motion.div>
              </div>
            </motion.div>
          </AnimatePresence>

          {/* Navigation dots */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-3 z-10">
            {slides.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrent(i)}
                className={`w-3 h-3 rounded-full transition-all ${
                  i === current 
                    ? 'bg-white w-8' 
                    : 'bg-white/40 hover:bg-white/60'
                }`}
              />
            ))}
          </div>

          {/* Navigation arrows */}
          <button
            onClick={() => setCurrent((prev) => (prev - 1 + slides.length) % slides.length)}
            className="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-all z-10"
          >
            ‹
          </button>
          <button
            onClick={() => setCurrent((prev) => (prev + 1) % slides.length)}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-all z-10"
          >
            ›
          </button>
        </div>
      </div>
    </section>
  );
}