import type { Metadata } from 'next'
import './globals.css'
import Header from '@/components/layout/Header'
import Navigation from '@/components/layout/Navigation'

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
        <div className="min-h-screen flex flex-col">
          <Header />
          <Navigation />
          <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8">
            {children}
          </main>
          <footer className="border-t border-gray-200 py-8 px-4">
            <div className="max-w-7xl mx-auto text-sm text-gray-500">
              <p className="mb-1">Data: nflverse · Season 2025</p>
              <p>EPA: Expected Points Added</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
