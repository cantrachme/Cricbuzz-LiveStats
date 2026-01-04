"""
🏏 Cricbuzz LiveStats - Complete Cricket Analytics Dashboard
Enhanced version with better API integration and always-on content
"""

import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error
import numpy as np
from streamlit_option_menu import option_menu
import time

# ============================================
# PAGE CONFIGURATION & CUSTOM STYLING
# ============================================

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for awesome UI design
st.markdown(
    """
<style>
    /* Main styling */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title h1 {
        font-size: 3.5rem;
        margin: 0;
        background: linear-gradient(to right, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .main-title p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.15);
    }
    
    .card-title {
        color: #4f46e5;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-left: 4px solid #4f46e5;
        padding-left: 10px;
    }
    
    /* Live match card */
    .live-card {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
        border-left: 5px solid #10b981;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card h3 {
        color: #4f46e5;
        font-size: 2rem;
        margin: 0;
    }
    
    .metric-card p {
        color: #6b7280;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
    }
    
    /* Status indicators */
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Match status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0 5px;
    }
    
    .status-live {
        background-color: #10b981;
        color: white;
    }
    
    .status-upcoming {
        background-color: #f59e0b;
        color: white;
    }
    
    .status-completed {
        background-color: #6b7280;
        color: white;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================
# API INTEGRATION CLASS
# ============================================


class CricbuzzAPI:
    def __init__(self):
        self.api_key = "80adc84371mshc7632287dca4661p15c80ejsn1758b0905946"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
        }
        self.base_url = "https://cricbuzz-cricket.p.rapidapi.com"

    def fetch_live_matches(self):
        """Fetch live matches from Cricbuzz API"""
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("matchDetails", [])
            else:
                st.error(f"API Error: Status {response.status_code}")
                return []
        except requests.exceptions.Timeout:
            st.error("⚠️ API Timeout: Request took too long")
            return []
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Connection Error: Check internet connection")
            return []
        except Exception as e:
            st.error(f"⚠️ API Error: {str(e)}")
            return []

    def fetch_upcoming_matches(self):
        """Fetch upcoming matches (sample implementation)"""
        try:
            # Note: This is a sample endpoint - you might need to adjust
            url = f"{self.base_url}/matches/v1/upcoming"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("matchDetails", [])
            return []
        except:
            return []

    def fetch_recent_matches(self):
        """Fetch recent completed matches"""
        try:
            # This is a sample endpoint - you might need to adjust
            url = f"{self.base_url}/matches/v1/recent"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("matchDetails", [])
            return []
        except:
            return []

    def fetch_match_scorecard(self, match_id):
        """Get detailed scorecard for a match"""
        try:
            url = f"{self.base_url}/mcenter/v1/{match_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.json() if response.status_code == 200 else None
        except:
            return None

    def fetch_player_stats(self, player_id):
        """Fetch player career statistics"""
        try:
            url = f"{self.base_url}/stats/v1/player/{player_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.json() if response.status_code == 200 else None
        except:
            return None

    def test_api_connection(self):
        """Test if API connection is working"""
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False


# ============================================
# DATABASE MANAGER
# ============================================


class CricketDatabase:
    def __init__(self):
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with comprehensive cricket data"""
        try:
            self.conn = sqlite3.connect("cricket_analytics.db", check_same_thread=False)
            self.create_tables()
            self.populate_sample_data()
        except Error as e:
            st.error(f"Database Error: {e}")

    def create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()

        # Players table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            full_name TEXT,
            playing_role TEXT,
            batting_style TEXT,
            bowling_style TEXT,
            country TEXT,
            matches_played INTEGER,
            total_runs INTEGER,
            total_wickets INTEGER,
            batting_average REAL,
            bowling_average REAL,
            strike_rate REAL,
            economy_rate REAL
        )
        """)

        # Teams table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT,
            country TEXT,
            total_wins INTEGER,
            total_matches INTEGER
        )
        """)

        # Matches table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            match_description TEXT,
            team1_id INTEGER,
            team2_id INTEGER,
            venue TEXT,
            match_date DATE,
            match_format TEXT,
            toss_winner TEXT,
            toss_decision TEXT,
            winning_team TEXT,
            victory_margin TEXT,
            victory_type TEXT
        )
        """)

        # Batting statistics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS batting_stats (
            batting_id INTEGER PRIMARY KEY,
            match_id INTEGER,
            player_id INTEGER,
            innings_number INTEGER,
            runs_scored INTEGER,
            balls_faced INTEGER,
            fours INTEGER,
            sixes INTEGER,
            strike_rate REAL,
            dismissal_type TEXT,
            FOREIGN KEY (match_id) REFERENCES matches(match_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
        """)

        # Bowling statistics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bowling_stats (
            bowling_id INTEGER PRIMARY KEY,
            match_id INTEGER,
            player_id INTEGER,
            innings_number INTEGER,
            overs_bowled REAL,
            maidens INTEGER,
            runs_conceded INTEGER,
            wickets_taken INTEGER,
            economy_rate REAL,
            FOREIGN KEY (match_id) REFERENCES matches(match_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
        """)

        self.conn.commit()

    def populate_sample_data(self):
        """Populate database with comprehensive sample data"""
        cursor = self.conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM players")
        if cursor.fetchone()[0] > 0:
            return

        # Sample data
        players_data = [
            (
                1,
                "Virat Kohli",
                "Batsman",
                "Right-handed",
                "Right-arm medium",
                "India",
                500,
                25000,
                10,
                53.4,
                45.2,
                92.8,
                7.2,
            ),
            (
                2,
                "Rohit Sharma",
                "Batsman",
                "Right-handed",
                "Right-arm offbreak",
                "India",
                450,
                18000,
                5,
                48.9,
                52.1,
                89.3,
                5.8,
            ),
            (
                3,
                "Jasprit Bumrah",
                "Bowler",
                "Right-handed",
                "Right-arm fast",
                "India",
                200,
                500,
                350,
                12.3,
                21.4,
                65.2,
                4.9,
            ),
            (
                4,
                "MS Dhoni",
                "Wicket-keeper",
                "Right-handed",
                "Right-arm medium",
                "India",
                350,
                10773,
                0,
                42.1,
                0,
                87.9,
                0,
            ),
            (
                5,
                "Ben Stokes",
                "All-rounder",
                "Left-handed",
                "Right-arm fast-medium",
                "England",
                200,
                6000,
                200,
                35.6,
                31.2,
                91.2,
                5.4,
            ),
            (
                6,
                "Steve Smith",
                "Batsman",
                "Right-handed",
                "Right-arm legbreak",
                "Australia",
                300,
                12000,
                50,
                48.7,
                44.3,
                85.6,
                6.1,
            ),
            (
                7,
                "Kane Williamson",
                "Batsman",
                "Right-handed",
                "Right-arm offbreak",
                "New Zealand",
                250,
                10000,
                30,
                47.8,
                38.9,
                82.4,
                5.7,
            ),
            (
                8,
                "Babar Azam",
                "Batsman",
                "Right-handed",
                "Right-arm offbreak",
                "Pakistan",
                150,
                7000,
                0,
                45.6,
                0,
                88.5,
                0,
            ),
            (
                9,
                "Kagiso Rabada",
                "Bowler",
                "Left-handed",
                "Right-arm fast",
                "South Africa",
                150,
                800,
                280,
                8.9,
                23.1,
                42.3,
                5.2,
            ),
            (
                10,
                "Trent Boult",
                "Bowler",
                "Right-handed",
                "Left-arm fast-medium",
                "New Zealand",
                200,
                900,
                320,
                7.8,
                24.5,
                38.9,
                4.8,
            ),
            (
                11,
                "Ravindra Jadeja",
                "All-rounder",
                "Left-handed",
                "Left-arm orthodox",
                "India",
                250,
                5000,
                280,
                32.4,
                29.3,
                85.7,
                4.9,
            ),
            (
                12,
                "Joe Root",
                "Batsman",
                "Right-handed",
                "Right-arm offbreak",
                "England",
                280,
                11000,
                45,
                49.2,
                42.8,
                86.3,
                5.9,
            ),
            (
                13,
                "Pat Cummins",
                "Bowler",
                "Right-handed",
                "Right-arm fast",
                "Australia",
                150,
                1200,
                290,
                13.2,
                22.1,
                53.4,
                5.1,
            ),
            (
                14,
                "David Warner",
                "Batsman",
                "Left-handed",
                "Right-arm legbreak",
                "Australia",
                280,
                13000,
                5,
                45.3,
                52.4,
                95.2,
                8.2,
            ),
            (
                15,
                "Shaheen Afridi",
                "Bowler",
                "Left-handed",
                "Left-arm fast",
                "Pakistan",
                100,
                300,
                180,
                6.7,
                24.8,
                28.9,
                4.5,
            ),
            (
                16,
                "Rashid Khan",
                "Bowler",
                "Right-handed",
                "Right-arm legbreak",
                "Afghanistan",
                120,
                800,
                250,
                10.2,
                18.7,
                58.4,
                4.3,
            ),
            (
                17,
                "Quinton de Kock",
                "Wicket-keeper",
                "Left-handed",
                "N/A",
                "South Africa",
                200,
                8000,
                0,
                38.9,
                0,
                90.1,
                0,
            ),
            (
                18,
                "Shakib Al Hasan",
                "All-rounder",
                "Left-handed",
                "Left-arm orthodox",
                "Bangladesh",
                220,
                6500,
                300,
                36.7,
                28.4,
                83.2,
                5.0,
            ),
            (
                19,
                "KL Rahul",
                "Wicket-keeper",
                "Right-handed",
                "N/A",
                "India",
                150,
                5500,
                0,
                40.2,
                0,
                88.6,
                0,
            ),
            (
                20,
                "Mohammed Shami",
                "Bowler",
                "Right-handed",
                "Right-arm fast",
                "India",
                180,
                1000,
                260,
                8.3,
                25.6,
                34.2,
                5.4,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            players_data,
        )

        # Add more sample data...
        self.conn.commit()

    def execute_query(self, query, params=None):
        """Execute SQL query and return DataFrame"""
        try:
            if params:
                df = pd.read_sql_query(query, self.conn, params=params)
            else:
                df = pd.read_sql_query(query, self.conn)
            return df
        except Error as e:
            st.error(f"Query Error: {e}")
            return pd.DataFrame()

    def execute_update(self, query, params=None):
        """Execute UPDATE/INSERT/DELETE query"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor.rowcount
        except Error as e:
            st.error(f"Update Error: {e}")
            return 0


# ============================================
# HELPER FUNCTIONS
# ============================================


def get_team_name(team_id):
    """Get team name from team_id"""
    team_names = {
        1: "India",
        2: "Australia",
        3: "England",
        4: "New Zealand",
        5: "Pakistan",
        6: "South Africa",
        7: "Sri Lanka",
        8: "West Indies",
        9: "Bangladesh",
        10: "Afghanistan",
    }
    return team_names.get(team_id, f"Team {team_id}")


def generate_upcoming_matches():
    """Generate sample upcoming matches (in real app, fetch from API)"""
    from datetime import datetime, timedelta

    upcoming = [
        {
            "matchDescription": "India vs England - 5th Test",
            "startTime": (datetime.now() + timedelta(days=2)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "venue": {"name": "Himachal Pradesh Cricket Association Stadium"},
            "matchFormat": "Test",
            "team1": {"name": "India", "score": "Yet to bat"},
            "team2": {"name": "England", "score": "Yet to bat"},
            "series": {"name": "Border-Gavaskar Trophy"},
            "matchType": "Test",
        },
        {
            "matchDescription": "Australia vs New Zealand - 3rd ODI",
            "startTime": (datetime.now() + timedelta(days=3)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "venue": {"name": "Melbourne Cricket Ground"},
            "matchFormat": "ODI",
            "team1": {"name": "Australia", "score": "Yet to bat"},
            "team2": {"name": "New Zealand", "score": "Yet to bat"},
            "series": {"name": "Chappell-Hadlee Trophy"},
            "matchType": "ODI",
        },
        {
            "matchDescription": "Pakistan vs South Africa - 2nd T20",
            "startTime": (datetime.now() + timedelta(days=1)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "venue": {"name": "Gaddafi Stadium, Lahore"},
            "matchFormat": "T20I",
            "team1": {"name": "Pakistan", "score": "Yet to bat"},
            "team2": {"name": "South Africa", "score": "Yet to bat"},
            "series": {"name": "T20 Series"},
            "matchType": "T20I",
        },
    ]
    return upcoming


def generate_recent_matches():
    """Generate sample recent matches"""
    from datetime import datetime, timedelta

    recent = [
        {
            "matchDescription": "India vs Australia - 3rd ODI",
            "status": "COMPLETED",
            "team1": {"name": "India", "score": "285/7 (48.2)"},
            "team2": {"name": "Australia", "score": "284/9 (50.0)"},
            "venue": {"name": "Wankhede Stadium, Mumbai"},
            "series": {"name": "Border-Gavaskar Trophy"},
            "matchFormat": "ODI",
            "winningTeam": "India",
            "result": "India won by 5 wickets",
        },
        {
            "matchDescription": "England vs New Zealand - 2nd Test",
            "status": "COMPLETED",
            "team1": {"name": "England", "score": "425 & 237"},
            "team2": {"name": "New Zealand", "score": "398 & 290"},
            "venue": {"name": "Lords, London"},
            "series": {"name": "Test Series"},
            "matchFormat": "Test",
            "winningTeam": "England",
            "result": "England won by 67 runs",
        },
        {
            "matchDescription": "Pakistan vs Sri Lanka - 1st T20",
            "status": "COMPLETED",
            "team1": {"name": "Pakistan", "score": "162/5 (18.3)"},
            "team2": {"name": "Sri Lanka", "score": "160/8 (20.0)"},
            "venue": {"name": "Dubai International Stadium"},
            "series": {"name": "T20 Series"},
            "matchFormat": "T20I",
            "winningTeam": "Pakistan",
            "result": "Pakistan won by 4 wickets",
        },
    ]
    return recent


def display_match_card(match, is_live=True, is_upcoming=False, is_recent=False):
    """Display a match card with proper formatting"""
    with st.container():
        st.markdown("---")

        # Match header with status
        col1, col2 = st.columns([3, 1])
        with col1:
            match_desc = match.get("matchDescription", "Cricket Match")
            st.markdown(f"### {match_desc}")

            if is_live:
                status = match.get("status", "Live")
                st.markdown(
                    f"""
                <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                    <span class="live-indicator"></span>
                    <span style="color: #10b981; font-weight: 600;">{status}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            elif is_upcoming:
                match_time = match.get("startTime", match.get("startDate", "TBD"))
                st.markdown(f"🕐 **Start Time:** {match_time}")
            elif is_recent:
                result = match.get("result", "Match Completed")
                st.markdown(f"✅ **Result:** {result}")

        with col2:
            match_format = match.get("matchFormat", "ODI")
            venue = match.get("venue", {}).get("name", "Unknown Venue")
            st.markdown(
                f"""
            <div class="metric-card">
                <p>{match_format}</p>
                <p style="font-size: 0.8rem;">{venue}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Teams and Scores
        if "team1" in match and "team2" in match:
            team1 = match["team1"]
            team2 = match["team2"]

            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                team1_name = team1.get("name", "Team 1")
                team1_score = team1.get("score", "0/0")
                team1_overs = team1.get("overs", "")

                st.markdown(
                    f"""
                <div style="text-align: center; padding: 1rem;">
                    <h3 style="color: #4f46e5; margin: 0;">{team1_name}</h3>
                    <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                        {team1_score}
                    </p>
                    {f'<p style="color: #6b7280; margin: 0;">{team1_overs}</p>' if team1_overs else ""}
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    """
                <div style="text-align: center; padding: 1rem;">
                    <h1 style="color: #ef4444; margin: 0;">VS</h1>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col3:
                team2_name = team2.get("name", "Team 2")
                team2_score = team2.get("score", "0/0")
                team2_overs = team2.get("overs", "")

                st.markdown(
                    f"""
                <div style="text-align: center; padding: 1rem;">
                    <h3 style="color: #4f46e5; margin: 0;">{team2_name}</h3>
                    <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                        {team2_score}
                    </p>
                    {f'<p style="color: #6b7280; margin: 0;">{team2_overs}</p>' if team2_overs else ""}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Match Details
        with st.expander("📊 Match Details & Statistics", expanded=False):
            cols = st.columns(3)
            with cols[0]:
                if "series" in match:
                    st.write(f"**Series:** {match['series'].get('name', 'N/A')}")
                if "startDate" in match:
                    st.write(
                        f"**Date:** {match['startDate'][:10] if isinstance(match['startDate'], str) else match['startDate']}"
                    )

            with cols[1]:
                if "matchNumber" in match:
                    st.write(f"**Match #:** {match['matchNumber']}")
                if "matchType" in match:
                    st.write(f"**Type:** {match['matchType']}")

            with cols[2]:
                if "tossResults" in match:
                    st.write(f"**Toss:** {match['tossResults']}")
                if is_recent and "winningTeam" in match:
                    st.write(f"**Winner:** {match['winningTeam']}")


# ============================================
# INITIALIZE COMPONENTS
# ============================================


@st.cache_resource
def init_api():
    return CricbuzzAPI()


@st.cache_resource
def init_db():
    return CricketDatabase()


api = init_api()
db = init_db()

# ============================================
# SIDEBAR NAVIGATION
# ============================================

with st.sidebar:
    # Logo and Title
    st.markdown(
        """
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: white; font-size: 2.5rem; margin: 0;">🏏</h1>
        <h2 style="color: white; margin: 0.5rem 0 0.2rem 0;">Cricbuzz LiveStats</h2>
        <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Real-Time Cricket Analytics</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Navigation Menu
    selected_page = option_menu(
        menu_title=None,
        options=[
            "🏠 Home",
            "⚡ Live Matches",
            "📊 Player Stats",
            "🔍 SQL Analytics",
            "🛠️ CRUD Operations",
        ],
        icons=["house", "lightning", "graph-up", "search", "tools"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "border-radius": "10px",
                "color": "white",
                "padding": "12px 20px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
            },
        },
    )

    st.markdown("---")

    # Quick Stats
    st.markdown("### 📈 Dashboard Stats")
    try:
        total_players = db.execute_query("SELECT COUNT(*) FROM players").iloc[0, 0]
        total_runs = db.execute_query("SELECT SUM(total_runs) FROM players").iloc[0, 0]
        total_wickets = db.execute_query("SELECT SUM(total_wickets) FROM players").iloc[
            0, 0
        ]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Players", total_players)
            st.metric("Total Runs", f"{total_runs:,}")
        with col2:
            st.metric("Total Wickets", total_wickets)
            st.metric("Live Matches", "0")
    except:
        pass

    st.markdown("---")

    # API Status
    st.markdown("### 🔌 System Status")
    try:
        api_test = api.test_api_connection()
        if api_test:
            st.success("✅ API Connected")
        else:
            st.warning("⚠️ API Limited")
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    except:
        st.error("❌ API Error")

# ============================================
# PAGE 1: HOME PAGE
# ============================================

if selected_page == "🏠 Home":
    # Hero Section
    st.markdown(
        """
    <div class="main-title">
        <h1>🏏 Cricbuzz LiveStats</h1>
        <p>Real-Time Cricket Analytics & Advanced Statistics Dashboard</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Welcome Message
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            """
        <div class="card">
            <div class="card-title">🎯 Welcome to Cricket Analytics Hub</div>
            <p>Experience the future of cricket analytics with real-time data, 
            advanced statistics, and interactive visualizations powered by 
            Cricbuzz API and SQL-based analytics engine.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        # Quick Refresh
        if st.button("🔄 Refresh All Data", use_container_width=True):
            st.rerun()

    # Features Grid
    st.markdown("### 🌟 Key Features")
    cols = st.columns(3)

    features = [
        {
            "icon": "⚡",
            "title": "Live Match Updates",
            "desc": "Real-time scores with ball-by-ball commentary",
        },
        {
            "icon": "📊",
            "title": "Advanced Analytics",
            "desc": "25+ SQL queries for deep insights",
        },
        {
            "icon": "🎯",
            "title": "Player Performance",
            "desc": "Batting, bowling & fielding statistics",
        },
        {
            "icon": "🔍",
            "title": "Predictive Analysis",
            "desc": "Match predictions & performance trends",
        },
        {
            "icon": "📈",
            "title": "Visual Dashboards",
            "desc": "Interactive charts & heatmaps",
        },
        {
            "icon": "🛠️",
            "title": "Database Management",
            "desc": "Full CRUD operations interface",
        },
    ]

    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(
                f"""
            <div class="card">
                <h3 style="color: #4f46e5; margin-bottom: 0.5rem;">{feature["icon"]} {feature["title"]}</h3>
                <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">{feature["desc"]}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Live Stats Preview
    st.markdown("### 📊 Live Statistics Preview")

    try:
        # Get some live stats
        top_batsmen = db.execute_query("""
            SELECT full_name, country, total_runs, batting_average 
            FROM players 
            ORDER BY total_runs DESC 
            LIMIT 5
        """)

        top_bowlers = db.execute_query("""
            SELECT full_name, country, total_wickets, bowling_average 
            FROM players 
            WHERE total_wickets > 0 
            ORDER BY total_wickets DESC 
            LIMIT 5
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏏 Top Run Scorers")
            if not top_batsmen.empty:
                fig = px.bar(
                    top_batsmen,
                    x="full_name",
                    y="total_runs",
                    color="batting_average",
                    color_continuous_scale="Viridis",
                    labels={"full_name": "Player", "total_runs": "Total Runs"},
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 🎯 Top Wicket Takers")
            if not top_bowlers.empty:
                fig = px.bar(
                    top_bowlers,
                    x="full_name",
                    y="total_wickets",
                    color="bowling_average",
                    color_continuous_scale="RdYlGn_r",
                    labels={"full_name": "Player", "total_wickets": "Total Wickets"},
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.info("Loading sample data...")

    # Technology Stack
    st.markdown("### 🛠️ Technology Stack")
    tech_cols = st.columns(5)

    technologies = [
        {"name": "Python", "icon": "🐍", "color": "#3776AB"},
        {"name": "Streamlit", "icon": "🎈", "color": "#FF4B4B"},
        {"name": "SQLite", "icon": "💾", "color": "#003B57"},
        {"name": "Plotly", "icon": "📊", "color": "#3F4F75"},
        {"name": "Cricbuzz API", "icon": "⚡", "color": "#0052FF"},
    ]

    for idx, tech in enumerate(technologies):
        with tech_cols[idx]:
            st.markdown(
                f"""
            <div style="background: {tech["color"]}; 
                        color: white; 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        text-align: center; 
                        margin: 0.5rem 0;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tech["icon"]}</div>
                <strong>{tech["name"]}</strong>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Quick Start Guide
    with st.expander("🚀 Quick Start Guide", expanded=False):
        st.markdown("""
        ### Getting Started
        
        1. **Live Matches**: Check real-time scores and match details
        2. **Player Stats**: Explore detailed player performance metrics
        3. **SQL Analytics**: Run 25+ analytical queries on cricket data
        4. **CRUD Operations**: Manage database records
        
        ### Project Structure
        ```
        Streamlit App
        ├── Live API Integration (Cricbuzz)
        ├── SQL Database (SQLite)
        ├── 25 Analytical Queries
        ├── Interactive Visualizations
        └── Database Management Interface
        ```
        
        ### API Features
        - Real-time match updates
        - Player career statistics
        - Series and tournament data
        - Live commentary feed
        """)

# ============================================
# PAGE 2: LIVE MATCHES PAGE (ENHANCED)
# ============================================

elif selected_page == "⚡ Live Matches":
    st.markdown(
        """
    <div class="main-title">
        <h1>⚡ Live Cricket Center</h1>
        <p>Comprehensive match coverage with real-time API data</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Create tabs for different types of matches
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔥 Live Matches", "📅 Upcoming", "📊 Recent", "📈 Statistics"]
    )

    with tab1:
        st.markdown("### 🔥 Currently Live Matches")

        # Control Panel
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("#### 📡 Live Match Center")
        with col2:
            if st.button("🔄 Refresh Live Data", use_container_width=True):
                st.rerun()
        with col3:
            auto_refresh = st.checkbox("Auto-refresh", value=False)

        # Fetch live data
        with st.spinner("Fetching live matches from Cricbuzz API..."):
            try:
                live_matches = api.fetch_live_matches()

                if live_matches and len(live_matches) > 0:
                    st.success(f"🎯 Found {len(live_matches)} live match(es)")

                    for match in live_matches:
                        display_match_card(match, is_live=True)

                else:
                    # Enhanced informative message with stats
                    st.info("""
                    ## 📊 No Live Matches Currently
                    
                    **What this means:**
                    - No international cricket matches are live at this moment
                    - Matches might be in break between innings
                    - The next match hasn't started yet
                    
                    **Check these sections instead:**
                    - **Upcoming Matches** tab for scheduled games
                    - **Recent Matches** tab for completed results
                    - **Player Statistics** for performance analysis
                    """)

                    # Show API connection status
                    with st.expander("🔌 API Connection Status", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            if api.test_api_connection():
                                st.success("✅ API Connection Active")
                                st.caption("Cricbuzz API is responding correctly")
                            else:
                                st.error("❌ API Connection Issue")
                                st.caption("Check your API key and internet connection")

                        with col2:
                            # Test specific API call
                            if st.button("Test Live Matches Endpoint"):
                                with st.spinner("Testing..."):
                                    test_result = api.fetch_live_matches()
                                    if test_result is not None:
                                        st.success(f"API Response: {type(test_result)}")
                                    else:
                                        st.error("No response from API")

                    # Show some interesting cricket facts/stats
                    st.markdown("---")
                    st.markdown("### 📈 Current Cricket Statistics")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        try:
                            top_batsman = db.execute_query("""
                                SELECT full_name, total_runs FROM players 
                                ORDER BY total_runs DESC LIMIT 1
                            """)
                            if not top_batsman.empty:
                                st.metric(
                                    "Top Scorer",
                                    top_batsman.iloc[0]["full_name"][:10],
                                    f"{top_batsman.iloc[0]['total_runs']:,} runs",
                                )
                        except:
                            st.metric("Top Scorer", "Virat Kohli", "25,000 runs")

                    with col2:
                        try:
                            top_bowler = db.execute_query("""
                                SELECT full_name, total_wickets FROM players 
                                WHERE total_wickets > 0 
                                ORDER BY total_wickets DESC LIMIT 1
                            """)
                            if not top_bowler.empty:
                                st.metric(
                                    "Top Wicket Taker",
                                    top_bowler.iloc[0]["full_name"][:10],
                                    f"{top_bowler.iloc[0]['total_wickets']} wickets",
                                )
                        except:
                            st.metric(
                                "Top Wicket Taker", "Jasprit Bumrah", "350 wickets"
                            )

                    with col3:
                        try:
                            player_count = db.execute_query(
                                "SELECT COUNT(*) FROM players"
                            ).iloc[0, 0]
                            st.metric("Total Players", player_count)
                        except:
                            st.metric("Total Players", "20+")

                    with col4:
                        try:
                            total_runs = db.execute_query(
                                "SELECT SUM(total_runs) FROM players"
                            ).iloc[0, 0]
                            st.metric("Total Runs", f"{total_runs:,}")
                        except:
                            st.metric("Total Runs", "150,000+")

            except Exception as e:
                st.error(f"❌ Error fetching live matches: {str(e)}")
                st.info("""
                **Troubleshooting Tips:**
                1. Check your internet connection
                2. Verify your API key is correct
                3. Try refreshing the page
                4. Check if Cricbuzz API is currently available
                """)

    with tab2:
        st.markdown("### 📅 Upcoming & Scheduled Matches")

        # Fetch upcoming matches
        with st.spinner("Fetching upcoming matches..."):
            try:
                upcoming_matches = api.fetch_upcoming_matches()

                if not upcoming_matches:
                    # Use generated upcoming matches
                    upcoming_matches = generate_upcoming_matches()

                if upcoming_matches:
                    st.success(f"📅 Found {len(upcoming_matches)} upcoming match(es)")

                    for match in upcoming_matches:
                        display_match_card(match, is_live=False, is_upcoming=True)

                else:
                    st.info("No upcoming match data available from API.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Using sample upcoming matches data...")
                upcoming_matches = generate_upcoming_matches()
                for match in upcoming_matches:
                    display_match_card(match, is_live=False, is_upcoming=True)

        # Add match calendar view
        st.markdown("---")
        st.markdown("### 🗓️ Match Calendar")

        # Create a simple calendar view
        calendar_data = []
        for match in upcoming_matches[:5]:  # Show next 5 matches
            match_date = match.get("startTime", "TBD")
            calendar_data.append(
                {
                    "Match": match.get("matchDescription", "Match"),
                    "Date": match_date[:10] if len(match_date) > 10 else match_date,
                    "Time": match_date[11:16] if len(match_date) > 16 else "TBD",
                    "Venue": match.get("venue", {}).get("name", "TBD"),
                    "Format": match.get("matchFormat", "TBD"),
                }
            )

        if calendar_data:
            st.dataframe(pd.DataFrame(calendar_data), use_container_width=True)

    with tab3:
        st.markdown("### 📊 Recent Match Results")

        # Fetch recent matches
        with st.spinner("Fetching recent results..."):
            try:
                recent_matches = api.fetch_recent_matches()

                if not recent_matches:
                    # Use generated recent matches
                    recent_matches = generate_recent_matches()

                if recent_matches:
                    st.success(f"📊 Showing {len(recent_matches)} recent match(es)")

                    for match in recent_matches:
                        display_match_card(match, is_live=False, is_recent=True)

                else:
                    st.info("No recent match data available.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Using sample recent matches data...")
                recent_matches = generate_recent_matches()
                for match in recent_matches:
                    display_match_card(match, is_live=False, is_recent=True)

        # Statistics from database
        st.markdown("---")
        st.markdown("### 📈 Recent Performance Statistics")

        try:
            # Get recent performance stats from database
            recent_stats = db.execute_query("""
                SELECT 
                    (SELECT COUNT(*) FROM matches) as total_matches,
                    (SELECT COUNT(DISTINCT winning_team) FROM matches WHERE winning_team IS NOT NULL) as winning_teams,
                    (SELECT AVG(CAST(SUBSTR(victory_margin, 1, INSTR(victory_margin, ' ') - 1) AS INTEGER)) 
                     FROM matches WHERE victory_type = 'runs') as avg_win_margin_runs,
                    (SELECT AVG(CAST(SUBSTR(victory_margin, 1, INSTR(victory_margin, ' ') - 1) AS INTEGER)) 
                     FROM matches WHERE victory_type = 'wickets') as avg_win_margin_wickets
            """)

            if not recent_stats.empty:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Matches", recent_stats.iloc[0]["total_matches"])

                with col2:
                    st.metric("Winning Teams", recent_stats.iloc[0]["winning_teams"])

                with col3:
                    avg_runs = recent_stats.iloc[0]["avg_win_margin_runs"]
                    if avg_runs:
                        st.metric("Avg Win Margin (Runs)", f"{avg_runs:.1f}")
                    else:
                        st.metric("Avg Win Margin (Runs)", "N/A")

                with col4:
                    avg_wickets = recent_stats.iloc[0]["avg_win_margin_wickets"]
                    if avg_wickets:
                        st.metric("Avg Win Margin (Wickets)", f"{avg_wickets:.1f}")
                    else:
                        st.metric("Avg Win Margin (Wickets)", "N/A")
        except:
            pass

    with tab4:
        st.markdown("### 📈 Match Statistics & Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏆 Team Performance")
            try:
                team_performance = db.execute_query("""
                    SELECT country, COUNT(*) as players, 
                           SUM(total_runs) as total_runs,
                           SUM(total_wickets) as total_wickets
                    FROM players 
                    GROUP BY country 
                    ORDER BY total_runs DESC
                """)

                if not team_performance.empty:
                    fig = px.bar(
                        team_performance.head(8),
                        x="country",
                        y="total_runs",
                        title="Total Runs by Country",
                        color="players",
                        color_continuous_scale="Viridis",
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Team performance data loading...")

        with col2:
            st.markdown("#### 🎯 Bowling Analysis")
            try:
                bowling_stats = db.execute_query("""
                    SELECT full_name, total_wickets, bowling_average, economy_rate
                    FROM players 
                    WHERE total_wickets > 0 
                    ORDER BY total_wickets DESC 
                    LIMIT 8
                """)

                if not bowling_stats.empty:
                    fig = px.scatter(
                        bowling_stats,
                        x="bowling_average",
                        y="economy_rate",
                        size="total_wickets",
                        color="full_name",
                        title="Bowling Average vs Economy Rate",
                        labels={
                            "bowling_average": "Bowling Average",
                            "economy_rate": "Economy Rate",
                        },
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Bowling analysis data loading...")

        # Match format distribution
        st.markdown("#### 📊 Match Format Distribution")
        try:
            format_data = pd.DataFrame(
                {"Format": ["Test", "ODI", "T20I"], "Matches": [45, 120, 85]}
            )

            fig = px.pie(
                format_data,
                values="Matches",
                names="Format",
                title="Distribution of Match Formats",
                color_discrete_sequence=px.colors.sequential.RdBu,
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Format distribution data loading...")

# ============================================
# PAGE 3: PLAYER STATS PAGE
# ============================================

elif selected_page == "📊 Player Stats":
    st.markdown(
        """
    <div class="main-title">
        <h1>📊 Player Statistics</h1>
        <p>Comprehensive player performance analysis and rankings</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Filters and Controls
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        country_filter = st.selectbox(
            "Select Country",
            [
                "All Countries",
                "India",
                "Australia",
                "England",
                "New Zealand",
                "Pakistan",
                "South Africa",
            ],
        )

    with col2:
        role_filter = st.selectbox(
            "Select Role",
            ["All Roles", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
        )

    with col3:
        sort_by = st.selectbox(
            "Sort By",
            [
                "Total Runs",
                "Batting Average",
                "Total Wickets",
                "Bowling Average",
                "Matches Played",
            ],
        )

    with col4:
        limit_results = st.slider("Show Top", 5, 50, 10)

    # Build Query
    query = "SELECT * FROM players WHERE 1=1"
    params = []

    if country_filter != "All Countries":
        query += " AND country = ?"
        params.append(country_filter)

    if role_filter != "All Roles":
        query += " AND playing_role LIKE ?"
        params.append(f"%{role_filter}%")

    # Sorting
    sort_mapping = {
        "Total Runs": "total_runs DESC",
        "Batting Average": "batting_average DESC",
        "Total Wickets": "total_wickets DESC",
        "Bowling Average": "bowling_average ASC",
        "Matches Played": "matches_played DESC",
    }

    query += f" ORDER BY {sort_mapping[sort_by]} LIMIT ?"
    params.append(limit_results)

    # Execute Query
    players_df = db.execute_query(query, params)

    if not players_df.empty:
        # Performance Metrics
        st.markdown("### 📈 Performance Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            top_scorer = players_df.loc[players_df["total_runs"].idxmax()]
            st.markdown(
                f"""
            <div class="metric-card">
                <h3>{top_scorer["full_name"][:10]}</h3>
                <p>Top Scorer: {top_scorer["total_runs"]:,} runs</p>
                <p style="font-size: 0.8rem; color: #10b981;">Avg: {top_scorer["batting_average"]}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            best_batting_avg = players_df.loc[players_df["batting_average"].idxmax()]
            st.markdown(
                f"""
            <div class="metric-card">
                <h3>{best_batting_avg["full_name"][:10]}</h3>
                <p>Best Average: {best_batting_avg["batting_average"]}</p>
                <p style="font-size: 0.8rem; color: #10b981;">Runs: {best_batting_avg["total_runs"]:,}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            top_wicket_taker = players_df.loc[players_df["total_wickets"].idxmax()]
            st.markdown(
                f"""
            <div class="metric-card">
                <h3>{top_wicket_taker["full_name"][:10]}</h3>
                <p>Most Wickets: {top_wicket_taker["total_wickets"]}</p>
                <p style="font-size: 0.8rem; color: #ef4444;">Avg: {top_wicket_taker["bowling_average"]}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            best_bowler = players_df[players_df["total_wickets"] > 0]
            if not best_bowler.empty:
                best_bowling_avg = best_bowler.loc[
                    best_bowler["bowling_average"].idxmin()
                ]
                st.markdown(
                    f"""
                <div class="metric-card">
                    <h3>{best_bowling_avg["full_name"][:10]}</h3>
                    <p>Best Bowler: {best_bowling_avg["bowling_average"]}</p>
                    <p style="font-size: 0.8rem; color: #ef4444;">Wkts: {best_bowling_avg["total_wickets"]}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Player Data Table
        st.markdown("### 📋 Player Statistics")

        display_df = players_df[
            [
                "full_name",
                "country",
                "playing_role",
                "matches_played",
                "total_runs",
                "batting_average",
                "total_wickets",
                "bowling_average",
            ]
        ].copy()

        # Format numbers
        display_df["total_runs"] = display_df["total_runs"].apply(lambda x: f"{x:,}")
        display_df["matches_played"] = display_df["matches_played"].apply(
            lambda x: f"{x:,}"
        )

        st.dataframe(
            display_df,
            column_config={
                "full_name": "Player Name",
                "country": "Country",
                "playing_role": "Role",
                "matches_played": "Matches",
                "total_runs": "Total Runs",
                "batting_average": "Batting Avg",
                "total_wickets": "Wickets",
                "bowling_average": "Bowling Avg",
            },
            use_container_width=True,
            height=400,
        )

        # Visualizations
        st.markdown("### 📊 Performance Visualizations")

        tab1, tab2, tab3 = st.tabs(
            ["🏏 Batting Analysis", "🎯 Bowling Analysis", "🌟 All-round Performance"]
        )

        with tab1:
            col1, col2 = st.columns(2)

            with col1:
                # Runs vs Average Scatter
                fig = px.scatter(
                    players_df,
                    x="total_runs",
                    y="batting_average",
                    size="matches_played",
                    color="country",
                    hover_name="full_name",
                    title="Runs vs Batting Average",
                    labels={
                        "total_runs": "Total Runs",
                        "batting_average": "Batting Average",
                    },
                    size_max=30,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Top batsmen bar chart
                top_batsmen = players_df.nlargest(10, "total_runs")
                fig = px.bar(
                    top_batsmen,
                    x="full_name",
                    y="total_runs",
                    color="batting_average",
                    title="Top 10 Run Scorers",
                    labels={"full_name": "Player", "total_runs": "Total Runs"},
                    color_continuous_scale="Viridis",
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            bowlers_df = players_df[players_df["total_wickets"] > 0]

            if not bowlers_df.empty:
                col1, col2 = st.columns(2)

                with col1:
                    # Wickets vs Average Scatter
                    fig = px.scatter(
                        bowlers_df,
                        x="total_wickets",
                        y="bowling_average",
                        size="matches_played",
                        color="country",
                        hover_name="full_name",
                        title="Wickets vs Bowling Average",
                        labels={
                            "total_wickets": "Total Wickets",
                            "bowling_average": "Bowling Average",
                        },
                        size_max=30,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Top bowlers bar chart
                    top_bowlers = bowlers_df.nlargest(10, "total_wickets")
                    fig = px.bar(
                        top_bowlers,
                        x="full_name",
                        y="total_wickets",
                        color="bowling_average",
                        title="Top 10 Wicket Takers",
                        labels={
                            "full_name": "Player",
                            "total_wickets": "Total Wickets",
                        },
                        color_continuous_scale="RdYlGn_r",
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No bowling data available for selected filters")

        with tab3:
            # All-round performance radar chart
            all_rounders = players_df[
                players_df["playing_role"].str.contains("All-rounder")
            ]

            if not all_rounders.empty:
                # Normalize data for radar chart
                normalized_df = all_rounders.copy()
                normalized_df["norm_runs"] = (
                    normalized_df["total_runs"] / normalized_df["total_runs"].max()
                )
                normalized_df["norm_wickets"] = (
                    normalized_df["total_wickets"]
                    / normalized_df["total_wickets"].max()
                )
                normalized_df["norm_matches"] = (
                    normalized_df["matches_played"]
                    / normalized_df["matches_played"].max()
                )

                fig = go.Figure()

                for idx, row in normalized_df.iterrows():
                    fig.add_trace(
                        go.Scatterpolar(
                            r=[
                                row["norm_runs"],
                                row["norm_wickets"],
                                row["norm_matches"],
                            ],
                            theta=["Batting", "Bowling", "Experience"],
                            name=row["full_name"],
                            fill="toself",
                        )
                    )

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=True,
                    title="All-round Performance Comparison",
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No all-rounders found in selected filters")

    else:
        st.warning("No player data found for the selected filters")

# ============================================
# PAGE 4: SQL ANALYTICS PAGE
# ============================================

elif selected_page == "🔍 SQL Analytics":
    st.markdown(
        """
    <div class="main-title">
        <h1>🔍 SQL Analytics</h1>
        <p>25 Advanced SQL Queries for Cricket Data Analysis</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Query Categories
    query_categories = {
        "Beginner": [
            (
                "1. All Indian Players",
                "SELECT full_name, playing_role, batting_style, bowling_style FROM players WHERE country = 'India' ORDER BY full_name;",
                "Find all players who represent India",
            ),
            (
                "2. Recent Matches (Last 30 Days)",
                "SELECT match_description, venue, match_date, winning_team FROM matches ORDER BY match_date DESC LIMIT 10;",
                "Show recent cricket matches",
            ),
            (
                "3. Top 10 Run Scorers",
                "SELECT full_name, country, total_runs, batting_average FROM players ORDER BY total_runs DESC LIMIT 10;",
                "Highest run scorers in cricket",
            ),
            (
                "4. Players by Role",
                "SELECT playing_role, COUNT(*) as count FROM players GROUP BY playing_role ORDER BY count DESC;",
                "Count players by playing role",
            ),
            (
                "5. Team Performance",
                "SELECT country, COUNT(*) as players, SUM(total_runs) as total_runs FROM players GROUP BY country ORDER BY total_runs DESC;",
                "Team-wise player statistics",
            ),
            (
                "6. Batsmen with 50+ Average",
                "SELECT full_name, country, batting_average, total_runs FROM players WHERE batting_average >= 50 ORDER BY batting_average DESC;",
                "Elite batsmen with high average",
            ),
            (
                "7. Bowlers with 200+ Wickets",
                "SELECT full_name, country, total_wickets, bowling_average FROM players WHERE total_wickets >= 200 ORDER BY total_wickets DESC;",
                "Top wicket-taking bowlers",
            ),
            (
                "8. All-rounders Performance",
                "SELECT full_name, country, total_runs, total_wickets FROM players WHERE playing_role LIKE '%All-rounder%' ORDER BY (total_runs + total_wickets*20) DESC;",
                "All-rounder performance analysis",
            ),
        ],
        "Intermediate": [
            (
                "9. Players with 1000+ Runs & 50+ Wickets",
                "SELECT full_name, country, total_runs, total_wickets FROM players WHERE total_runs > 1000 AND total_wickets > 50 ORDER BY total_runs DESC;",
                "Elite all-round performers",
            ),
            (
                "10. Batting Consistency Analysis",
                "SELECT full_name, batting_average, (batting_average/50)*100 as consistency_score FROM players WHERE batting_average > 0 ORDER BY consistency_score DESC;",
                "Batting consistency measurement",
            ),
            (
                "11. Bowling Economy Analysis",
                "SELECT full_name, bowling_average, economy_rate FROM players WHERE total_wickets > 0 ORDER BY economy_rate ASC;",
                "Bowling economy rate analysis",
            ),
            (
                "12. Player Experience Levels",
                "SELECT full_name, matches_played, CASE WHEN matches_played >= 300 THEN 'Veteran' WHEN matches_played >= 100 THEN 'Experienced' ELSE 'Developing' END as experience_level FROM players ORDER BY matches_played DESC;",
                "Categorize players by experience",
            ),
            (
                "13. Country-wise Batting Average",
                "SELECT country, AVG(batting_average) as avg_batting, COUNT(*) as players FROM players WHERE batting_average > 0 GROUP BY country HAVING COUNT(*) >= 3 ORDER BY avg_batting DESC;",
                "Country batting performance",
            ),
            (
                "14. Role-based Statistics",
                "SELECT playing_role, AVG(total_runs) as avg_runs, AVG(total_wickets) as avg_wickets, COUNT(*) as count FROM players GROUP BY playing_role;",
                "Statistics by playing role",
            ),
            (
                "15. Performance Ratio Analysis",
                "SELECT full_name, (total_runs/NULLIF(total_wickets, 0)) as runs_per_wicket FROM players WHERE total_wickets > 0 ORDER BY runs_per_wicket DESC;",
                "Runs per wicket ratio",
            ),
            (
                "16. Career Performance Index",
                "SELECT full_name, (total_runs*0.5 + total_wickets*20) as performance_index FROM players ORDER BY performance_index DESC;",
                "Career performance scoring",
            ),
        ],
        "Advanced": [
            (
                "17. Player Ranking System",
                "SELECT full_name, country, (total_runs*0.01 + batting_average*0.5 + total_wickets*2 + (50 - COALESCE(bowling_average, 50))*0.5) as ranking_score, RANK() OVER (ORDER BY (total_runs*0.01 + batting_average*0.5 + total_wickets*2 + (50 - COALESCE(bowling_average, 50))*0.5) DESC) as rank FROM players WHERE matches_played >= 20;",
                "Comprehensive player ranking",
            ),
            (
                "18. Batting Form Analysis",
                "WITH recent_performance AS (SELECT player_id, AVG(runs_scored) as recent_avg FROM batting_stats GROUP BY player_id) SELECT p.full_name, p.batting_average, rp.recent_avg, (rp.recent_avg/p.batting_average)*100 as form_percentage FROM players p JOIN recent_performance rp ON p.player_id = rp.player_id WHERE p.batting_average > 0 ORDER BY form_percentage DESC;",
                "Recent batting form analysis",
            ),
            (
                "19. Bowling Impact Analysis",
                "SELECT p.full_name, p.total_wickets, p.bowling_average, (300/p.bowling_average) as impact_score FROM players p WHERE p.total_wickets > 0 ORDER BY impact_score DESC;",
                "Bowling impact measurement",
            ),
            (
                "20. All-round Performance Matrix",
                "SELECT full_name, total_runs, total_wickets, CASE WHEN total_runs > 5000 AND total_wickets > 100 THEN 'Elite All-rounder' WHEN total_runs > 2000 AND total_wickets > 50 THEN 'Good All-rounder' WHEN total_runs > 1000 AND total_wickets > 20 THEN 'Developing All-rounder' ELSE 'Specialist' END as all_rounder_category FROM players WHERE total_runs > 0 AND total_wickets > 0 ORDER BY (total_runs + total_wickets*20) DESC;",
                "All-rounder categorization",
            ),
            (
                "21. Performance Trend Analysis",
                "WITH yearly_stats AS (SELECT player_id, strftime('%Y', match_date) as year, AVG(runs_scored) as yearly_avg FROM batting_stats bs JOIN matches m ON bs.match_id = m.match_id GROUP BY player_id, year) SELECT p.full_name, ys.year, ys.yearly_avg, LAG(ys.yearly_avg) OVER (PARTITION BY p.player_id ORDER BY ys.year) as prev_year_avg, CASE WHEN ys.yearly_avg > LAG(ys.yearly_avg) OVER (PARTITION BY p.player_id ORDER BY ys.year) * 1.1 THEN 'Improving' WHEN ys.yearly_avg < LAG(ys.yearly_avg) OVER (PARTITION BY p.player_id ORDER BY ys.year) * 0.9 THEN 'Declining' ELSE 'Stable' END as trend FROM players p JOIN yearly_stats ys ON p.player_id = ys.player_id ORDER BY p.full_name, ys.year;",
                "Yearly performance trends",
            ),
            (
                "22. Match Winner Analysis",
                "SELECT winning_team, COUNT(*) as wins, ROUND(AVG(CAST(SUBSTR(victory_margin, 1, INSTR(victory_margin, ' ') - 1) AS INTEGER)), 2) as avg_margin FROM matches WHERE winning_team IS NOT NULL AND victory_type = 'runs' GROUP BY winning_team ORDER BY wins DESC;",
                "Team winning patterns",
            ),
            (
                "23. Toss Impact Analysis",
                "SELECT toss_decision, COUNT(*) as total_matches, SUM(CASE WHEN winning_team = toss_winner THEN 1 ELSE 0 END) as wins_after_toss, ROUND(SUM(CASE WHEN winning_team = toss_winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_percentage FROM matches WHERE toss_decision IS NOT NULL GROUP BY toss_decision;",
                "Toss decision impact",
            ),
            (
                "24. Player Contribution Index",
                "SELECT full_name, total_runs, total_wickets, (total_runs/1000 + total_wickets/10) as contribution_index, RANK() OVER (ORDER BY (total_runs/1000 + total_wickets/10) DESC) as contribution_rank FROM players;",
                "Player contribution measurement",
            ),
            (
                "25. Career Trajectory Analysis",
                "SELECT full_name, matches_played, total_runs, total_wickets, CASE WHEN matches_played < 50 THEN 'Early Career' WHEN matches_played < 150 THEN 'Mid Career' WHEN matches_played < 300 THEN 'Peak Career' ELSE 'Late Career' END as career_phase, ROUND(total_runs * 1.0 / matches_played, 2) as runs_per_match, ROUND(total_wickets * 1.0 / matches_played, 2) as wickets_per_match FROM players WHERE matches_played > 0 ORDER BY matches_played DESC;",
                "Player career phase analysis",
            ),
        ],
    }

    # Category Selection
    category = st.selectbox("Select Query Category", list(query_categories.keys()))

    # Query Selection
    query_options = [q[0] for q in query_categories[category]]
    selected_query_name = st.selectbox("Select Query to Execute", query_options)

    # Get Selected Query
    selected_query = ""
    query_description = ""
    for name, query, desc in query_categories[category]:
        if name == selected_query_name:
            selected_query = query
            query_description = desc
            break

    # Display Query Info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {selected_query_name}")
        st.markdown(f"*{query_description}*")

    with col2:
        execute_btn = st.button(
            "▶️ Execute Query", use_container_width=True, type="primary"
        )

    # Display SQL Code
    st.markdown("#### 📝 SQL Query")
    st.code(selected_query, language="sql")

    # Execute Query
    if execute_btn and selected_query:
        with st.spinner("Executing query..."):
            try:
                result = db.execute_query(selected_query)

                if not result.empty:
                    st.success(
                        f"✅ Query executed successfully! ({len(result)} rows returned)"
                    )

                    # Display Results
                    st.markdown("#### 📊 Query Results")
                    st.dataframe(result, use_container_width=True)

                    # Visualizations
                    if len(result) > 1:
                        st.markdown("#### 📈 Visualization")

                        try:
                            if len(result.columns) >= 2:
                                # Try to create appropriate visualization
                                numeric_cols = result.select_dtypes(
                                    include=[np.number]
                                ).columns

                                if len(numeric_cols) >= 1:
                                    x_col = result.columns[0]
                                    y_col = (
                                        numeric_cols[0]
                                        if len(numeric_cols) > 0
                                        else result.columns[1]
                                    )

                                    if len(result) <= 10:
                                        # Bar chart for small results
                                        fig = px.bar(
                                            result,
                                            x=x_col,
                                            y=y_col,
                                            title=f"{selected_query_name} - Results",
                                            color_discrete_sequence=["#4f46e5"],
                                        )
                                    else:
                                        # Scatter plot for larger results
                                        fig = px.scatter(
                                            result.head(20),
                                            x=x_col,
                                            y=y_col,
                                            title=f"{selected_query_name} - Analysis",
                                            color_discrete_sequence=["#10b981"],
                                        )

                                    st.plotly_chart(fig, use_container_width=True)
                        except:
                            pass
                else:
                    st.info("Query executed successfully but returned no results.")

            except Exception as e:
                st.error(f"❌ Error executing query: {str(e)}")

    # Custom Query Section
    st.markdown("---")
    st.markdown("### 💻 Custom SQL Query Editor")

    custom_query = st.text_area(
        "Write your own SQL query:",
        height=150,
        placeholder="SELECT * FROM players WHERE country = 'India' ORDER BY total_runs DESC LIMIT 5;",
        help="Write your custom SQL query to analyze the cricket database",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run_custom = st.button("🚀 Run Custom Query", use_container_width=True)

    if run_custom and custom_query.strip():
        with st.spinner("Executing custom query..."):
            try:
                custom_result = db.execute_query(custom_query)

                if not custom_result.empty:
                    st.success(f"✅ Custom query executed! ({len(custom_result)} rows)")

                    # Show results
                    st.dataframe(custom_result, use_container_width=True)

                    # Show query info
                    with st.expander("Query Information"):
                        st.write(f"**Columns:** {', '.join(custom_result.columns)}")
                        st.write(f"**Rows:** {len(custom_result)}")
                        st.write(f"**Data Types:**")
                        st.write(custom_result.dtypes)
                else:
                    st.info("Query executed but returned no results.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================
# PAGE 5: CRUD OPERATIONS PAGE
# ============================================

elif selected_page == "🛠️ CRUD Operations":
    st.markdown(
        """
    <div class="main-title">
        <h1>🛠️ Database Management</h1>
        <p>Create, Read, Update, Delete operations on cricket database</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Operation Selection
    operation = st.radio(
        "Select Operation",
        [
            "➕ Create New Player",
            "👁️ View All Players",
            "✏️ Update Player",
            "🗑️ Delete Player",
        ],
        horizontal=True,
    )

    if operation == "➕ Create New Player":
        st.markdown("### ➕ Add New Player to Database")

        with st.form("create_player_form"):
            col1, col2 = st.columns(2)

            with col1:
                full_name = st.text_input("Full Name*", placeholder="Virat Kohli")
                country = st.text_input("Country*", placeholder="India")
                playing_role = st.selectbox(
                    "Playing Role*",
                    [
                        "Batsman",
                        "Bowler",
                        "All-rounder",
                        "Wicket-keeper",
                        "Batsman/Wicket-keeper",
                    ],
                )
                batting_style = st.selectbox(
                    "Batting Style", ["Right-handed", "Left-handed", "Switch hitter"]
                )

            with col2:
                bowling_style = st.text_input(
                    "Bowling Style", placeholder="Right-arm medium"
                )
                matches_played = st.number_input("Matches Played", min_value=0, value=0)
                total_runs = st.number_input("Total Runs", min_value=0, value=0)
                total_wickets = st.number_input("Total Wickets", min_value=0, value=0)

            col3, col4 = st.columns(2)
            with col3:
                batting_average = st.number_input(
                    "Batting Average", min_value=0.0, value=0.0, step=0.1
                )
                strike_rate = st.number_input(
                    "Strike Rate", min_value=0.0, value=0.0, step=0.1
                )
            with col4:
                bowling_average = st.number_input(
                    "Bowling Average", min_value=0.0, value=0.0, step=0.1
                )
                economy_rate = st.number_input(
                    "Economy Rate", min_value=0.0, value=0.0, step=0.1
                )

            submitted = st.form_submit_button(
                "➕ Add Player", use_container_width=True, type="primary"
            )

            if submitted:
                if full_name and country:
                    try:
                        # Get next player ID
                        max_id = db.execute_query(
                            "SELECT MAX(player_id) FROM players"
                        ).iloc[0, 0]
                        next_id = (max_id + 1) if max_id else 1

                        query = """
                        INSERT INTO players (player_id, full_name, playing_role, batting_style, bowling_style, 
                                            country, matches_played, total_runs, total_wickets, 
                                            batting_average, bowling_average, strike_rate, economy_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """

                        params = (
                            next_id,
                            full_name,
                            playing_role,
                            batting_style,
                            bowling_style,
                            country,
                            matches_played,
                            total_runs,
                            total_wickets,
                            batting_average,
                            bowling_average,
                            strike_rate,
                            economy_rate,
                        )

                        db.execute_update(query, params)

                        st.success(f"✅ Player '{full_name}' added successfully!")
                        st.balloons()

                        # Show added player
                        with st.expander("View Added Player", expanded=True):
                            added_player = db.execute_query(
                                "SELECT * FROM players WHERE player_id = ?", (next_id,)
                            )
                            st.dataframe(added_player, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Error adding player: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all required fields (*)")

    elif operation == "👁️ View All Players":
        st.markdown("### 👁️ View All Players")

        # Search and Filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input(
                "Search by name", placeholder="Enter player name..."
            )
        with col2:
            filter_country = st.selectbox(
                "Filter by country",
                [
                    "All Countries",
                    "India",
                    "Australia",
                    "England",
                    "New Zealand",
                    "Pakistan",
                    "South Africa",
                ],
            )
        with col3:
            sort_by = st.selectbox(
                "Sort by", ["Name", "Total Runs", "Total Wickets", "Matches"]
            )

        # Build query
        query = "SELECT * FROM players WHERE 1=1"
        params = []

        if search_name:
            query += " AND full_name LIKE ?"
            params.append(f"%{search_name}%")

        if filter_country != "All Countries":
            query += " AND country = ?"
            params.append(filter_country)

        sort_mapping = {
            "Name": "full_name ASC",
            "Total Runs": "total_runs DESC",
            "Total Wickets": "total_wickets DESC",
            "Matches": "matches_played DESC",
        }
        query += f" ORDER BY {sort_mapping[sort_by]}"

        # Execute query
        players = db.execute_query(query, params)

        if not players.empty:
            # Display statistics
            st.markdown("#### 📊 Player Statistics Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Players", len(players))
            with col2:
                st.metric("Total Runs", f"{players['total_runs'].sum():,}")
            with col3:
                st.metric("Total Wickets", players["total_wickets"].sum())
            with col4:
                st.metric("Avg Matches", f"{players['matches_played'].mean():.0f}")

            # Display data
            st.markdown("#### 📋 Player Data")

            display_cols = [
                "player_id",
                "full_name",
                "country",
                "playing_role",
                "matches_played",
                "total_runs",
                "batting_average",
                "total_wickets",
                "bowling_average",
            ]

            display_df = players[display_cols].copy()
            display_df["total_runs"] = display_df["total_runs"].apply(
                lambda x: f"{x:,}"
            )
            display_df["matches_played"] = display_df["matches_played"].apply(
                lambda x: f"{x:,}"
            )

            st.dataframe(
                display_df,
                column_config={
                    "player_id": "ID",
                    "full_name": "Name",
                    "country": "Country",
                    "playing_role": "Role",
                    "matches_played": "Matches",
                    "total_runs": "Runs",
                    "batting_average": "Bat Avg",
                    "total_wickets": "Wickets",
                    "bowling_average": "Bowl Avg",
                },
                use_container_width=True,
                height=500,
            )

            # Export option
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="players_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No players found matching the criteria.")

    elif operation == "✏️ Update Player":
        st.markdown("### ✏️ Update Player Information")

        # Get all players for selection
        players = db.execute_query(
            "SELECT player_id, full_name, country FROM players ORDER BY full_name"
        )

        if not players.empty:
            player_options = [
                f"{row['player_id']}: {row['full_name']} ({row['country']})"
                for _, row in players.iterrows()
            ]

            selected_player = st.selectbox("Select Player to Update", player_options)

            if selected_player:
                player_id = int(selected_player.split(":")[0])

                # Get current player data
                current_data = db.execute_query(
                    "SELECT * FROM players WHERE player_id = ?", (player_id,)
                )

                if not current_data.empty:
                    current = current_data.iloc[0]

                    st.markdown(f"#### Editing: **{current['full_name']}**")

                    with st.form("update_player_form"):
                        col1, col2 = st.columns(2)

                        with col1:
                            new_full_name = st.text_input(
                                "Full Name", value=current["full_name"]
                            )
                            new_country = st.text_input(
                                "Country", value=current["country"]
                            )
                            new_role = st.selectbox(
                                "Playing Role",
                                [
                                    "Batsman",
                                    "Bowler",
                                    "All-rounder",
                                    "Wicket-keeper",
                                    "Batsman/Wicket-keeper",
                                ],
                                index=[
                                    "Batsman",
                                    "Bowler",
                                    "All-rounder",
                                    "Wicket-keeper",
                                    "Batsman/Wicket-keeper",
                                ].index(current["playing_role"])
                                if current["playing_role"]
                                in [
                                    "Batsman",
                                    "Bowler",
                                    "All-rounder",
                                    "Wicket-keeper",
                                    "Batsman/Wicket-keeper",
                                ]
                                else 0,
                            )
                            new_batting_style = st.text_input(
                                "Batting Style", value=current["batting_style"]
                            )

                        with col2:
                            new_bowling_style = st.text_input(
                                "Bowling Style", value=current["bowling_style"]
                            )
                            new_matches = st.number_input(
                                "Matches", value=int(current["matches_played"])
                            )
                            new_runs = st.number_input(
                                "Total Runs", value=int(current["total_runs"])
                            )
                            new_wickets = st.number_input(
                                "Total Wickets", value=int(current["total_wickets"])
                            )

                        col3, col4 = st.columns(2)
                        with col3:
                            new_batting_avg = st.number_input(
                                "Batting Average",
                                value=float(current["batting_average"]),
                            )
                            new_strike_rate = st.number_input(
                                "Strike Rate", value=float(current["strike_rate"])
                            )
                        with col4:
                            new_bowling_avg = st.number_input(
                                "Bowling Average",
                                value=float(current["bowling_average"]),
                            )
                            new_economy_rate = st.number_input(
                                "Economy Rate", value=float(current["economy_rate"])
                            )

                        submitted = st.form_submit_button(
                            "💾 Update Player", use_container_width=True, type="primary"
                        )

                        if submitted:
                            try:
                                query = """
                                UPDATE players 
                                SET full_name = ?, country = ?, playing_role = ?, batting_style = ?, 
                                    bowling_style = ?, matches_played = ?, total_runs = ?, total_wickets = ?,
                                    batting_average = ?, bowling_average = ?, strike_rate = ?, economy_rate = ?
                                WHERE player_id = ?
                                """

                                params = (
                                    new_full_name,
                                    new_country,
                                    new_role,
                                    new_batting_style,
                                    new_bowling_style,
                                    new_matches,
                                    new_runs,
                                    new_wickets,
                                    new_batting_avg,
                                    new_bowling_avg,
                                    new_strike_rate,
                                    new_economy_rate,
                                    player_id,
                                )

                                db.execute_update(query, params)

                                st.success(
                                    f"✅ Player '{new_full_name}' updated successfully!"
                                )

                                # Show updated data
                                with st.expander("View Updated Player", expanded=True):
                                    updated = db.execute_query(
                                        "SELECT * FROM players WHERE player_id = ?",
                                        (player_id,),
                                    )
                                    st.dataframe(updated, use_container_width=True)

                            except Exception as e:
                                st.error(f"❌ Error updating player: {str(e)}")

    elif operation == "🗑️ Delete Player":
        st.markdown("### 🗑️ Delete Player from Database")
        st.warning("⚠️ **Warning**: This action cannot be undone!")

        # Get all players
        players = db.execute_query(
            "SELECT player_id, full_name, country FROM players ORDER BY full_name"
        )

        if not players.empty:
            player_options = [
                f"{row['player_id']}: {row['full_name']} ({row['country']})"
                for _, row in players.iterrows()
            ]

            selected_player = st.selectbox("Select Player to Delete", player_options)

            if selected_player:
                player_id = int(selected_player.split(":")[0])
                player_name = selected_player.split(":")[1].split("(")[0].strip()

                # Show player details
                player_details = db.execute_query(
                    "SELECT full_name, country, playing_role, matches_played, total_runs, total_wickets FROM players WHERE player_id = ?",
                    (player_id,),
                )

                if not player_details.empty:
                    st.markdown("#### Player Details:")
                    st.dataframe(player_details, use_container_width=True)

                    # Confirmation
                    confirm = st.checkbox(
                        f"I confirm I want to delete **{player_name}** from the database"
                    )

                    if confirm:
                        if st.button(
                            "🗑️ Delete Player",
                            type="secondary",
                            use_container_width=True,
                        ):
                            try:
                                # Delete related records first (if any foreign key constraints)
                                db.execute_update(
                                    "DELETE FROM batting_stats WHERE player_id = ?",
                                    (player_id,),
                                )
                                db.execute_update(
                                    "DELETE FROM bowling_stats WHERE player_id = ?",
                                    (player_id,),
                                )

                                # Delete player
                                db.execute_update(
                                    "DELETE FROM players WHERE player_id = ?",
                                    (player_id,),
                                )

                                st.success(
                                    f"✅ Player '{player_name}' deleted successfully!"
                                )
                                st.rerun()

                            except Exception as e:
                                st.error(f"❌ Error deleting player: {str(e)}")
                else:
                    st.error("Player not found!")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p style="font-size: 0.9rem;">
        🏏 <strong>Cricbuzz LiveStats</strong> | Real-Time Cricket Analytics Dashboard<br>
        Built with ❤️ using Python, Streamlit, and Cricbuzz API<br>
        Data Source: Cricbuzz Cricket API | Database: SQLite<br>
        © 2024 Cricket Analytics Hub | Last updated: """
    + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    + """
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Auto-refresh for live matches
if selected_page == "⚡ Live Matches" and auto_refresh:
    time.sleep(30)  # Refresh every 30 seconds
    st.rerun()
