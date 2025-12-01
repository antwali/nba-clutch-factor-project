#!/usr/bin/env python3
"""
Prediction script for NBA Clutch Factor.
Uses the ClutchPredictor class for accurate predictions.
"""

import sys
import os
import argparse
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.predictor import ClutchPredictor

def main():
    """Main prediction script."""
    parser = argparse.ArgumentParser(
        description='NBA Clutch Factor Predictions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic prediction
  python run_predictions.py --player "LeBron James"
  
  # Home game prediction
  python run_predictions.py --player "Stephen Curry" --home
  
  # Full game context
  python run_predictions.py --player "Kevin Durant" --home --opponent 0.7 --rest 2 --clutch 52.0 --mpg 36.0
  
  # JSON output
  python run_predictions.py --player "Damian Lillard" --json
        """
    )
    parser.add_argument('--player', type=str, default='LeBron James',
                       help='Player name for prediction')
    parser.add_argument('--home', action='store_true',
                       help='Home game (default: away)')
    parser.add_argument('--opponent', type=float, default=0.6,
                       help='Opponent strength (0.0-1.0, default: 0.6)')
    parser.add_argument('--rest', type=int, default=1,
                       help='Rest days since last game (default: 1)')
    parser.add_argument('--clutch', type=float, default=45.0,
                       help='Season clutch FG%% (default: 45.0)')
    parser.add_argument('--mpg', type=float, default=32.0,
                       help='Minutes per game (default: 32.0)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--model-path', type=str, default='models/trained_models/',
                       help='Path to trained models directory')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = ClutchPredictor(model_path=args.model_path)
    model_loaded = predictor.load_model()
    
    if not args.json:
        print(f"🏀 NBA Clutch Factor - Predicting {args.player}")
        print("=" * 60)
        
        if model_loaded:
            print("✅ Using trained model")
        else:
            print("⚠️  Using rule-based prediction (model not found)")
        print()
    
    # Game context
    game_context = {
        'home_game': 1 if args.home else 0,
        'opponent_strength': max(0.0, min(1.0, args.opponent)),
        'rest_days': max(0, args.rest),
        'season_clutch_pct': max(0.0, min(100.0, args.clutch)),
        'minutes_per_game': max(0.0, min(48.0, args.mpg))
    }
    
    # Make prediction
    if not args.json:
        print("🔮 Making prediction...")
        print()
    
    result = predictor.predict_player_performance(args.player, game_context)
    
    # Output results
    if args.json:
        output = {
            'player': result['player_name'],
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities'],
            'game_context': game_context,
            'method': result.get('method', 'unknown'),
            'timestamp': result.get('timestamp', '')
        }
        print(json.dumps(output, indent=2))
    else:
        # Formatted output
        print(f"✅ Prediction: {result['prediction']}")
        print(f"📊 Confidence: {result['confidence']:.1%}")
        print()
        
        print("📈 Probability Breakdown:")
        for category, prob in result['probabilities'].items():
            bar_length = int(prob * 40)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            print(f"   {category:15} {bar} {prob:5.1%}")
        
        print()
        print("📋 Game Context:")
        print(f"   Home Game:        {'Yes' if args.home else 'No'}")
        print(f"   Opponent Strength: {game_context['opponent_strength']:.2f}")
        print(f"   Rest Days:        {game_context['rest_days']}")
        print(f"   Season Clutch FG%: {game_context['season_clutch_pct']:.1f}%")
        print(f"   Minutes per Game:  {game_context['minutes_per_game']:.1f}")
        
        if 'explanation' in result:
            print()
            print(f"💡 Explanation: {result['explanation']}")

if __name__ == "__main__":
    main()