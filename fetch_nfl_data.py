"""
Fetch NFL data and export as JSON for the Next.js app
"""

import nflreadpy as nfl
import pandas as pd
import json
from pathlib import Path

def fetch_season_data(season=2025):
    """Fetch play-by-play data for a season"""
    print(f"Fetching {season} season data...")
    pbp = nfl.load_pbp(season)

    # Convert Polars to Pandas if needed
    if hasattr(pbp, 'to_pandas'):
        pbp = pbp.to_pandas()

    return pbp

def calculate_team_stats(pbp):
    """Calculate team offensive EPA stats"""
    # Filter for offensive plays only
    offensive_plays = pbp[
        (pbp['play_type'].isin(['pass', 'run'])) &
        (pbp['posteam'].notna()) &
        (pbp['epa'].notna()) &
        ((pbp['penalty'] == 0) | (pbp['penalty'].isna()))
    ].copy()

    # Filter to regular season only
    if 'season_type' in offensive_plays.columns:
        offensive_plays = offensive_plays[offensive_plays['season_type'] == 'REG']

    # Calculate team stats
    team_stats = offensive_plays.groupby('posteam')['epa'].agg(['mean', 'sum', 'count']).reset_index()
    team_stats.columns = ['team', 'epaPerPlay', 'totalEPA', 'plays']
    team_stats = team_stats.sort_values('epaPerPlay', ascending=False)

    return team_stats.to_dict('records')

def calculate_league_stats(pbp):
    """Calculate overall league statistics"""
    stats = {
        'totalPlays': len(pbp),
        'totalTouchdowns': int(pbp['touchdown'].sum()),
        'passingPlays': int((pbp['pass'] == 1).sum()),
        'rushingPlays': int((pbp['rush'] == 1).sum()),
    }
    return stats

def main():
    # Fetch 2025 data
    pbp = fetch_season_data(2025)

    # Calculate stats
    team_stats = calculate_team_stats(pbp)
    league_stats = calculate_league_stats(pbp)

    # Prepare data structure
    data = {
        'season': 2025,
        'leagueStats': league_stats,
        'teamStats': team_stats,
        'lastUpdated': pd.Timestamp.now().isoformat()
    }

    # Create output directory
    output_dir = Path(__file__).parent / 'web' / 'public' / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON file
    output_file = output_dir / 'nfl_2025.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Data exported to {output_file}")
    print(f"   Teams: {len(team_stats)}")
    print(f"   Total plays: {league_stats['totalPlays']:,}")
    print(f"   Top team: {team_stats[0]['team']} (EPA/Play: {team_stats[0]['epaPerPlay']:.3f})")

if __name__ == '__main__':
    main()
