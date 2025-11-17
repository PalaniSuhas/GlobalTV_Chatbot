// app/layout.tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Global TV - Premium Streaming Entertainment',
  description: 'Watch live TV, on-demand shows, and exclusive content on Global TV. 24/7 support available.',
  keywords: 'streaming, tv, entertainment, global tv, on-demand, live tv',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#0A0A0A" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}