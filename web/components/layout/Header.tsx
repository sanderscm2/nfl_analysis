'use client'

export default function Header() {
  const currentYear = new Date().getFullYear()
  const seasons = [2025, 2024, 2023, 2022, 2021, 2020]

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-normal tracking-tight">
          NFL Analytics
        </h1>
        <div className="flex items-center gap-4">
          <label htmlFor="season" className="text-sm text-gray-600 uppercase tracking-wider">
            Season
          </label>
          <select
            id="season"
            className="bg-background border border-gray-300 rounded-sm px-4 py-2 text-sm focus:outline-none focus:border-secondary"
            defaultValue={2025}
          >
            {seasons.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>
      </div>
    </header>
  )
}
