'use client'

import { useState, useEffect } from 'react'
import { useSeason } from '@/lib/SeasonContext'

interface NFLData {
  season: number
  playerStats: {
    qb: Array<{
      player: string
      epaPerPlay: number
      totalEPA: number
      plays: number
      passingYards: number
      touchdowns: number
      interceptions: number
      completions: number
      attempts: number
    }>
    rb: Array<{
      player: string
      epaPerPlay: number
      totalEPA: number
      plays: number
      rushingYards: number
      touchdowns: number
    }>
    wr: Array<{
      player: string
      epaPerPlay: number
      totalEPA: number
      targets: number
      receivingYards: number
      touchdowns: number
      receptions: number
    }>
    te: Array<{
      player: string
      epaPerPlay: number
      totalEPA: number
      targets: number
      receivingYards: number
      touchdowns: number
      receptions: number
    }>
  }
}

type Position = 'all' | 'qb' | 'rb' | 'wr' | 'te' | 'flex'

const POSITION_LABELS = {
  all: 'All Positions',
  qb: 'Quarterbacks',
  rb: 'Running Backs',
  wr: 'Wide Receivers',
  te: 'Tight Ends',
  flex: 'Flex (RB/WR/TE)'
}

export default function PlayersPage() {
  const { season } = useSeason()
  const [position, setPosition] = useState<Position>('all')
  const [data, setData] = useState<NFLData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetch(`/data/nfl_${season}.json`)
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load NFL data:', err)
        setLoading(false)
      })
  }, [season])

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-lg text-gray-500">Loading player data...</div>
      </div>
    )
  }

  // Combine all players for "all" position view
  const getAllPlayers = () => {
    const allPlayers = [
      ...data.playerStats.qb.map(p => ({ ...p, position: 'QB' })),
      ...data.playerStats.rb.map(p => ({ ...p, position: 'RB' })),
      ...data.playerStats.wr.map(p => ({ ...p, position: 'WR' })),
      ...data.playerStats.te.map(p => ({ ...p, position: 'TE' }))
    ]
    return allPlayers.sort((a, b) => b.epaPerPlay - a.epaPerPlay).slice(0, 50)
  }

  // Combine flex players (RB, WR, TE)
  const getFlexPlayers = () => {
    const flexPlayers = [
      ...data.playerStats.rb.map(p => ({ ...p, position: 'RB' })),
      ...data.playerStats.wr.map(p => ({ ...p, position: 'WR' })),
      ...data.playerStats.te.map(p => ({ ...p, position: 'TE' }))
    ]
    return flexPlayers.sort((a, b) => b.epaPerPlay - a.epaPerPlay).slice(0, 50)
  }

  const players = position === 'all' ? getAllPlayers() :
                  position === 'flex' ? getFlexPlayers() :
                  data.playerStats[position]

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center pb-6 border-b-2 border-gray-300">
        <h2 className="text-2xl">Player Statistics — {season} Season</h2>
      </div>

      <div className="flex gap-2 border-b border-gray-200">
        {(Object.keys(POSITION_LABELS) as Position[]).map(pos => {
          const getBorderColor = () => {
            if (position !== pos) return ''
            switch (pos) {
              case 'qb': return 'border-purple-700'
              case 'rb': return 'border-green-700'
              case 'wr': return 'border-blue-700'
              case 'te': return 'border-orange-700'
              default: return 'border-gray-900'
            }
          }

          return (
            <button
              key={pos}
              onClick={() => setPosition(pos)}
              className={`px-6 py-3 text-sm uppercase tracking-wider transition-colors ${
                position === pos
                  ? `border-b-2 ${getBorderColor()} text-gray-900`
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {POSITION_LABELS[pos]}
            </button>
          )
        })}
      </div>

      <section>
        <div className="bg-surface border border-gray-200 rounded-sm overflow-hidden">
          {(position === 'all' || position === 'flex') && (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Rank</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Player</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Pos</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">EPA/Play</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Total EPA</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Plays</th>
                </tr>
              </thead>
              <tbody>
                {players.map((player: any, idx) => (
                  <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-500">#{idx + 1}</td>
                    <td className="py-3 px-4 font-medium">{player.player}</td>
                    <td className="py-3 px-4">
                      <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${
                        player.position === 'QB' ? 'bg-purple-100 text-purple-700' :
                        player.position === 'RB' ? 'bg-green-100 text-green-700' :
                        player.position === 'WR' ? 'bg-blue-100 text-blue-700' :
                        'bg-orange-100 text-orange-700'
                      }`}>
                        {player.position}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-mono">{player.epaPerPlay.toFixed(3)}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.totalEPA.toFixed(1)}</td>
                    <td className="py-3 px-4 text-right">{player.plays || player.targets}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {position === 'qb' && (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Rank</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Player</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">EPA/Play</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Total EPA</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Plays</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Yards</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">TD</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">INT</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Comp%</th>
                </tr>
              </thead>
              <tbody>
                {(players as NFLData['playerStats']['qb']).map((player, idx) => (
                  <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-500">#{idx + 1}</td>
                    <td className="py-3 px-4 font-medium">{player.player}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.epaPerPlay.toFixed(3)}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.totalEPA.toFixed(1)}</td>
                    <td className="py-3 px-4 text-right">{player.plays}</td>
                    <td className="py-3 px-4 text-right">{player.passingYards.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right">{player.touchdowns}</td>
                    <td className="py-3 px-4 text-right">{player.interceptions}</td>
                    <td className="py-3 px-4 text-right">{((player.completions / player.attempts) * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {position === 'rb' && (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Rank</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Player</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">EPA/Play</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Total EPA</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Carries</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Yards</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">YPC</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">TD</th>
                </tr>
              </thead>
              <tbody>
                {(players as NFLData['playerStats']['rb']).map((player, idx) => (
                  <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-500">#{idx + 1}</td>
                    <td className="py-3 px-4 font-medium">{player.player}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.epaPerPlay.toFixed(3)}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.totalEPA.toFixed(1)}</td>
                    <td className="py-3 px-4 text-right">{player.plays}</td>
                    <td className="py-3 px-4 text-right">{player.rushingYards.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right">{(player.rushingYards / player.plays).toFixed(1)}</td>
                    <td className="py-3 px-4 text-right">{player.touchdowns}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {(position === 'wr' || position === 'te') && (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Rank</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Player</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">EPA/Play</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Total EPA</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Targets</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Rec</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Catch%</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">Yards</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600 uppercase tracking-wider">TD</th>
                </tr>
              </thead>
              <tbody>
                {(players as NFLData['playerStats']['wr']).map((player, idx) => (
                  <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-500">#{idx + 1}</td>
                    <td className="py-3 px-4 font-medium">{player.player}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.epaPerPlay.toFixed(3)}</td>
                    <td className="py-3 px-4 text-right font-mono">{player.totalEPA.toFixed(1)}</td>
                    <td className="py-3 px-4 text-right">{player.targets}</td>
                    <td className="py-3 px-4 text-right">{player.receptions}</td>
                    <td className="py-3 px-4 text-right">{((player.receptions / player.targets) * 100).toFixed(1)}%</td>
                    <td className="py-3 px-4 text-right">{player.receivingYards.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right">{player.touchdowns}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="mt-4 text-sm text-gray-500">
          {position === 'all' && <p>Top 50 players across all positions · Sorted by EPA per play</p>}
          {position === 'flex' && <p>Top 50 skill position players (RB/WR/TE) · Sorted by EPA per play</p>}
          {position === 'qb' && <p>Minimum 100 pass attempts · Sorted by EPA per play</p>}
          {position === 'rb' && <p>Minimum 50 carries · Sorted by EPA per play</p>}
          {(position === 'wr' || position === 'te') && <p>Minimum 30 targets · Sorted by EPA per play</p>}
        </div>
      </section>

      <section className="bg-surface border border-gray-200 rounded-sm p-6">
        <div className="flex items-start gap-3">
          <div className="text-2xl">📊</div>
          <div>
            <h3 className="font-medium mb-2">About Player Statistics</h3>
            <p className="text-sm text-gray-700">
              EPA (Expected Points Added) measures a player's contribution to their team's expected points on each play.
              Higher EPA values indicate more efficient and impactful performance.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
