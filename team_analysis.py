"""
Team Performance Analysis
Analyze offensive and defensive performance by team
"""

import nflreadpy as nfl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(season=2024):
    """Load play-by-play data and prepare for analysis"""
    print(f"Loading {season} season data...")
    pbp = nfl.load_pbp(season)
    return pbp

def analyze_team_offense(pbp, team_abbr):
    """Analyze a team's offensive performance"""
    team_offense = pbp[pbp['posteam'] == team_abbr].copy()

    print(f"\n{'='*60}")
    print(f"{team_abbr} OFFENSIVE STATS")
    print(f"{'='*60}")

    # Overall stats
    total_plays = len(team_offense)
    print(f"Total plays: {total_plays:,}")

    # Passing stats
    passes = team_offense[team_offense['pass'] == 1]
    if len(passes) > 0:
        print(f"\nPassing:")
        print(f"  Attempts: {len(passes):,}")
        print(f"  Completions: {passes['complete_pass'].sum():,}")
        print(f"  Completion %: {(passes['complete_pass'].sum() / len(passes) * 100):.1f}%")
        print(f"  Total yards: {passes['yards_gained'].sum():,}")
        print(f"  Yards/attempt: {passes['yards_gained'].mean():.2f}")
        print(f"  TDs: {passes['pass_touchdown'].sum()}")
        print(f"  INTs: {passes['interception'].sum()}")

        if 'epa' in passes.columns:
            print(f"  EPA/play: {passes['epa'].mean():.3f}")

    # Rushing stats
    rushes = team_offense[team_offense['rush'] == 1]
    if len(rushes) > 0:
        print(f"\nRushing:")
        print(f"  Attempts: {len(rushes):,}")
        print(f"  Total yards: {rushes['yards_gained'].sum():,}")
        print(f"  Yards/attempt: {rushes['yards_gained'].mean():.2f}")
        print(f"  TDs: {rushes['rush_touchdown'].sum()}")

        if 'epa' in rushes.columns:
            print(f"  EPA/play: {rushes['epa'].mean():.3f}")

    return team_offense

def compare_all_teams(pbp):
    """Compare offensive efficiency across all teams"""
    print(f"\n{'='*60}")
    print("ALL TEAMS OFFENSIVE EFFICIENCY (EPA)")
    print(f"{'='*60}")

    # Calculate EPA by team
    if 'epa' in pbp.columns:
        team_epa = pbp.groupby('posteam')['epa'].agg(['mean', 'sum', 'count'])
        team_epa = team_epa.sort_values('mean', ascending=False)
        team_epa.columns = ['EPA/Play', 'Total EPA', 'Plays']

        print("\nTop 10 Offenses by EPA/Play:")
        print(team_epa.head(10))

        return team_epa
    else:
        print("EPA data not available")
        return None

def visualize_team_comparison(team_epa):
    """Create visualizations of team performance"""
    if team_epa is None:
        return

    # Set style
    sns.set_style("whitegrid")

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # EPA per play bar chart
    top_teams = team_epa.nlargest(15, 'EPA/Play')
    ax1.barh(range(len(top_teams)), top_teams['EPA/Play'])
    ax1.set_yticks(range(len(top_teams)))
    ax1.set_yticklabels(top_teams.index)
    ax1.set_xlabel('EPA per Play')
    ax1.set_title('Top 15 Offenses by EPA/Play')
    ax1.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

    # Total EPA bar chart
    top_teams_total = team_epa.nlargest(15, 'Total EPA')
    ax2.barh(range(len(top_teams_total)), top_teams_total['Total EPA'])
    ax2.set_yticks(range(len(top_teams_total)))
    ax2.set_yticklabels(top_teams_total.index)
    ax2.set_xlabel('Total EPA')
    ax2.set_title('Top 15 Offenses by Total EPA')

    plt.tight_layout()
    plt.savefig('team_epa_comparison.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualization saved as 'team_epa_comparison.png'")
    plt.close()

if __name__ == "__main__":
    # Load data
    pbp = load_and_prepare_data(2024)

    # Analyze a specific team (change to your favorite team)
    analyze_team_offense(pbp, 'KC')  # Kansas City Chiefs

    # Compare all teams
    team_epa = compare_all_teams(pbp)

    # Create visualizations
    if team_epa is not None:
        visualize_team_comparison(team_epa)

    print("\n✓ Analysis complete!")
