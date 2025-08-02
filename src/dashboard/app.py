"""
Streamlit dashboard for NBA Clutch Factor predictions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import random

def main():
    st.set_page_config(
        page_title="NBA Clutch Factor",
        page_icon="🏀",
        layout="wide"
    )
    
    st.title("🏀 NBA Clutch Factor - Player Performance Predictor")
    st.markdown("Predict NBA player performance in high-pressure clutch situations")
    
    # Sidebar
    st.sidebar.header("Prediction Inputs")
    player_name = st.sidebar.text_input("Player Name", "LeBron James")
    home_game = st.sidebar.checkbox("Home Game", value=True)
    opponent_strength = st.sidebar.slider("Opponent Strength", 0.0, 1.0, 0.5)
    
    # Main area
    if st.button("Predict Performance", type="primary"):
        # Demo prediction
        categories = ['Underperform', 'Expected', 'Overperform']
        prediction = random.choice(categories)
        confidence = random.uniform(0.6, 0.9)
        
        st.success(f"🏀 Prediction: {prediction}")
        st.info(f"📊 Confidence: {confidence:.1%}")
        st.write(f"Player: {player_name}")
        st.write(f"Home Game: {'Yes' if home_game else 'No'}")
        st.write(f"Opponent Strength: {opponent_strength}")
    
    # Sample data
    st.header("Sample Player Rankings")
    sample_data = {
        'Player': ['Damian Lillard', 'Stephen Curry', 'LeBron James'],
        'Clutch FG%': [48.2, 45.8, 43.1],
        'Rating': [92.5, 89.2, 87.8]
    }
    df = pd.DataFrame(sample_data)
    st.dataframe(df)

if __name__ == "__main__":
    main()
