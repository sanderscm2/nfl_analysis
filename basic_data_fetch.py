"""
Basic NFL Data Fetching Example
This script shows how to download and explore NFL play-by-play data
"""

import nflreadpy as nfl
import pandas as pd

def fetch_recent_season_data(season=2024):
    """Fetch play-by-play data for a season"""
    print(f"Fetching NFL data for {season} season...")

    # Load play-by-play data
    pbp = nfl.load_pbp(season)

    print(f"\nDataset shape: {pbp.shape}")
    print(f"Columns: {pbp.shape[1]}")
    print(f"Total plays: {pbp.shape[0]:,}")

    return pbp

def explore_data(pbp):
    """Explore the structure of the data"""
    print("\n" + "="*50)
    print("SAMPLE DATA")
    print("="*50)
    print(pbp.head())

    print("\n" + "="*50)
    print("COLUMN NAMES")
    print("="*50)
    print(pbp.columns.tolist())

    print("\n" + "="*50)
    print("DATA TYPES")
    print("="*50)
    print(pbp.dtypes)

def basic_stats(pbp):
    """Calculate some basic statistics"""
    print("\n" + "="*50)
    print("BASIC STATISTICS")
    print("="*50)

    # Passing plays
    passing_plays = pbp[pbp['pass'] == 1]
    print(f"Total passing plays: {len(passing_plays):,}")
    print(f"Average yards per pass: {passing_plays['yards_gained'].mean():.2f}")

    # Rushing plays
    rushing_plays = pbp[pbp['rush'] == 1]
    print(f"\nTotal rushing plays: {len(rushing_plays):,}")
    print(f"Average yards per rush: {rushing_plays['yards_gained'].mean():.2f}")

    # Touchdowns
    touchdowns = pbp[pbp['touchdown'] == 1]
    print(f"\nTotal touchdowns: {len(touchdowns):,}")

if __name__ == "__main__":
    # Fetch data for 2024 season
    pbp_data = fetch_recent_season_data(2024)

    # Explore the data
    explore_data(pbp_data)

    # Show basic statistics
    basic_stats(pbp_data)

    print("\n✓ Data fetch complete!")
