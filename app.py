"""
NFL Analysis Dashboard
Interactive web app for exploring NFL statistics and trends
"""

import streamlit as st
import nflreadpy as nfl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="NFL Analysis Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #013369 0%, #D50A0A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #013369;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_pbp_data(season):
    """Load play-by-play data with caching"""
    try:
        pbp = nfl.load_pbp(season)
        # Convert Polars DataFrame to Pandas DataFrame
        if hasattr(pbp, 'to_pandas'):
            pbp = pbp.to_pandas()
        return pbp
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_team_stats(pbp, team):
    """Calculate team statistics"""
    team_plays = pbp[pbp['posteam'] == team].copy()

    # Passing stats
    passes = team_plays[team_plays['pass'] == 1]
    pass_stats = {
        'attempts': len(passes),
        'completions': passes['complete_pass'].sum(),
        'pass_yards': passes['yards_gained'].sum(),
        'pass_tds': passes['pass_touchdown'].sum(),
        'interceptions': passes['interception'].sum(),
    }
    if len(passes) > 0:
        pass_stats['completion_pct'] = (pass_stats['completions'] / pass_stats['attempts']) * 100
        pass_stats['yards_per_attempt'] = pass_stats['pass_yards'] / pass_stats['attempts']
        if 'epa' in passes.columns:
            pass_stats['pass_epa'] = passes['epa'].mean()

    # Rushing stats
    rushes = team_plays[team_plays['rush'] == 1]
    rush_stats = {
        'rush_attempts': len(rushes),
        'rush_yards': rushes['yards_gained'].sum(),
        'rush_tds': rushes['rush_touchdown'].sum(),
    }
    if len(rushes) > 0:
        rush_stats['yards_per_carry'] = rush_stats['rush_yards'] / rush_stats['rush_attempts']
        if 'epa' in rushes.columns:
            rush_stats['rush_epa'] = rushes['epa'].mean()

    return {**pass_stats, **rush_stats}

@st.cache_data
def get_all_teams_epa(pbp):
    """Calculate EPA for all teams"""
    if 'epa' not in pbp.columns:
        return None

    team_epa = pbp.groupby('posteam')['epa'].agg(['mean', 'sum', 'count']).reset_index()
    team_epa.columns = ['Team', 'EPA/Play', 'Total EPA', 'Plays']
    team_epa = team_epa.sort_values('EPA/Play', ascending=False)
    return team_epa

# Header
st.markdown('<h1 class="main-header">🏈 NFL Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # Season selection
    season = st.selectbox(
        "Select Season",
        options=[2024, 2023, 2022, 2021, 2020],
        index=0
    )

    st.markdown("---")

    # Team selection
    teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
             'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
             'LA', 'LAC', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
             'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS']

    selected_team = st.selectbox(
        "Select Team for Detailed Analysis",
        options=teams,
        index=teams.index('KC')
    )

    st.markdown("---")
    st.info("💡 This dashboard uses nflreadpy to fetch NFL play-by-play data and advanced metrics like EPA (Expected Points Added).")

# Load data
with st.spinner(f"Loading {season} season data..."):
    pbp = load_pbp_data(season)

if pbp is None:
    st.error("Failed to load data. Please try again.")
    st.stop()

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 League Overview", "🏟️ Team Analysis", "👤 Player Stats", "📈 Advanced Metrics"])

# Tab 1: League Overview
with tab1:
    st.header("League-Wide Statistics")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_plays = len(pbp)
        st.metric("Total Plays", f"{total_plays:,}")

    with col2:
        total_touchdowns = pbp['touchdown'].sum()
        st.metric("Total Touchdowns", f"{int(total_touchdowns):,}")

    with col3:
        passing_plays = (pbp['pass'] == 1).sum()
        st.metric("Passing Plays", f"{int(passing_plays):,}")

    with col4:
        rushing_plays = (pbp['rush'] == 1).sum()
        st.metric("Rushing Plays", f"{int(rushing_plays):,}")

    st.markdown("---")

    # Team EPA comparison
    st.subheader("Team Offensive Efficiency (EPA)")

    team_epa = get_all_teams_epa(pbp)

    if team_epa is not None:
        col1, col2 = st.columns(2)

        with col1:
            # EPA per play chart
            fig = px.bar(
                team_epa.head(15),
                x='EPA/Play',
                y='Team',
                orientation='h',
                title='Top 15 Offenses by EPA/Play',
                color='EPA/Play',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Total EPA chart
            fig = px.bar(
                team_epa.head(15),
                x='Total EPA',
                y='Team',
                orientation='h',
                title='Top 15 Offenses by Total EPA',
                color='Total EPA',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        # Full rankings table
        st.subheader("Complete Team Rankings")
        st.dataframe(
            team_epa.style.background_gradient(subset=['EPA/Play'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("EPA data not available for this season.")

# Tab 2: Team Analysis
with tab2:
    st.header(f"{selected_team} Team Analysis")

    team_stats = get_team_stats(pbp, selected_team)

    # Passing metrics
    st.subheader("🎯 Passing Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pass Attempts", f"{team_stats.get('attempts', 0):,}")
    with col2:
        st.metric("Completions", f"{team_stats.get('completions', 0):,}")
    with col3:
        st.metric("Completion %", f"{team_stats.get('completion_pct', 0):.1f}%")
    with col4:
        st.metric("Pass Yards", f"{team_stats.get('pass_yards', 0):,}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pass TDs", f"{team_stats.get('pass_tds', 0)}")
    with col2:
        st.metric("INTs", f"{team_stats.get('interceptions', 0)}")
    with col3:
        st.metric("Yards/Attempt", f"{team_stats.get('yards_per_attempt', 0):.2f}")
    with col4:
        if 'pass_epa' in team_stats:
            st.metric("EPA/Pass", f"{team_stats['pass_epa']:.3f}")

    st.markdown("---")

    # Rushing metrics
    st.subheader("🏃 Rushing Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rush Attempts", f"{team_stats.get('rush_attempts', 0):,}")
    with col2:
        st.metric("Rush Yards", f"{team_stats.get('rush_yards', 0):,}")
    with col3:
        st.metric("Rush TDs", f"{team_stats.get('rush_tds', 0)}")
    with col4:
        st.metric("Yards/Carry", f"{team_stats.get('yards_per_carry', 0):.2f}")

    if 'rush_epa' in team_stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("EPA/Rush", f"{team_stats['rush_epa']:.3f}")

# Tab 3: Player Stats
with tab3:
    st.header("Player Statistics")

    # Top QBs
    if 'epa' in pbp.columns and 'passer_player_name' in pbp.columns:
        st.subheader("🎯 Top Quarterbacks by EPA/Play")

        qb_stats = pbp[pbp['pass'] == 1].groupby('passer_player_name').agg({
            'epa': ['mean', 'count'],
            'yards_gained': 'sum',
            'pass_touchdown': 'sum',
            'interception': 'sum',
            'complete_pass': 'sum'
        }).reset_index()

        qb_stats.columns = ['Player', 'EPA/Play', 'Attempts', 'Pass Yards', 'TDs', 'INTs', 'Completions']
        qb_stats = qb_stats[qb_stats['Attempts'] >= 100]
        qb_stats['Comp %'] = (qb_stats['Completions'] / qb_stats['Attempts'] * 100).round(1)
        qb_stats = qb_stats.sort_values('EPA/Play', ascending=False).head(20)

        # QBs visualization
        fig = px.scatter(
            qb_stats.head(15),
            x='Attempts',
            y='EPA/Play',
            size='Pass Yards',
            color='TDs',
            hover_data=['Player', 'Comp %', 'INTs'],
            title='QB Performance: EPA/Play vs Attempts',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

        # QBs table
        st.dataframe(
            qb_stats[['Player', 'Attempts', 'Pass Yards', 'TDs', 'INTs', 'Comp %', 'EPA/Play']].style.background_gradient(subset=['EPA/Play'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )

    st.markdown("---")

    # Top RBs
    if 'epa' in pbp.columns and 'rusher_player_name' in pbp.columns:
        st.subheader("🏃 Top Running Backs by EPA/Rush")

        rb_stats = pbp[pbp['rush'] == 1].groupby('rusher_player_name').agg({
            'epa': ['mean', 'count'],
            'yards_gained': 'sum',
            'rush_touchdown': 'sum'
        }).reset_index()

        rb_stats.columns = ['Player', 'EPA/Rush', 'Attempts', 'Rush Yards', 'TDs']
        rb_stats = rb_stats[rb_stats['Attempts'] >= 50]
        rb_stats['Yards/Carry'] = (rb_stats['Rush Yards'] / rb_stats['Attempts']).round(2)
        rb_stats = rb_stats.sort_values('EPA/Rush', ascending=False).head(20)

        # RBs visualization
        fig = px.bar(
            rb_stats.head(15),
            x='Player',
            y='EPA/Rush',
            color='Yards/Carry',
            title='Top 15 Running Backs by EPA/Rush',
            color_continuous_scale='Blues',
            hover_data=['Attempts', 'Rush Yards', 'TDs']
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # RBs table
        st.dataframe(
            rb_stats[['Player', 'Attempts', 'Rush Yards', 'TDs', 'Yards/Carry', 'EPA/Rush']].style.background_gradient(subset=['EPA/Rush'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )

# Tab 4: Advanced Metrics
with tab4:
    st.header("Advanced Metrics & Insights")

    if 'epa' in pbp.columns:
        st.subheader("EPA Distribution")

        col1, col2 = st.columns(2)

        with col1:
            # Pass EPA distribution
            pass_epa = pbp[pbp['pass'] == 1]['epa'].dropna()
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=pass_epa, nbinsx=50, name='Pass EPA'))
            fig.update_layout(
                title='Passing EPA Distribution',
                xaxis_title='EPA',
                yaxis_title='Frequency',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Rush EPA distribution
            rush_epa = pbp[pbp['rush'] == 1]['epa'].dropna()
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=rush_epa, nbinsx=50, name='Rush EPA', marker_color='orange'))
            fig.update_layout(
                title='Rushing EPA Distribution',
                xaxis_title='EPA',
                yaxis_title='Frequency',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        # Win Probability
        if 'wp' in pbp.columns:
            st.subheader("Win Probability Trends")
            st.info("Select a specific game to see win probability chart")

    # Data export
    st.markdown("---")
    st.subheader("📥 Export Data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export Team Stats to CSV"):
            team_epa = get_all_teams_epa(pbp)
            if team_epa is not None:
                csv = team_epa.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"nfl_team_stats_{season}.csv",
                    mime="text/csv"
                )

    with col2:
        st.info("More export options coming soon!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with Streamlit | Data from nflverse | Season {}</p>
    <p>EPA (Expected Points Added) measures the value of a play based on expected points before and after the play</p>
</div>
""".format(season), unsafe_allow_html=True)
