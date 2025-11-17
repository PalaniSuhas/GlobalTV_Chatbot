// components/Features.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

const features = [
  {
    icon: '🎯',
    title: 'AI-Powered Recommendations',
    description: 'Machine learning algorithms that understand your taste and suggest perfect content',
    gradient: 'from-blue-600/20 to-blue-600/5',
    highlight: 'from-blue-600 to-cyan-600'
  },
  {
    icon: '📱',
    title: 'Seamless Multi-Device',
    description: 'Start on TV, continue on mobile. Your progress syncs across all devices',
    gradient: 'from-purple-600/20 to-purple-600/5',
    highlight: 'from-purple-600 to-pink-600'
  },
  {
    icon: '⚡',
    title: 'Ultra-Fast Streaming',
    description: 'Adaptive bitrate technology ensures smooth 4K HDR playback',
    gradient: 'from-yellow-600/20 to-yellow-600/5',
    highlight: 'from-yellow-600 to-orange-600'
  },
  {
    icon: '👨‍👩‍👧‍👦',
    title: 'Family Profiles',
    description: 'Personalized experience for everyone with individual watchlists',
    gradient: 'from-green-600/20 to-green-600/5',
    highlight: 'from-green-600 to-teal-600'
  },
  {
    icon: '💾',
    title: 'Offline Downloads',
    description: 'Download your favorites and watch anywhere, even without internet',
    gradient: 'from-indigo-600/20 to-indigo-600/5',
    highlight: 'from-indigo-600 to-blue-600'
  },
  {
    icon: '🔒',
    title: 'Smart Parental Controls',
    description: 'Age-appropriate content filtering with PIN protection',
    gradient: 'from-red-600/20 to-red-600/5',
    highlight: 'from-red-600 to-rose-600'
  }
];

const stats = [
  { number: '10M+', label: 'Active Users', icon: '👥' },
  { number: '200+', label: 'Live Channels', icon: '📡' },
  { number: '10K+', label: 'Shows & Movies', icon: '🎬' },
  { number: '99.9%', label: 'Uptime', icon: '⚡' }
];

export default function Features() {
  const sectionRef = useRef(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-100px" });

  return (
    <section id="features" ref={sectionRef} className="py-32 px-6 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black" />
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"
      />

      <div className="relative z-10 max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={isInView ? { opacity: 1, scale: 1 } : {}}
            transition={{ delay: 0.2 }}
            className="inline-block mb-4"
          >
            <span className="px-6 py-2 bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-full text-blue-400 font-medium backdrop-blur-sm">
              ✨ Premium Features
            </span>
          </motion.div>

          <h2 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Everything You Need,
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 text-transparent bg-clip-text">
              Nothing You Don't
            </span>
          </h2>
          
          <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Experience the future of streaming with cutting-edge technology designed for your entertainment
          </p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.4, duration: 0.8 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-24"
        >
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={isInView ? { opacity: 1, scale: 1 } : {}}
              transition={{ delay: 0.5 + (i * 0.1) }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="p-6 rounded-2xl bg-gradient-to-br from-gray-800/50 to-gray-900/50 border border-gray-700 backdrop-blur-sm text-center"
            >
              <div className="text-4xl mb-3">{stat.icon}</div>
              <div className="text-3xl font-bold text-white mb-1">{stat.number}</div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-24">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 40 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.6 + (i * 0.1), duration: 0.6 }}
              whileHover={{ y: -12, scale: 1.02 }}
              className="group relative"
            >
              {/* Card */}
              <div className={`relative p-8 rounded-3xl bg-gradient-to-br ${feature.gradient} backdrop-blur-xl border border-gray-700 hover:border-gray-600 transition-all duration-500 overflow-hidden`}>
                {/* Hover Gradient Overlay */}
                <motion.div
                  className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                />

                {/* Content */}
                <div className="relative z-10">
                  <motion.div
                    animate={{
                      rotate: [0, 5, -5, 0]
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      repeatDelay: 2
                    }}
                    className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300"
                  >
                    {feature.icon}
                  </motion.div>

                  <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-300 transition-all">
                    {feature.title}
                  </h3>

                  <p className="text-gray-400 leading-relaxed mb-4">
                    {feature.description}
                  </p>

                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: '100%' }}
                    transition={{ delay: 1 + (i * 0.1), duration: 0.8 }}
                    className={`h-1 rounded-full bg-gradient-to-r ${feature.highlight}`}
                  />
                </div>

                {/* Shine Effect */}
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                  initial={{ x: '-100%' }}
                  whileHover={{ x: '100%' }}
                  transition={{ duration: 0.6 }}
                />
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 1.2, duration: 0.8 }}
          className="relative p-12 md:p-16 rounded-3xl bg-gradient-to-br from-blue-600/20 via-purple-600/20 to-pink-600/20 backdrop-blur-xl border border-gray-700 overflow-hidden"
        >
          {/* Animated Background */}
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 180, 360]
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear"
            }}
            className="absolute top-1/2 left-1/2 w-96 h-96 bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-full blur-3xl"
          />

          <div className="relative z-10 text-center">
            <h3 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Ready to Transform Your
              <br />
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 text-transparent bg-clip-text">
                Entertainment Experience?
              </span>
            </h3>

            <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Join millions streaming their favorite content in stunning quality
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="group relative px-10 py-5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full text-white text-lg font-bold overflow-hidden shadow-2xl"
              >
                <span className="relative z-10 flex items-center justify-center gap-3">
                  Start Your Free Trial
                  <motion.span
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    →
                  </motion.span>
                </span>
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600"
                  initial={{ x: '100%' }}
                  whileHover={{ x: 0 }}
                  transition={{ duration: 0.3 }}
                />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-10 py-5 bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 hover:border-white/40 rounded-full text-white text-lg font-bold transition-all"
              >
                View All Plans
              </motion.button>
            </div>

            <p className="mt-8 text-gray-400 text-sm">
              No credit card required • Cancel anytime • 30-day money-back guarantee
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}