'use client'

import { useState, useEffect } from 'react'
import { useSeason } from '@/lib/SeasonContext'
import { getTeamLogo, TEAM_COLORS } from '@/lib/teamLogos'
import Image from 'next/image'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, ReferenceLine } from 'recharts'

interface NFLData {
  season: number
  leagueStats: {
    totalPlays: number
    totalTouchdowns: number
    passingPlays: number
    rushingPlays: number
  }
  teamStats: Array<{
    team: string
    epaPerPlay: number
    totalEPA: number
    plays: number
    passEpaPerPlay: number
    passTotalEPA: number
    passPlays: number
    rushEpaPerPlay: number
    rushTotalEPA: number
    rushPlays: number
  }>
}

const NFL_TEAMS = [
  'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
  'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
  'LA', 'LAC', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
  'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
]

export default function TeamsPage() {
  const { season } = useSeason()
  const [selectedTeam, setSelectedTeam] = useState('KC')
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
        <div className="text-lg text-gray-500">Loading team data...</div>
      </div>
    )
  }

  const teamData = data.teamStats.find(t => t.team === selectedTeam)
  const teamRank = data.teamStats.findIndex(t => t.team === selectedTeam) + 1
  const teamColors = TEAM_COLORS[selectedTeam] || { primary: '#666', secondary: '#999' }

  return (
    <div className="space-y-8">
      <div
        className="flex justify-between items-center pb-6 border-b-2 transition-colors duration-500"
        style={{ borderBottomColor: teamColors.primary }}
      >
        <div className="flex items-center gap-4">
          <div
            className="rounded-full p-2 transition-colors duration-500"
            style={{ backgroundColor: `${teamColors.primary}20` }}
          >
            <Image
              src={getTeamLogo(selectedTeam)}
              alt={`${selectedTeam} logo`}
              width={60}
              height={60}
              className="object-contain"
            />
          </div>
          <h2 className="text-2xl">Team Analysis — {season} Season</h2>
        </div>
        <select
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          className="bg-background border border-gray-300 rounded-sm px-4 py-2 text-sm focus:outline-none focus:border-secondary"
        >
          {NFL_TEAMS.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>

      {teamData ? (
        <>
          <section>
            <h3 className="text-xl mb-4">Offensive Efficiency</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div
                className="metric-card transition-all duration-500"
                style={teamRank <= 10 ? {
                  backgroundColor: `${teamColors.primary}08`
                } : {}}
              >
                <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
                  League Rank
                </div>
                <div
                  className="text-3xl font-light transition-colors duration-500"
                  style={teamRank <= 5 ? { color: teamColors.primary } : {}}
                >
                  #{teamRank}
                </div>
              </div>
              <div
                className="metric-card transition-all duration-500"
                style={teamData.epaPerPlay > 0 ? {
                  borderColor: teamColors.primary,
                  borderWidth: '2px'
                } : {}}
              >
                <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
                  EPA/Play
                </div>
                <div
                  className="text-3xl font-light transition-colors duration-500"
                  style={teamData.epaPerPlay > 0.08 ? { color: teamColors.primary } : {}}
                >
                  <span className={teamData.epaPerPlay > 0.08 ? '' :
                    teamData.epaPerPlay > 0 ? 'text-yellow-600' : 'text-red-600'}>
                    {teamData.epaPerPlay.toFixed(3)}
                  </span>
                </div>
              </div>
              <div className="metric-card">
                <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
                  Total EPA
                </div>
                <div className="text-3xl font-light">{teamData.totalEPA.toFixed(1)}</div>
              </div>
              <div className="metric-card">
                <div className="text-sm uppercase tracking-wider text-gray-500 mb-2">
                  Total Plays
                </div>
                <div className="text-3xl font-light">{teamData.plays.toLocaleString()}</div>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-xl mb-4">Pass vs Rush Efficiency</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-surface border border-gray-200 rounded-sm p-6">
                <h4 className="text-sm uppercase tracking-wider text-gray-500 mb-4">EPA per Play Comparison</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={[
                    {
                      type: 'Pass',
                      EPA: Number(teamData.passEpaPerPlay.toFixed(3)),
                      plays: teamData.passPlays
                    },
                    {
                      type: 'Rush',
                      EPA: Number(teamData.rushEpaPerPlay.toFixed(3)),
                      plays: teamData.rushPlays
                    }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="type" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb' }}
                      formatter={(value: number, name: string, props: any) => [
                        `${value} (${props.payload.plays} plays)`,
                        'EPA/Play'
                      ]}
                    />
                    <Bar dataKey="EPA" fill={teamColors.primary} radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-surface border border-gray-200 rounded-sm p-6">
                <h4 className="text-sm uppercase tracking-wider text-gray-500 mb-4">Play Distribution</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Pass', value: teamData.passPlays, color: teamColors.primary },
                        { name: 'Rush', value: teamData.rushPlays, color: teamColors.secondary }
                      ]}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      dataKey="value"
                    >
                      <Cell fill={teamColors.primary} />
                      <Cell fill={teamColors.secondary} />
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-4 text-center text-sm text-gray-600">
                  {teamData.passPlays} pass plays · {teamData.rushPlays} rush plays
                </div>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-xl mb-4">League Standings</h3>
            <div className="bg-surface border border-gray-200 rounded-sm p-6">
              <ResponsiveContainer width="100%" height={1000}>
                <BarChart
                  data={data.teamStats.map((team, idx) => ({
                    team: team.team,
                    epaPerPlay: Number(team.epaPerPlay.toFixed(3)),
                    isSelected: team.team === selectedTeam
                  }))}
                  layout="vertical"
                  margin={{ left: 50, right: 20, top: 10, bottom: 10 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis type="number" stroke="#6b7280" />
                  <YAxis
                    type="category"
                    dataKey="team"
                    stroke="#6b7280"
                    width={45}
                    tick={{ fontSize: 12 }}
                    interval={0}
                  />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb' }}
                    formatter={(value: number) => [value, 'EPA/Play']}
                  />
                  <ReferenceLine
                    x={data.teamStats.reduce((sum, t) => sum + t.epaPerPlay, 0) / data.teamStats.length}
                    stroke="#9ca3af"
                    strokeDasharray="5 5"
                    strokeWidth={2}
                    label={{
                      value: 'League Avg',
                      position: 'insideTopRight',
                      fill: '#6b7280',
                      fontSize: 12
                    }}
                  />
                  <Bar
                    dataKey="epaPerPlay"
                    radius={[0, 4, 4, 0]}
                  >
                    {data.teamStats.map((team, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={team.team === selectedTeam ? teamColors.primary : '#d1d5db'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <p className="text-xs text-gray-500 mt-4 text-center">
                All 32 teams ranked by EPA/Play · {selectedTeam} highlighted · League average shown
              </p>
            </div>
          </section>

          <section className="bg-surface border border-gray-200 rounded-sm p-6">
            <div className="flex items-start gap-3">
              <div className="text-2xl">📊</div>
              <div>
                <h3 className="font-medium mb-2">Team Summary</h3>
                <p className="text-sm text-gray-700">
                  {selectedTeam} ranks #{teamRank} in offensive efficiency with an EPA per play of {teamData.epaPerPlay.toFixed(3)}.
                  They have run {teamData.plays.toLocaleString()} plays this season for a total EPA of {teamData.totalEPA.toFixed(1)}.
                </p>
                <p className="text-xs text-gray-500 mt-3">
                  Detailed passing and rushing stats coming in next update
                </p>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-xl mb-4">League Comparison</h3>
            <div className="bg-surface border border-gray-200 rounded-sm p-6">
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm text-gray-600">EPA/Play vs League Avg</span>
                    <span className="text-sm font-medium">
                      {((teamData.epaPerPlay / (data.teamStats.reduce((sum, t) => sum + t.epaPerPlay, 0) / data.teamStats.length) - 1) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${Math.min(Math.max((teamData.epaPerPlay / 0.25) * 100, 0), 100)}%`,
                        backgroundColor: teamData.epaPerPlay > 0.08 ? teamColors.primary : '#ca8a04'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </section>
        </>
      ) : (
        <div className="text-center py-12 text-gray-500">
          No data available for {selectedTeam}
        </div>
      )}
    </div>
  )
}
