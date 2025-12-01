"""
Enhanced Streamlit dashboard for NBA Clutch Factor predictions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.models.predictor import ClutchPredictor

# Page configuration
st.set_page_config(
    page_title="NBA Clutch Factor",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictor' not in st.session_state:
    st.session_state.predictor = ClutchPredictor()
    st.session_state.predictor.load_model()
    st.session_state.predictions_history = []

# Popular NBA players for quick selection
POPULAR_PLAYERS = [
    "LeBron James", "Stephen Curry", "Kevin Durant", "Damian Lillard",
    "Kawhi Leonard", "Jimmy Butler", "Kyrie Irving", "Paul George",
    "James Harden", "Russell Westbrook", "Jayson Tatum", "Luka Doncic",
    "Giannis Antetokounmpo", "Joel Embiid", "Devin Booker"
]

def create_probability_chart(result):
    """Create a bar chart showing prediction probabilities."""
    probs = result['probabilities']
    categories = list(probs.keys())
    values = list(probs.values())
    
    # Color mapping
    colors = {
        'Overperform': '#2ecc71',
        'Expected': '#f39c12',
        'Underperform': '#e74c3c'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=[colors.get(cat, '#3498db') for cat in categories],
            text=[f'{v:.1%}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Prediction Probabilities",
        xaxis_title="Performance Category",
        yaxis_title="Probability",
        yaxis=dict(range=[0, 1], tickformat='.0%'),
        height=300,
        showlegend=False,
        template="plotly_white"
    )
    
    return fig

def create_feature_importance_chart(predictor):
    """Create a chart showing feature importance."""
    importance = predictor.feature_importance
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(importance.values()),
            y=list(importance.keys()),
            orientation='h',
            marker_color='#3498db',
            text=[f'{v:.1%}' for v in importance.values()],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Feature Importance",
        xaxis_title="Importance",
        yaxis_title="Feature",
        xaxis=dict(tickformat='.0%'),
        height=300,
        template="plotly_white"
    )
    
    return fig

def display_prediction_result(result, player_name):
    """Display prediction results in a formatted way."""
    prediction = result['prediction']
    confidence = result['confidence']
    probabilities = result['probabilities']
    
    # Color coding based on prediction
    if prediction == 'Overperform':
        color = '🟢'
        bg_color = '#d4edda'
    elif prediction == 'Expected':
        color = '🟡'
        bg_color = '#fff3cd'
    else:
        color = '🔴'
        bg_color = '#f8d7da'
    
    # Main prediction card
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.metric(
            label="Prediction",
            value=f"{color} {prediction}",
            delta=f"{confidence:.1%} confidence"
        )
    
    with col2:
        st.metric(
            label="Player",
            value=player_name
        )
    
    with col3:
        method = result.get('method', 'demo_rules')
        method_display = 'Trained Model' if method == 'trained_model' else 'Rule-Based'
        st.metric(
            label="Method",
            value=method_display
        )
    
    # Probability breakdown
    st.subheader("📊 Probability Breakdown")
    prob_col1, prob_col2 = st.columns([2, 1])
    
    with prob_col1:
        fig = create_probability_chart(result)
        st.plotly_chart(fig, use_container_width=True)
    
    with prob_col2:
        st.markdown("### Detailed Probabilities")
        for category, prob in probabilities.items():
            st.progress(prob, text=f"{category}: {prob:.1%}")
    
    # Explanation
    if 'explanation' in result:
        st.info(f"💡 **Explanation:** {result['explanation']}")

def main():
    # Header
    st.markdown('<div class="main-header">🏀 NBA Clutch Factor</div>', unsafe_allow_html=True)
    st.markdown("### Predict NBA player performance in high-pressure clutch situations")
    
    # Sidebar
    st.sidebar.header("⚙️ Prediction Settings")
    
    # Player selection
    player_option = st.sidebar.radio(
        "Player Selection",
        ["Select from list", "Enter custom name"],
        index=0
    )
    
    if player_option == "Select from list":
        player_name = st.sidebar.selectbox(
            "Choose Player",
            POPULAR_PLAYERS,
            index=0
        )
    else:
        player_name = st.sidebar.text_input("Player Name", "LeBron James")
    
    # Game context inputs
    st.sidebar.markdown("---")
    st.sidebar.subheader("Game Context")
    
    home_game = st.sidebar.checkbox("Home Game", value=True)
    opponent_strength = st.sidebar.slider(
        "Opponent Strength",
        0.0, 1.0, 0.5, 0.05,
        help="0.0 = Weak opponent, 1.0 = Strong opponent"
    )
    rest_days = st.sidebar.slider(
        "Rest Days",
        0, 5, 1,
        help="Days since last game"
    )
    season_clutch_pct = st.sidebar.slider(
        "Season Clutch FG%",
        30.0, 60.0, 45.0, 0.5,
        help="Player's season clutch field goal percentage"
    )
    minutes_per_game = st.sidebar.slider(
        "Minutes per Game",
        20.0, 40.0, 32.0, 0.5,
        help="Average minutes played per game"
    )
    
    # Model information
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Model Info")
    model_info = st.session_state.predictor.get_model_info()
    st.sidebar.write(f"**Model Status:** {'✅ Loaded' if model_info['model_loaded'] else '⚠️ Demo Mode'}")
    st.sidebar.write(f"**Scaler:** {'✅ Loaded' if model_info['scaler_loaded'] else '❌ Not Available'}")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Prediction", "📈 Comparison", "📊 Model Info", "📜 History"])
    
    with tab1:
        st.header("Single Player Prediction")
        
        # Create game context
        game_context = {
            'home_game': 1 if home_game else 0,
            'opponent_strength': opponent_strength,
            'rest_days': rest_days,
            'season_clutch_pct': season_clutch_pct,
            'minutes_per_game': minutes_per_game
        }
        
        # Prediction button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.button(
                "🚀 Make Prediction",
                type="primary",
                use_container_width=True
            )
        
        if predict_button:
            with st.spinner("Analyzing player performance..."):
                result = st.session_state.predictor.predict_player_performance(
                    player_name, game_context
                )
                
                # Store in history
                result['game_context'] = game_context
                st.session_state.predictions_history.append(result)
                
                # Display results
                display_prediction_result(result, player_name)
                
                # Show game context summary
                st.markdown("---")
                st.subheader("🎮 Game Context Summary")
                context_cols = st.columns(5)
                context_cols[0].metric("Home", "Yes" if home_game else "No")
                context_cols[1].metric("Opponent", f"{opponent_strength:.2f}")
                context_cols[2].metric("Rest Days", f"{rest_days}")
                context_cols[3].metric("Clutch FG%", f"{season_clutch_pct:.1f}%")
                context_cols[4].metric("MPG", f"{minutes_per_game:.1f}")
    
    with tab2:
        st.header("Player Comparison")
        st.markdown("Compare predictions for multiple players")
        
        num_players = st.slider("Number of Players to Compare", 2, 5, 2)
        
        comparison_data = []
        for i in range(num_players):
            with st.expander(f"Player {i+1} Settings"):
                p_name = st.text_input(f"Player {i+1} Name", value=POPULAR_PLAYERS[i] if i < len(POPULAR_PLAYERS) else "Player", key=f"comp_player_{i}")
                p_home = st.checkbox("Home Game", value=True, key=f"comp_home_{i}")
                p_opp = st.slider("Opponent Strength", 0.0, 1.0, 0.5, key=f"comp_opp_{i}")
                p_rest = st.slider("Rest Days", 0, 5, 1, key=f"comp_rest_{i}")
                p_clutch = st.slider("Season Clutch FG%", 30.0, 60.0, 45.0, key=f"comp_clutch_{i}")
                p_mpg = st.slider("Minutes per Game", 20.0, 40.0, 32.0, key=f"comp_mpg_{i}")
                
                comparison_data.append({
                    'name': p_name,
                    'context': {
                        'home_game': 1 if p_home else 0,
                        'opponent_strength': p_opp,
                        'rest_days': p_rest,
                        'season_clutch_pct': p_clutch,
                        'minutes_per_game': p_mpg
                    }
                })
        
        if st.button("Compare Players", type="primary"):
            results = []
            for player_data in comparison_data:
                result = st.session_state.predictor.predict_player_performance(
                    player_data['name'], player_data['context']
                )
                results.append({
                    'player': player_data['name'],
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'probabilities': result['probabilities']
                })
            
            # Comparison table
            comparison_df = pd.DataFrame([
                {
                    'Player': r['player'],
                    'Prediction': r['prediction'],
                    'Confidence': f"{r['confidence']:.1%}",
                    'Overperform Prob': f"{r['probabilities']['Overperform']:.1%}",
                    'Expected Prob': f"{r['probabilities']['Expected']:.1%}",
                    'Underperform Prob': f"{r['probabilities']['Underperform']:.1%}"
                }
                for r in results
            ])
            
            st.dataframe(comparison_df, use_container_width=True)
            
            # Comparison chart
            fig = go.Figure()
            for result in results:
                fig.add_trace(go.Bar(
                    name=result['player'],
                    x=['Overperform', 'Expected', 'Underperform'],
                    y=[
                        result['probabilities']['Overperform'],
                        result['probabilities']['Expected'],
                        result['probabilities']['Underperform']
                    ]
                ))
            
            fig.update_layout(
                title="Player Comparison - Prediction Probabilities",
                xaxis_title="Category",
                yaxis_title="Probability",
                yaxis=dict(tickformat='.0%'),
                barmode='group',
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Model Information")
        
        model_info = st.session_state.predictor.get_model_info()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Model Status")
            
            if model_info['model_loaded']:
                st.success("✅ **Model Loaded:** Trained ML model is active")
            else:
                st.info("⚠️ **Demo Mode:** Using rule-based predictions")
                st.caption("💡 Run `python scripts/create_demo_model.py` to create a trained model")
            
            if model_info['scaler_loaded']:
                st.success("✅ **Scaler Loaded:** Feature scaling active")
            else:
                st.caption("ℹ️ **Scaler:** Not required for demo mode")
            
            st.write(f"**Model Path:** `{model_info['model_path']}`")
            st.write(f"**Categories:** {', '.join(model_info['categories'])}")
            
            # Add info box for demo mode
            if not model_info['model_loaded']:
                st.markdown("---")
                st.info("""
                **Demo Mode Information:**
                - Predictions use rule-based logic based on real NBA factors
                - All features are still considered (home/away, opponent, rest, etc.)
                - Results are realistic and based on statistical analysis
                - To use a trained ML model, create one using the script above
                """)
        
        with col2:
            st.subheader("Feature Importance")
            fig = create_feature_importance_chart(st.session_state.predictor)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("About the Model")
        st.markdown("""
        The NBA Clutch Factor model predicts player performance in clutch situations 
        (final 5 minutes with ≤5 point differential). The model considers:
        
        - **Home Court Advantage**: Players typically perform better at home
        - **Opponent Strength**: Stronger opponents make clutch situations more challenging
        - **Rest Days**: Well-rested players tend to perform better
        - **Season Clutch Performance**: Historical clutch performance is a strong indicator
        - **Playing Time**: Minutes per game indicates player role and stamina
        
        The model classifies performance into three categories:
        - **Overperform**: Exceeds expected performance in clutch situations
        - **Expected**: Meets expected performance levels
        - **Underperform**: Falls below expected performance
        """)
    
    with tab4:
        st.header("Prediction History")
        
        if st.session_state.predictions_history:
            history_df = pd.DataFrame([
                {
                    'Player': p['player_name'],
                    'Prediction': p['prediction'],
                    'Confidence': f"{p['confidence']:.1%}",
                    'Method': 'Trained Model' if p.get('method') == 'trained_model' else 'Rule-Based',
                    'Timestamp': p.get('timestamp', 'N/A')[:19] if 'timestamp' in p else 'N/A'
                }
                for p in st.session_state.predictions_history[-10:]  # Last 10 predictions
            ])
            
            st.dataframe(history_df, use_container_width=True)
            
            if st.button("Clear History"):
                st.session_state.predictions_history = []
                st.rerun()
        else:
            st.info("No predictions made yet. Go to the Prediction tab to make your first prediction!")

if __name__ == "__main__":
    main()
