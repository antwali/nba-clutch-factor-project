#!/usr/bin/env python3
"""
Quick demo script to showcase NBA Clutch Factor predictions.
Run this to see the app in action via command line.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.predictor import ClutchPredictor

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_section(text):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}\n")

def demo_single_prediction():
    """Demo single player prediction."""
    print_header("DEMO 1: Single Player Prediction")
    
    predictor = ClutchPredictor()
    predictor.load_model()
    
    # Scenario 1: LeBron James - Home game, moderate opponent
    print("📊 Scenario: LeBron James - Home Game vs Moderate Opponent")
    print("-" * 70)
    
    game_context = {
        'home_game': 1,
        'opponent_strength': 0.6,
        'rest_days': 1,
        'season_clutch_pct': 45.0,
        'minutes_per_game': 32.0
    }
    
    result = predictor.predict_player_performance("LeBron James", game_context)
    
    print(f"✅ Prediction: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.1%}")
    print(f"\n📈 Probability Breakdown:")
    for category, prob in result['probabilities'].items():
        bar = '█' * int(prob * 30)
        print(f"   {category:15} {bar} {prob:5.1%}")
    
    print(f"\n💡 {result['explanation']}")
    
    time.sleep(2)
    
    # Scenario 2: Strong opponent
    print_section("📊 Scenario: Same Player vs Strong Opponent (0.8)")
    
    game_context['opponent_strength'] = 0.8
    result2 = predictor.predict_player_performance("LeBron James", game_context)
    
    print(f"✅ Prediction: {result2['prediction']}")
    print(f"📊 Confidence: {result2['confidence']:.1%}")
    print(f"\n💡 Notice how the prediction changes with stronger opponent!")
    print(f"   Previous: {result['prediction']} → Current: {result2['prediction']}")

def demo_clutch_performer():
    """Demo with a known clutch performer."""
    print_header("DEMO 2: Clutch Performer - Damian Lillard")
    
    predictor = ClutchPredictor()
    predictor.load_model()
    
    # Favorable conditions for a clutch player
    game_context = {
        'home_game': 1,
        'opponent_strength': 0.6,
        'rest_days': 2,  # Well rested
        'season_clutch_pct': 48.5,  # High clutch percentage
        'minutes_per_game': 36.0
    }
    
    result = predictor.predict_player_performance("Damian Lillard", game_context)
    
    print(f"✅ Prediction: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.1%}")
    print(f"\n📈 Probability Breakdown:")
    for category, prob in result['probabilities'].items():
        bar = '█' * int(prob * 30)
        print(f"   {category:15} {bar} {prob:5.1%}")
    
    print(f"\n💡 {result['explanation']}")
    print(f"\n🏀 Damian Lillard is known for clutch performance!")
    print(f"   High clutch FG% + favorable conditions = {result['prediction']}")

def demo_multiple_players():
    """Demo comparing multiple players."""
    print_header("DEMO 3: Multiple Player Comparison")
    
    predictor = ClutchPredictor()
    predictor.load_model()
    
    # Same game context for all players
    game_context = {
        'home_game': 1,
        'opponent_strength': 0.65,
        'rest_days': 1,
        'season_clutch_pct': 45.0,
        'minutes_per_game': 32.0
    }
    
    players = [
        "LeBron James",
        "Stephen Curry",
        "Kevin Durant",
        "Damian Lillard"
    ]
    
    print("Comparing 4 players with identical game context:\n")
    print(f"{'Player':<20} {'Prediction':<15} {'Confidence':<12} {'Top Probability'}")
    print("-" * 70)
    
    results = []
    for player in players:
        result = predictor.predict_player_performance(player, game_context)
        results.append((player, result))
        
        top_prob = max(result['probabilities'].items(), key=lambda x: x[1])
        print(f"{player:<20} {result['prediction']:<15} {result['confidence']:>10.1%}  {top_prob[0]}: {top_prob[1]:.1%}")
    
    print("\n💡 Notice how different players get different predictions")
    print("   even with the same game context - this is due to player-specific")
    print("   historical performance factors!")

def demo_game_context_impact():
    """Demo how game context affects predictions."""
    print_header("DEMO 4: Game Context Impact")
    
    predictor = ClutchPredictor()
    predictor.load_model()
    
    player = "Stephen Curry"
    
    scenarios = [
        {
            'name': 'Ideal Conditions',
            'context': {
                'home_game': 1,
                'opponent_strength': 0.4,  # Weak opponent
                'rest_days': 3,  # Well rested
                'season_clutch_pct': 47.0,
                'minutes_per_game': 34.0
            }
        },
        {
            'name': 'Challenging Conditions',
            'context': {
                'home_game': 0,  # Away
                'opponent_strength': 0.8,  # Strong opponent
                'rest_days': 0,  # Back-to-back
                'season_clutch_pct': 42.0,  # Lower clutch %
                'minutes_per_game': 38.0  # Heavy minutes
            }
        }
    ]
    
    for scenario in scenarios:
        print_section(f"📊 {scenario['name']}")
        print(f"   Home: {'Yes' if scenario['context']['home_game'] else 'No'}")
        print(f"   Opponent: {scenario['context']['opponent_strength']:.1f}")
        print(f"   Rest Days: {scenario['context']['rest_days']}")
        print(f"   Clutch FG%: {scenario['context']['season_clutch_pct']:.1f}%")
        
        result = predictor.predict_player_performance(player, scenario['context'])
        print(f"\n   ✅ Prediction: {result['prediction']}")
        print(f"   📊 Confidence: {result['confidence']:.1%}")
        
        time.sleep(1)

def demo_model_info():
    """Demo model information."""
    print_header("DEMO 5: Model Information")
    
    predictor = ClutchPredictor()
    predictor.load_model()
    
    model_info = predictor.get_model_info()
    
    print("📊 Model Status:")
    print(f"   Model Loaded: {'✅ Yes' if model_info['model_loaded'] else '⚠️  No (Demo Mode)'}")
    print(f"   Scaler Loaded: {'✅ Yes' if model_info['scaler_loaded'] else '❌ No'}")
    print(f"   Categories: {', '.join(model_info['categories'])}")
    
    print("\n📈 Feature Importance:")
    for feature, importance in model_info['feature_importance'].items():
        bar = '█' * int(importance * 30)
        print(f"   {feature:20} {bar} {importance:5.1%}")
    
    print("\n💡 These weights show which factors matter most for predictions!")

def main():
    """Run all demos."""
    print("\n" + "🏀" * 35)
    print(" " * 20 + "NBA CLUTCH FACTOR DEMO")
    print("🏀" * 35)
    
    print("\nThis demo showcases the NBA Clutch Factor prediction system.")
    print("You'll see how the model predicts player performance in clutch situations.\n")
    
    input("Press ENTER to start the demo...")
    
    try:
        demo_single_prediction()
        time.sleep(2)
        
        demo_clutch_performer()
        time.sleep(2)
        
        demo_multiple_players()
        time.sleep(2)
        
        demo_game_context_impact()
        time.sleep(2)
        
        demo_model_info()
        
        print_header("DEMO COMPLETE!")
        print("✅ You've seen:")
        print("   • Single player predictions")
        print("   • Clutch performer analysis")
        print("   • Multi-player comparison")
        print("   • Game context impact")
        print("   • Model information")
        print("\n🚀 Try the interactive dashboard: streamlit run src/dashboard/app.py")
        print("📝 Or use the CLI: python scripts/run_predictions.py --player 'Player Name'")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {str(e)}")
        print("   Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

