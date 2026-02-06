"""
Player Performance Analysis
Analyze individual player statistics and performance
"""

import nflreadpy as nfl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_season_data(season=2024):
    """Load play-by-play data for analysis"""
    print(f"Loading {season} season data...")
    pbp = nfl.load_pbp(season)
    return pbp

def analyze_quarterback(pbp, qb_name):
    """Analyze a quarterback's performance"""
    # Filter for plays where this QB was the passer
    qb_plays = pbp[pbp['passer_player_name'] == qb_name].copy()

    if len(qb_plays) == 0:
        print(f"No plays found for {qb_name}")
        return None

    print(f"\n{'='*60}")
    print(f"{qb_name} - QUARTERBACK STATS")
    print(f"{'='*60}")

    # Basic passing stats
    attempts = len(qb_plays)
    completions = qb_plays['complete_pass'].sum()
    yards = qb_plays['yards_gained'].sum()
    tds = qb_plays['pass_touchdown'].sum()
    ints = qb_plays['interception'].sum()

    print(f"\nPassing Stats:")
    print(f"  Attempts: {attempts:,}")
    print(f"  Completions: {completions:,}")
    print(f"  Completion %: {(completions / attempts * 100):.1f}%")
    print(f"  Yards: {yards:,}")
    print(f"  Yards/Attempt: {(yards / attempts):.2f}")
    print(f"  Touchdowns: {tds}")
    print(f"  Interceptions: {ints}")
    print(f"  TD/INT Ratio: {(tds / ints if ints > 0 else tds):.2f}")

    # Advanced metrics
    if 'epa' in qb_plays.columns:
        avg_epa = qb_plays['epa'].mean()
        total_epa = qb_plays['epa'].sum()
        print(f"\nAdvanced Metrics:")
        print(f"  EPA/Play: {avg_epa:.3f}")
        print(f"  Total EPA: {total_epa:.2f}")

    if 'cpoe' in qb_plays.columns:
        avg_cpoe = qb_plays['cpoe'].mean()
        print(f"  CPOE (Completion % Over Expected): {avg_cpoe:.1f}%")

    if 'air_yards' in qb_plays.columns:
        avg_air_yards = qb_plays['air_yards'].mean()
        print(f"  Average Air Yards: {avg_air_yards:.1f}")

    return qb_plays

def analyze_running_back(pbp, rb_name):
    """Analyze a running back's performance"""
    # Filter for rushing plays
    rb_rushes = pbp[pbp['rusher_player_name'] == rb_name].copy()

    # Also get receiving plays
    rb_targets = pbp[pbp['receiver_player_name'] == rb_name].copy()

    if len(rb_rushes) == 0 and len(rb_targets) == 0:
        print(f"No plays found for {rb_name}")
        return None

    print(f"\n{'='*60}")
    print(f"{rb_name} - RUNNING BACK STATS")
    print(f"{'='*60}")

    # Rushing stats
    if len(rb_rushes) > 0:
        attempts = len(rb_rushes)
        yards = rb_rushes['yards_gained'].sum()
        tds = rb_rushes['rush_touchdown'].sum()

        print(f"\nRushing Stats:")
        print(f"  Attempts: {attempts:,}")
        print(f"  Yards: {yards:,}")
        print(f"  Yards/Carry: {(yards / attempts):.2f}")
        print(f"  Touchdowns: {tds}")

        if 'epa' in rb_rushes.columns:
            print(f"  EPA/Rush: {rb_rushes['epa'].mean():.3f}")

    # Receiving stats
    if len(rb_targets) > 0:
        targets = len(rb_targets)
        receptions = rb_targets['complete_pass'].sum()
        rec_yards = rb_targets['yards_gained'].sum()
        rec_tds = rb_targets['pass_touchdown'].sum()

        print(f"\nReceiving Stats:")
        print(f"  Targets: {targets:,}")
        print(f"  Receptions: {receptions:,}")
        print(f"  Catch Rate: {(receptions / targets * 100):.1f}%")
        print(f"  Yards: {rec_yards:,}")
        print(f"  Yards/Reception: {(rec_yards / receptions if receptions > 0 else 0):.2f}")
        print(f"  Touchdowns: {rec_tds}")

    return {'rushes': rb_rushes, 'targets': rb_targets}

def top_players_by_position(pbp):
    """Find top performing players by position"""

    # Top QBs by EPA
    if 'epa' in pbp.columns:
        print(f"\n{'='*60}")
        print("TOP QUARTERBACKS BY EPA/PLAY")
        print(f"{'='*60}")

        qb_stats = pbp[pbp['pass'] == 1].groupby('passer_player_name').agg({
            'epa': ['mean', 'count'],
            'yards_gained': 'sum',
            'pass_touchdown': 'sum',
            'interception': 'sum'
        })

        # Filter QBs with at least 100 attempts
        qb_stats = qb_stats[qb_stats[('epa', 'count')] >= 100]
        qb_stats = qb_stats.sort_values(('epa', 'mean'), ascending=False)

        print("\nTop 10 QBs (min 100 attempts):")
        for idx, (name, row) in enumerate(qb_stats.head(10).iterrows(), 1):
            print(f"{idx:2d}. {name:25s} EPA/Play: {row[('epa', 'mean')]:.3f} ({int(row[('epa', 'count')])} att)")

        # Top RBs by EPA
        print(f"\n{'='*60}")
        print("TOP RUNNING BACKS BY EPA/RUSH")
        print(f"{'='*60}")

        rb_stats = pbp[pbp['rush'] == 1].groupby('rusher_player_name').agg({
            'epa': ['mean', 'count'],
            'yards_gained': 'sum',
            'rush_touchdown': 'sum'
        })

        # Filter RBs with at least 50 attempts
        rb_stats = rb_stats[rb_stats[('epa', 'count')] >= 50]
        rb_stats = rb_stats.sort_values(('epa', 'mean'), ascending=False)

        print("\nTop 10 RBs (min 50 attempts):")
        for idx, (name, row) in enumerate(rb_stats.head(10).iterrows(), 1):
            print(f"{idx:2d}. {name:25s} EPA/Rush: {row[('epa', 'mean')]:.3f} ({int(row[('epa', 'count')])} att)")

if __name__ == "__main__":
    # Load data
    pbp = load_season_data(2024)

    # Analyze specific players (change to your favorite players)
    analyze_quarterback(pbp, "P.Mahomes")
    analyze_running_back(pbp, "C.McCaffrey")

    # Show top players
    top_players_by_position(pbp)

    print("\n✓ Player analysis complete!")
