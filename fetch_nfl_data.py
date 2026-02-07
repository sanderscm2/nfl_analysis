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

    # Calculate overall team stats
    team_stats = offensive_plays.groupby('posteam')['epa'].agg(['mean', 'sum', 'count']).reset_index()
    team_stats.columns = ['team', 'epaPerPlay', 'totalEPA', 'plays']

    # Calculate passing stats
    pass_plays = offensive_plays[offensive_plays['play_type'] == 'pass']
    pass_stats = pass_plays.groupby('posteam')['epa'].agg(['mean', 'sum', 'count']).reset_index()
    pass_stats.columns = ['team', 'passEpaPerPlay', 'passTotalEPA', 'passPlays']

    # Calculate rushing stats
    rush_plays = offensive_plays[offensive_plays['play_type'] == 'run']
    rush_stats = rush_plays.groupby('posteam')['epa'].agg(['mean', 'sum', 'count']).reset_index()
    rush_stats.columns = ['team', 'rushEpaPerPlay', 'rushTotalEPA', 'rushPlays']

    # Merge all stats
    team_stats = team_stats.merge(pass_stats, on='team', how='left')
    team_stats = team_stats.merge(rush_stats, on='team', how='left')

    # Fill NaN with 0
    team_stats = team_stats.fillna(0)

    team_stats = team_stats.sort_values('epaPerPlay', ascending=False)

    return team_stats.to_dict('records')

def calculate_player_stats(pbp, season):
    """Calculate player statistics for QB, RB, WR, TE"""
    player_stats = {
        'qb': [],
        'rb': [],
        'wr': [],
        'te': []
    }

    # Load roster data to get position information
    rosters = nfl.load_rosters(season)
    if hasattr(rosters, 'to_pandas'):
        rosters = rosters.to_pandas()

    # Create position lookup dictionary
    position_lookup = dict(zip(rosters['gsis_id'], rosters['position']))

    # Filter for offensive plays
    offensive_plays = pbp[
        (pbp['play_type'].isin(['pass', 'run'])) &
        (pbp['epa'].notna()) &
        ((pbp['penalty'] == 0) | (pbp['penalty'].isna()))
    ].copy()

    # QB stats (passing + rushing plays for QBs)
    # Get passing plays for QBs
    qb_pass_plays = offensive_plays[offensive_plays['passer_player_name'].notna()].copy()
    qb_pass_plays['position'] = qb_pass_plays['passer_player_id'].map(position_lookup)
    qb_pass_plays = qb_pass_plays[qb_pass_plays['position'] == 'QB'].copy()
    qb_pass_plays['player_name'] = qb_pass_plays['passer_player_name']
    qb_pass_plays['player_id'] = qb_pass_plays['passer_player_id']

    # Get rushing plays for QBs
    qb_rush_plays = offensive_plays[
        (offensive_plays['rusher_player_name'].notna()) &
        (offensive_plays['play_type'] == 'run')
    ].copy()
    qb_rush_plays['position'] = qb_rush_plays['rusher_player_id'].map(position_lookup)
    qb_rush_plays = qb_rush_plays[qb_rush_plays['position'] == 'QB'].copy()
    qb_rush_plays['player_name'] = qb_rush_plays['rusher_player_name']
    qb_rush_plays['player_id'] = qb_rush_plays['rusher_player_id']

    # Combine passing and rushing plays for QBs
    qb_all_plays = pd.concat([qb_pass_plays, qb_rush_plays])

    if len(qb_all_plays) > 0:
        # Calculate overall EPA (all plays)
        qb_overall = qb_all_plays.groupby('player_name').agg({
            'epa': ['mean', 'sum', 'count']
        }).reset_index()
        qb_overall.columns = ['player', 'epaPerPlay', 'totalEPA', 'plays']

        # Calculate passing stats
        if len(qb_pass_plays) > 0:
            qb_passing = qb_pass_plays.groupby('player_name').agg({
                'passing_yards': 'sum',
                'pass_touchdown': 'sum',
                'interception': 'sum',
                'complete_pass': 'sum',
                'pass_attempt': 'sum'
            }).reset_index()
            qb_passing.columns = ['player', 'passingYards', 'touchdowns', 'interceptions', 'completions', 'attempts']
            qb_grouped = qb_overall.merge(qb_passing, on='player', how='left')
        else:
            qb_grouped = qb_overall
            qb_grouped['passingYards'] = 0
            qb_grouped['touchdowns'] = 0
            qb_grouped['interceptions'] = 0
            qb_grouped['completions'] = 0
            qb_grouped['attempts'] = 0

        qb_grouped = qb_grouped.fillna(0)
        qb_grouped = qb_grouped[qb_grouped['plays'] >= 100]  # Min 100 plays
        qb_grouped = qb_grouped.sort_values('epaPerPlay', ascending=False)
        player_stats['qb'] = qb_grouped.head(50).to_dict('records')

    # RB stats (rusher with position = RB)
    rb_plays = offensive_plays[
        (offensive_plays['rusher_player_name'].notna()) &
        (offensive_plays['play_type'] == 'run')
    ].copy()
    rb_plays['position'] = rb_plays['rusher_player_id'].map(position_lookup)
    rb_plays = rb_plays[rb_plays['position'] == 'RB']

    if len(rb_plays) > 0:
        rb_grouped = rb_plays.groupby('rusher_player_name').agg({
            'epa': ['mean', 'sum', 'count'],
            'rushing_yards': 'sum',
            'rush_touchdown': 'sum'
        }).reset_index()
        rb_grouped.columns = ['player', 'epaPerPlay', 'totalEPA', 'plays', 'rushingYards', 'touchdowns']
        rb_grouped = rb_grouped[rb_grouped['plays'] >= 50]  # Min 50 plays
        rb_grouped = rb_grouped.sort_values('epaPerPlay', ascending=False)
        player_stats['rb'] = rb_grouped.head(50).to_dict('records')

    # WR stats (receiver with position = WR)
    wr_plays = offensive_plays[
        (offensive_plays['receiver_player_name'].notna()) &
        (offensive_plays['pass_attempt'] == 1)
    ].copy()
    wr_plays['position'] = wr_plays['receiver_player_id'].map(position_lookup)
    wr_plays = wr_plays[wr_plays['position'] == 'WR']

    if len(wr_plays) > 0:
        wr_grouped = wr_plays.groupby('receiver_player_name').agg({
            'epa': ['mean', 'sum', 'count'],
            'receiving_yards': 'sum',
            'pass_touchdown': 'sum',
            'complete_pass': 'sum'
        }).reset_index()
        wr_grouped.columns = ['player', 'epaPerPlay', 'totalEPA', 'targets', 'receivingYards', 'touchdowns', 'receptions']
        wr_grouped = wr_grouped[wr_grouped['targets'] >= 30]  # Min 30 targets
        wr_grouped = wr_grouped.sort_values('epaPerPlay', ascending=False)
        player_stats['wr'] = wr_grouped.head(50).to_dict('records')

    # TE stats (receiver with position = TE)
    te_plays = offensive_plays[
        (offensive_plays['receiver_player_name'].notna()) &
        (offensive_plays['pass_attempt'] == 1)
    ].copy()
    te_plays['position'] = te_plays['receiver_player_id'].map(position_lookup)
    te_plays = te_plays[te_plays['position'] == 'TE']

    if len(te_plays) > 0:
        te_grouped = te_plays.groupby('receiver_player_name').agg({
            'epa': ['mean', 'sum', 'count'],
            'receiving_yards': 'sum',
            'pass_touchdown': 'sum',
            'complete_pass': 'sum'
        }).reset_index()
        te_grouped.columns = ['player', 'epaPerPlay', 'totalEPA', 'targets', 'receivingYards', 'touchdowns', 'receptions']
        te_grouped = te_grouped[te_grouped['targets'] >= 30]  # Min 30 targets
        te_grouped = te_grouped.sort_values('epaPerPlay', ascending=False)
        player_stats['te'] = te_grouped.head(50).to_dict('records')

    return player_stats

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
    seasons = [2025, 2024, 2023, 2022, 2021, 2020]

    # Create output directory
    output_dir = Path(__file__).parent / 'web' / 'public' / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)

    for season in seasons:
        print(f"\n--- Processing {season} season ---")

        # Fetch data
        pbp = fetch_season_data(season)

        # Calculate stats
        team_stats = calculate_team_stats(pbp)
        player_stats = calculate_player_stats(pbp, season)
        league_stats = calculate_league_stats(pbp)

        # Prepare data structure
        data = {
            'season': season,
            'leagueStats': league_stats,
            'teamStats': team_stats,
            'playerStats': player_stats,
            'lastUpdated': pd.Timestamp.now().isoformat()
        }

        # Write JSON file
        output_file = output_dir / f'nfl_{season}.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Data exported to {output_file}")
        print(f"   Teams: {len(team_stats)}")
        print(f"   Total plays: {league_stats['totalPlays']:,}")
        print(f"   Top team: {team_stats[0]['team']} (EPA/Play: {team_stats[0]['epaPerPlay']:.3f})")

    print(f"\n✅ All seasons exported successfully!")

if __name__ == '__main__':
    main()
