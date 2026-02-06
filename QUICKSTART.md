# Quick Start Guide 🚀

## Getting Started (5 minutes)

### 1. Activate Virtual Environment
```bash
cd /Users/csanders/Documents/llm/nflanalysis
source venv/bin/activate
```

### 2. Run the Web Dashboard
```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

### 3. Run the Analysis Scripts
```bash
# Basic data exploration
python basic_data_fetch.py

# Team analysis with visualizations
python team_analysis.py

# Player statistics
python player_analysis.py
```

---

## What You Built

### 🌐 **Interactive Web Dashboard** (`app.py`)
A full-featured Streamlit web application with:
- **League Overview**: See all teams ranked by offensive efficiency
- **Team Analysis**: Deep dive into any team's stats
- **Player Stats**: Top QBs and RBs with interactive charts
- **Advanced Metrics**: EPA distributions and insights
- **Data Export**: Download stats as CSV

**Features:**
- ✅ Interactive charts and filters
- ✅ Real-time data loading with caching
- ✅ Responsive design
- ✅ Professional NFL-themed styling
- ✅ Multiple seasons support

### 📊 **Analysis Scripts**
Three Python scripts for programmatic analysis:
- `basic_data_fetch.py` - Introduction to NFL data
- `team_analysis.py` - Team comparisons and EPA analysis
- `player_analysis.py` - Individual player performance

---

## NFL Dashboard Features

### Tab 1: League Overview
- Total plays, touchdowns, and play type breakdown
- Team EPA rankings with interactive charts
- Sortable data tables with color gradients

### Tab 2: Team Analysis
- Select any NFL team
- Comprehensive passing statistics
- Rushing performance metrics
- EPA per play breakdown

### Tab 3: Player Stats
- Top quarterbacks by EPA/Play
- Interactive scatter plots
- Running back performance rankings
- Minimum threshold filters (100 attempts for QBs, 50 for RBs)

### Tab 4: Advanced Metrics
- EPA distribution histograms
- Pass vs Rush efficiency comparison
- Data export functionality

---

## Customization

### Change Default Team
Edit `app.py` line ~112:
```python
selected_team = st.selectbox(
    "Select Team for Detailed Analysis",
    options=teams,
    index=teams.index('YOUR_TEAM')  # Change 'KC' to your team
)
```

### Add More Seasons
Edit `app.py` line ~105:
```python
season = st.selectbox(
    "Select Season",
    options=[2024, 2023, 2022, 2021, 2020, 2019, 2018],  # Add more years
    index=0
)
```

### Customize Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#013369"  # Change to your team colors
backgroundColor = "#FFFFFF"
```

---

## Deployment Options

### 🌟 Recommended: Streamlit Community Cloud (FREE)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Click Deploy
5. **Your app is live!** Share the URL

See `DEPLOYMENT.md` for detailed deployment guides.

---

## Project Structure

```
nflanalysis/
├── app.py                    # Main web dashboard
├── basic_data_fetch.py       # Data exploration script
├── team_analysis.py          # Team comparison script
├── player_analysis.py        # Player analysis script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── DEPLOYMENT.md             # Deployment guides
├── QUICKSTART.md             # This file
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── .gitignore               # Git ignore rules
└── venv/                    # Virtual environment
```

---

## Common Team Abbreviations

| Code | Team |
|------|------|
| KC   | Kansas City Chiefs |
| SF   | San Francisco 49ers |
| BUF  | Buffalo Bills |
| BAL  | Baltimore Ravens |
| PHI  | Philadelphia Eagles |
| DAL  | Dallas Cowboys |
| GB   | Green Bay Packers |
| NE   | New England Patriots |
| LAR  | Los Angeles Rams |
| MIA  | Miami Dolphins |

Full list in sidebar dropdown!

---

## Key Metrics Explained

**EPA (Expected Points Added)**
- Measures the value of a play
- Positive EPA = good play
- Negative EPA = bad play
- Average NFL play ≈ 0 EPA

**CPOE (Completion % Over Expected)**
- How much better/worse than expected
- Accounts for throw difficulty
- Positive CPOE = accurate passer

**Air Yards**
- Distance ball traveled in the air
- Measures downfield aggression
- Higher = more aggressive passing

---

## Next Steps

### 1. Explore the Dashboard
- Try different teams
- Compare seasons
- Export data

### 2. Deploy to Web
- Follow `DEPLOYMENT.md`
- Share with friends
- Get feedback

### 3. Extend Functionality
Ideas:
- Add game-by-game analysis
- Create win probability charts
- Build predictive models
- Add defensive statistics
- Compare players head-to-head

### 4. Contribute
- Fork on GitHub
- Add new features
- Share improvements

---

## Troubleshooting

### "Module not found" error
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### App won't load data
- Check internet connection
- Try a different season
- Clear Streamlit cache (press 'c' in terminal)

### Slow performance
- Use fewer seasons
- Increase cache settings
- Filter data more aggressively

---

## Resources

- [nflverse Documentation](https://github.com/nflverse)
- [Streamlit Documentation](https://docs.streamlit.io)
- [NFL Data Dictionary](https://nflreadr.nflverse.com/articles/dictionary.html)
- [EPA Explainer](https://www.advancedfootballanalytics.com/index.php/home/stats/stats-explained/expected-points-and-epa-explained)

---

## Support

Questions? Issues? Open an issue on GitHub or check the README.md

**Enjoy analyzing NFL data! 🏈**
