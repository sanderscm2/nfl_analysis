import type { Metadata } from 'next'
import './globals.css'
import { SeasonProvider } from '@/lib/SeasonContext'
import Header from '@/components/layout/Header'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  title: 'NFL Analytics Dashboard',
  description: 'Advanced NFL analytics powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <SeasonProvider>
          <div className="min-h-screen flex flex-col">
            <Header />
            <Navigation />
            <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8">
              {children}
            </main>
            <Footer />
          </div>
        </SeasonProvider>
      </body>
    </html>
  )
}
