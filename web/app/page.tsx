'use client'

import { useState, useEffect } from 'react'

interface TeamStat {
  team: string
  epaPerPlay: number
  totalEPA: number
  plays: number
}

interface NFLData {
  season: number
  leagueStats: {
    totalPlays: number
    totalTouchdowns: number
    passingPlays: number
    rushingPlays: number
  }
  teamStats: TeamStat[]
  lastUpdated: string
}

export default function Home() {
  const [data, setData] = useState<NFLData | null>(null)
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState<'epaPerPlay' | 'totalEPA'>('epaPerPlay')

  useEffect(() => {
    fetch('/data/nfl_2025.json')
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load NFL data:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-lg text-gray-500">Loading NFL data...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-lg text-red-500">Failed to load data</div>
      </div>
    )
  }

  const sortedTeams = [...data.teamStats].sort((a, b) => b[sortBy] - a[sortBy])

  return (
    <div className="space-y-8">
      {/* Hero Stats */}
      <section>
        <h2 className="text-2xl mb-6 pb-4 border-b border-gray-200">
          League Overview — 2025 Season
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="metric-card">
            <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
              Total Plays
            </div>
            <div className="text-3xl font-light">{data.leagueStats.totalPlays.toLocaleString()}</div>
          </div>
          <div className="metric-card">
            <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
              Total Touchdowns
            </div>
            <div className="text-3xl font-light">{data.leagueStats.totalTouchdowns.toLocaleString()}</div>
          </div>
          <div className="metric-card">
            <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
              Passing Plays
            </div>
            <div className="text-3xl font-light">{data.leagueStats.passingPlays.toLocaleString()}</div>
          </div>
          <div className="metric-card">
            <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
              Rushing Plays
            </div>
            <div className="text-3xl font-light">{data.leagueStats.rushingPlays.toLocaleString()}</div>
          </div>
        </div>
      </section>

      {/* AI Insights Placeholder */}
      <section className="bg-surface border border-gray-200 rounded-sm p-6">
        <div className="flex items-start gap-3">
          <div className="text-2xl">🤖</div>
          <div>
            <h3 className="font-medium mb-2">AI Insights</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>• {sortedTeams[0].team} leading league in EPA/play at {sortedTeams[0].epaPerPlay.toFixed(3)}</li>
              <li>• Total of {data.leagueStats.totalPlays.toLocaleString()} plays across all teams</li>
              <li>• Pass/Rush ratio: {(data.leagueStats.passingPlays / data.leagueStats.rushingPlays).toFixed(2)}:1</li>
            </ul>
            <p className="text-xs text-gray-500 mt-3">
              AI-powered insights will be enhanced in Phase 3
            </p>
          </div>
        </div>
      </section>

      {/* Team Rankings */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl">Team Offensive Efficiency</h2>
          <div className="flex gap-4">
            <button
              onClick={() => setSortBy('epaPerPlay')}
              className={`text-sm px-4 py-2 rounded-sm transition-colors ${
                sortBy === 'epaPerPlay'
                  ? 'bg-secondary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              EPA/Play
            </button>
            <button
              onClick={() => setSortBy('totalEPA')}
              className={`text-sm px-4 py-2 rounded-sm transition-colors ${
                sortBy === 'totalEPA'
                  ? 'bg-secondary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Total EPA
            </button>
          </div>
        </div>

        <div className="bg-surface border border-gray-200 rounded-sm overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-6 py-3 text-xs uppercase tracking-wider text-gray-500 font-normal">
                  Rank
                </th>
                <th className="text-left px-6 py-3 text-xs uppercase tracking-wider text-gray-500 font-normal">
                  Team
                </th>
                <th className="text-right px-6 py-3 text-xs uppercase tracking-wider text-gray-500 font-normal">
                  EPA/Play
                </th>
                <th className="text-right px-6 py-3 text-xs uppercase tracking-wider text-gray-500 font-normal">
                  Total EPA
                </th>
                <th className="text-right px-6 py-3 text-xs uppercase tracking-wider text-gray-500 font-normal">
                  Plays
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {sortedTeams.map((team, index) => (
                <tr key={team.team} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-gray-500">{index + 1}</td>
                  <td className="px-6 py-4 font-medium">{team.team}</td>
                  <td className="px-6 py-4 text-right">
                    <span
                      className={`inline-block px-3 py-1 rounded-sm text-sm ${
                        team.epaPerPlay > 0.08
                          ? 'bg-green-50 text-green-700'
                          : team.epaPerPlay > 0
                          ? 'bg-yellow-50 text-yellow-700'
                          : 'bg-red-50 text-red-700'
                      }`}
                    >
                      {team.epaPerPlay.toFixed(3)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">{team.totalEPA.toFixed(1)}</td>
                  <td className="px-6 py-4 text-right text-gray-500">{team.plays.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="text-xs text-gray-500 mt-4">
          Data from nflverse · Last updated: {new Date(data.lastUpdated).toLocaleDateString()}
        </p>
      </section>
    </div>
  )
}
