#!/usr/bin/env python3
"""
Prediction script for NBA Clutch Factor.
"""

import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Main prediction script."""
    parser = argparse.ArgumentParser(description='NBA Clutch Factor Predictions')
    parser.add_argument('--player', type=str, default='LeBron James',
                       help='Player name for prediction')
    parser.add_argument('--home', action='store_true',
                       help='Home game (default: away)')
    
    args = parser.parse_args()
    
    print(f"🏀 NBA Clutch Factor - Predicting {args.player}")
    print("=" * 50)
    
    # Sample game context
    game_context = {
        'home_game': 1 if args.home else 0,
        'opponent_strength': 0.6,
        'rest_days': 1,
        'season_clutch_pct': 45.0,
        'minutes_per_game': 32.0
    }
    
    # Make prediction (demo)
    print("🔮 Making prediction...")
    
    # Simulate prediction
    import random
    categories = ['Underperform', 'Expected', 'Overperform']
    prediction = random.choice(categories)
    confidence = random.uniform(0.6, 0.9)
    
    print(f"✅ Prediction: {prediction}")
    print(f"📊 Confidence: {confidence:.1%}")
    print(f"🏠 Home Game: {'Yes' if args.home else 'No'}")
    
    # Display game context
    print("\n📋 Game Context:")
    print(f"   Opponent Strength: {game_context['opponent_strength']}")
    print(f"   Rest Days: {game_context['rest_days']}")
    print(f"   Season Clutch %: {game_context['season_clutch_pct']}")
    print(f"   Minutes per Game: {game_context['minutes_per_game']}")

if __name__ == "__main__":
    main()