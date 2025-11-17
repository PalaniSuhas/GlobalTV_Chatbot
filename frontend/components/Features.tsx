// components/Features.tsx
'use client';

import { motion } from 'framer-motion';

const features = [
  {
    icon: '🎯',
    title: 'Personalized Recommendations',
    description: 'AI-powered suggestions based on your viewing habits'
  },
  {
    icon: '📱',
    title: 'Multi-Device Support',
    description: 'Watch on TV, mobile, tablet, or desktop seamlessly'
  },
  {
    icon: '⚡',
    title: 'Lightning Fast Streaming',
    description: 'Buffer-free HD streaming with adaptive quality'
  },
  {
    icon: '👨‍👩‍👧‍👦',
    title: 'Family Profiles',
    description: 'Create separate profiles for each family member'
  },
  {
    icon: '💾',
    title: 'Download & Watch Offline',
    description: 'Save your favorite shows to watch without internet'
  },
  {
    icon: '🔒',
    title: 'Parental Controls',
    description: 'Keep your kids safe with content restrictions'
  }
];

export default function Features() {
  return (
    <section id="features" className="py-20 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Why Choose Global TV?
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Experience entertainment like never before with our cutting-edge features
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="p-8 rounded-3xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all group"
            >
              <div className="text-5xl mb-4 group-hover:scale-110 transition-transform">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-400">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-20 p-12 rounded-3xl bg-gradient-to-br from-blue-600/20 to-purple-600/20 backdrop-blur-xl border border-white/10 text-center"
        >
          <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Start Watching?
          </h3>
          <p className="text-xl text-gray-300 mb-8">
            Join millions of happy viewers streaming their favorite content
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full text-lg font-medium transition-all transform hover:scale-105 shadow-lg shadow-blue-500/50">
              Start Free Trial
            </button>
            <button className="px-8 py-4 bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white rounded-full text-lg font-medium transition-all border border-white/20">
              View Plans
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}