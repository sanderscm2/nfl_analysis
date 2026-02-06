# 🏈 NFL Analysis Dashboard

A comprehensive Python project for analyzing NFL data with an interactive web dashboard. Built with the nflverse ecosystem, Streamlit, and modern data science tools.

## 🌟 Features

### Interactive Web Dashboard
- **League Overview**: Compare all teams by offensive efficiency (EPA)
- **Team Analysis**: Deep dive into any team's passing and rushing stats
- **Player Statistics**: Top QBs and RBs with interactive visualizations
- **Advanced Metrics**: EPA distributions and performance insights
- **Data Export**: Download analysis results as CSV
- **Multi-Season Support**: Analyze data from 2020-2024

### Python Analysis Scripts
- `basic_data_fetch.py` - Introduction to NFL play-by-play data
- `team_analysis.py` - Team comparisons and visualizations
- `player_analysis.py` - Individual player performance analysis

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
cd /Users/csanders/Documents/llm/nflanalysis
source venv/bin/activate
```

### 2. Run the Web Dashboard
```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501` with the full interactive dashboard!

### 3. Run Analysis Scripts (Optional)
```bash
python basic_data_fetch.py    # Explore data structure
python team_analysis.py        # Team comparisons with charts
python player_analysis.py      # Player stats and rankings
```

## 📁 Project Structure

```
nflanalysis/
├── app.py                    # 🌐 Main web dashboard (Streamlit)
├── basic_data_fetch.py       # 📊 Data exploration script
├── team_analysis.py          # 🏟️ Team comparison script
├── player_analysis.py        # 👤 Player analysis script
├── requirements.txt          # 📦 Python dependencies
├── README.md                 # 📖 This file
├── QUICKSTART.md            # ⚡ Quick start guide
├── DEPLOYMENT.md            # 🚀 Deployment instructions
├── .streamlit/
│   └── config.toml          # ⚙️ Streamlit configuration
└── venv/                    # 🐍 Virtual environment
```

## 🎯 What You Can Do

### Web Dashboard Features
1. **Explore League Stats**
   - View total plays, touchdowns, and play types
   - Compare all 32 NFL teams by EPA
   - Interactive charts with color gradients
   - Sortable data tables

2. **Analyze Any Team**
   - Select from 32 NFL teams
   - Passing stats: completions, yards, TDs, INTs, EPA
   - Rushing stats: carries, yards, TDs, yards/carry
   - Season-by-season comparison

3. **Player Performance**
   - Top quarterbacks ranked by EPA/Play
   - Running back efficiency metrics
   - Interactive scatter plots and bar charts
   - Filterable by minimum attempts

4. **Advanced Analytics**
   - EPA distribution histograms
   - Pass vs Rush efficiency comparison
   - Export data for further analysis

## 🔑 Key Metrics Explained

- **EPA (Expected Points Added)**: Measures play value (+EPA = good, -EPA = bad)
- **CPOE (Completion % Over Expected)**: QB accuracy vs expected given throw difficulty
- **Air Yards**: Distance ball traveled in air (measures aggressiveness)
- **Yards Per Attempt**: Passing efficiency metric
- **Yards Per Carry**: Rushing efficiency metric

## 🌐 Deploy to Web (FREE)

### Recommended: Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "NFL analysis dashboard"
   git remote add origin https://github.com/YOUR_USERNAME/nfl-analysis.git
   git push -u origin main
   ```

2. **Deploy**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app" → Select your repo
   - Click "Deploy"

3. **Share Your Live URL!**
   - Your app will be at: `https://YOUR_USERNAME-nfl-analysis.streamlit.app`
   - 100% FREE hosting
   - Automatic updates from GitHub

See `DEPLOYMENT.md` for other hosting options (Heroku, AWS, Docker, etc.)

## 🛠️ Technology Stack

- **Data**: nflreadpy, pandas, numpy
- **Visualization**: plotly, matplotlib, seaborn, altair
- **Web Framework**: Streamlit
- **Machine Learning**: scikit-learn
- **Interactive Analysis**: Jupyter notebooks

## 📊 Available Data

The nflverse ecosystem provides:
- ✅ Play-by-play data (1999-present)
- ✅ Advanced metrics (EPA, Win Probability, CPOE)
- ✅ Weekly player statistics
- ✅ Seasonal team stats
- ✅ Rosters and draft data
- ✅ Schedules and game results
- ✅ Next Gen Stats (tracking data)

## 🎨 Customization

### Change Default Team
Edit `app.py` line 112:
```python
index=teams.index('YOUR_TEAM')  # Change from 'KC'
```

### Add More Seasons
Edit `app.py` line 105:
```python
options=[2024, 2023, 2022, 2021, 2020, 2019, 2018]
```

### Customize Theme Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#013369"  # NFL blue - change to your team colors
```

## 🏈 Team Abbreviations

| AFC East | AFC North | AFC South | AFC West |
|----------|-----------|-----------|----------|
| BUF | BAL | HOU | DEN |
| MIA | CIN | IND | KC |
| NE | CLE | JAX | LAC |
| NYJ | PIT | TEN | LV |

| NFC East | NFC North | NFC South | NFC West |
|----------|-----------|-----------|----------|
| DAL | CHI | ATL | ARI |
| NYG | DET | CAR | LA |
| PHI | GB | NO | SEA |
| WAS | MIN | TB | SF |

## 📚 Resources

- [nflverse GitHub](https://github.com/nflverse) - Data source documentation
- [nflreadpy Documentation](https://pypi.org/project/nflreadpy/) - Python API
- [Streamlit Docs](https://docs.streamlit.io) - Web framework
- [NFL Data Dictionary](https://nflreadr.nflverse.com/articles/dictionary.html) - Column definitions
- [EPA Explainer](https://www.advancedfootballanalytics.com/index.php/home/stats/stats-explained/expected-points-and-epa-explained) - Understanding EPA

## 🤝 Contributing

Ideas for enhancements:
- Add defensive statistics
- Game-by-game win probability charts
- Player comparison tool
- Predictive modeling (playoff predictions, MVP predictions)
- Historical trend analysis
- Fantasy football projections
- Injury impact analysis

## 📝 License

Open source - feel free to use and modify for your own projects!

## 🎉 Next Steps

1. ✅ **Run the dashboard**: `streamlit run app.py`
2. ✅ **Explore different teams and seasons**
3. ✅ **Export data and create custom analyses**
4. ✅ **Deploy to web and share with friends**
5. ✅ **Extend with your own features**

**Happy analyzing! 🏈📊**
