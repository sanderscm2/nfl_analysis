'use client'

import { useSeason } from '@/lib/SeasonContext'

export default function Footer() {
  const { season } = useSeason()

  return (
    <footer className="border-t border-gray-200 py-8 px-4">
      <div className="max-w-7xl mx-auto text-sm text-gray-500">
        <p className="mb-1">Data: nflverse · Season {season}</p>
        <p>EPA: Expected Points Added</p>
      </div>
    </footer>
  )
}
