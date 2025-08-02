"""
Main prediction module for NBA Clutch Factor.

This module contains the ClutchPredictor class which handles loading trained models
and making predictions about NBA player performance in clutch situations.
"""

import pandas as pd
import numpy as np
import os
import pickle
import joblib
from typing import Dict, List, Tuple, Optional, Any
import logging
import warnings
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClutchPredictor:
    """
    Main predictor class for NBA clutch performance prediction.
    
    This class handles model loading, feature preparation, and prediction
    generation for individual players in specific game contexts.
    """
    
    def __init__(self, model_path: str = "models/trained_models/"):
        """
        Initialize the ClutchPredictor.
        
        Args:
            model_path (str): Path to directory containing trained models
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.model_metadata = {}
        
        # Performance categories
        self.categories = ['Underperform', 'Expected', 'Overperform']
        
        # Feature importance (for demo purposes)
        self.feature_importance = {
            'home_game': 0.15,
            'opponent_strength': 0.25,
            'rest_days': 0.10,
            'season_clutch_pct': 0.30,
            'minutes_per_game': 0.20
        }
        
        logger.info("ClutchPredictor initialized")
        
    def load_model(self, model_name: str = "xgboost_clutch_model.pkl") -> bool:
        """
        Load trained model and associated artifacts.
        
        Args:
            model_name (str): Name of the model file to load
            
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            model_filepath = os.path.join(self.model_path, model_name)
            scaler_filepath = os.path.join(self.model_path, "feature_scaler.pkl")
            
            if os.path.exists(model_filepath):
                self.model = joblib.load(model_filepath)
                logger.info(f"Model {model_name} loaded successfully")
                
                # Try to load scaler if it exists
                if os.path.exists(scaler_filepath):
                    self.scaler = joblib.load(scaler_filepath)
                    logger.info("Feature scaler loaded successfully")
                
                return True
            else:
                logger.warning(f"Model file {model_filepath} not found. Using demo mode.")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
            
    def predict_player_performance(self, 
                                 player_name: str,
                                 game_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict clutch performance for a specific player.
        
        Args:
            player_name (str): Name of the player
            game_context (Dict[str, Any]): Dictionary containing game context features
                - home_game (int): 1 if home game, 0 if away
                - opponent_strength (float): Opponent strength rating (0-1)
                - rest_days (int): Days since last game
                - season_clutch_pct (float): Player's season clutch shooting %
                - minutes_per_game (float): Average minutes per game
                
        Returns:
            Dict[str, Any]: Dictionary containing prediction results
                - prediction (str): Predicted performance category
                - confidence (float): Confidence score (0-1)
                - probabilities (Dict[str, float]): Probability for each category
                - explanation (str): Brief explanation of the prediction
        """
        try:
            # Create feature vector
            features = self._create_feature_vector(player_name, game_context)
            
            if self.model is not None:
                # Use trained model
                result = self._predict_with_model(features)
            else:
                # Use demo prediction logic
                result = self._predict_demo(player_name, game_context, features)
            
            # Add explanation
            result['explanation'] = self._generate_explanation(player_name, game_context, result)
            result['timestamp'] = datetime.now().isoformat()
            result['player_name'] = player_name
            
            logger.info(f"Prediction generated for {player_name}: {result['prediction']}")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction for {player_name}: {str(e)}")
            return self._get_error_result(player_name, str(e))
    
    def predict_multiple_players(self, 
                               player_contexts: List[Tuple[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Predict clutch performance for multiple players.
        
        Args:
            player_contexts: List of (player_name, game_context) tuples
            
        Returns:
            List[Dict[str, Any]]: List of prediction results
        """
        results = []
        
        for player_name, game_context in player_contexts:
            result = self.predict_player_performance(player_name, game_context)
            results.append(result)
        
        logger.info(f"Generated predictions for {len(results)} players")
        return results
    
    def _create_feature_vector(self, 
                              player_name: str, 
                              game_context: Dict[str, Any]) -> List[float]:
        """
        Create feature vector for prediction.
        
        Args:
            player_name (str): Player name
            game_context (Dict[str, Any]): Game context dictionary
            
        Returns:
            List[float]: Feature vector for prediction
        """
        # Extract features with defaults
        features = [
            float(game_context.get('home_game', 0)),
            float(game_context.get('opponent_strength', 0.5)),
            float(game_context.get('rest_days', 1)),
            float(game_context.get('season_clutch_pct', 45.0)) / 100,  # Normalize to 0-1
            float(game_context.get('minutes_per_game', 30.0)) / 48,    # Normalize to 0-1
        ]
        
        # Add player-specific adjustments (simplified)
        player_adjustment = self._get_player_adjustment(player_name)
        features.append(player_adjustment)
        
        return features
    
    def _get_player_adjustment(self, player_name: str) -> float:
        """
        Get player-specific adjustment factor based on historical performance.
        
        Args:
            player_name (str): Player name
            
        Returns:
            float: Adjustment factor (-0.5 to 0.5)
        """
        # Simplified player adjustments for demo
        player_adjustments = {
            'damian lillard': 0.4,
            'lebron james': 0.3,
            'stephen curry': 0.35,
            'kevin durant': 0.3,
            'jimmy butler': 0.25,
            'kyrie irving': 0.2,
            'kawhi leonard': 0.3,
            'paul george': 0.1,
            'james harden': 0.15,
            'russell westbrook': -0.1,
        }
        
        name_lower = player_name.lower()
        return player_adjustments.get(name_lower, 0.0)
    
    def _predict_with_model(self, features: List[float]) -> Dict[str, Any]:
        """
        Make prediction using trained model.
        
        Args:
            features (List[float]): Feature vector
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        try:
            # Scale features if scaler is available
            if self.scaler:
                features_scaled = self.scaler.transform([features])
            else:
                features_scaled = [features]
            
            # Make prediction
            prediction_idx = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            predicted_category = self.categories[prediction_idx]
            confidence = max(probabilities)
            
            prob_dict = {
                self.categories[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
            
            return {
                'prediction': predicted_category,
                'confidence': float(confidence),
                'probabilities': prob_dict,
                'method': 'trained_model'
            }
            
        except Exception as e:
            logger.error(f"Error in model prediction: {str(e)}")
            return self._predict_demo("Unknown", {}, features)
    
    def _predict_demo(self, 
                     player_name: str, 
                     game_context: Dict[str, Any], 
                     features: List[float]) -> Dict[str, Any]:
        """
        Generate demo prediction using rule-based logic.
        
        Args:
            player_name (str): Player name
            game_context (Dict[str, Any]): Game context
            features (List[float]): Feature vector
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        # Rule-based prediction logic for demo
        home_boost = 0.1 if game_context.get('home_game', 0) else 0
        opponent_penalty = game_context.get('opponent_strength', 0.5) * 0.15
        rest_boost = min(game_context.get('rest_days', 1) * 0.03, 0.1)
        clutch_history = (game_context.get('season_clutch_pct', 45.0) - 45) * 0.01
        player_factor = features[-1] if len(features) > 5 else 0  # Player adjustment
        
        # Calculate base probability for overperforming
        base_overperform = 0.33 + home_boost - opponent_penalty + rest_boost + clutch_history + player_factor
        base_overperform = max(0.1, min(0.8, base_overperform))
        
        # Generate probabilities
        overperform_prob = base_overperform
        underperform_prob = max(0.1, min(0.5, 0.4 - player_factor - home_boost + opponent_penalty))
        expected_prob = 1.0 - overperform_prob - underperform_prob
        
        # Ensure probabilities sum to 1
        total = overperform_prob + expected_prob + underperform_prob
        probabilities = [underperform_prob/total, expected_prob/total, overperform_prob/total]
        
        # Determine prediction
        prediction_idx = probabilities.index(max(probabilities))
        predicted_category = self.categories[prediction_idx]
        confidence = max(probabilities)
        
        prob_dict = {
            self.categories[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        return {
            'prediction': predicted_category,
            'confidence': float(confidence),
            'probabilities': prob_dict,
            'method': 'demo_rules'
        }
    
    def _generate_explanation(self, 
                            player_name: str, 
                            game_context: Dict[str, Any], 
                            result: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation for the prediction.
        
        Args:
            player_name (str): Player name
            game_context (Dict[str, Any]): Game context
            result (Dict[str, Any]): Prediction result
            
        Returns:
            str: Explanation text
        """
        prediction = result['prediction']
        confidence = result['confidence']
        
        factors = []
        
        # Home court advantage
        if game_context.get('home_game', 0):
            factors.append("home court advantage")
        else:
            factors.append("playing on the road")
            
        # Opponent strength
        opp_strength = game_context.get('opponent_strength', 0.5)
        if opp_strength > 0.7:
            factors.append("facing a strong opponent")
        elif opp_strength < 0.3:
            factors.append("facing a weaker opponent")
            
        # Rest
        rest_days = game_context.get('rest_days', 1)
        if rest_days >= 3:
            factors.append("well-rested")
        elif rest_days == 0:
            factors.append("playing back-to-back")
            
        # Historical performance
        clutch_pct = game_context.get('season_clutch_pct', 45.0)
        if clutch_pct > 50:
            factors.append("strong clutch history")
        elif clutch_pct < 40:
            factors.append("struggles in clutch situations")
        
        factors_text = ", ".join(factors) if factors else "standard game conditions"
        
        return (f"{player_name} is predicted to {prediction.lower()} "
                f"(confidence: {confidence:.1%}) considering {factors_text}.")
    
    def _get_error_result(self, player_name: str, error_msg: str) -> Dict[str, Any]:
        """
        Generate error result when prediction fails.
        
        Args:
            player_name (str): Player name
            error_msg (str): Error message
            
        Returns:
            Dict[str, Any]: Error result
        """
        return {
            'prediction': 'Error',
            'confidence': 0.0,
            'probabilities': {cat: 0.0 for cat in self.categories},
            'explanation': f"Unable to generate prediction: {error_msg}",
            'player_name': player_name,
            'timestamp': datetime.now().isoformat(),
            'method': 'error'
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict[str, Any]: Model information
        """
        return {
            'model_loaded': self.model is not None,
            'scaler_loaded': self.scaler is not None,
            'categories': self.categories,
            'feature_importance': self.feature_importance,
            'model_path': self.model_path
        }

# Example usage and testing
if __name__ == "__main__":
    print("🏀 NBA Clutch Factor - Predictor Demo")
    print("=" * 50)
    
    # Initialize predictor
    predictor = ClutchPredictor()
    
    # Test single prediction
    game_context = {
        'home_game': 1,
        'opponent_strength': 0.65,
        'rest_days': 2,
        'season_clutch_pct': 48.5,
        'minutes_per_game': 35.2
    }
    
    result = predictor.predict_player_performance("LeBron James", game_context)
    
    print(f"Player: {result['player_name']}")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Explanation: {result['explanation']}")
    
    print(f"\nProbability breakdown:")
    for category, prob in result['probabilities'].items():
        print(f"  {category}: {prob:.1%}")
    
    # Test multiple players
    print(f"\n" + "=" * 50)
    print("Multiple Player Predictions:")
    
    players = [
       ("Stephen Curry", {'home_game': 1, 'opponent_strength': 0.6, 'rest_days': 1, 'season_clutch_pct': 47.3, 'minutes_per_game': 34.7}),
       ("Kevin Durant", {'home_game': 0, 'opponent_strength': 0.7, 'rest_days': 2, 'season_clutch_pct': 52.1, 'minutes_per_game': 37.2}),
       ("Damian Lillard", {'home_game': 1, 'opponent_strength': 0.5, 'rest_days': 0, 'season_clutch_pct': 44.8, 'minutes_per_game': 36.3})
   ]
   
    results = predictor.predict_multiple_players(players)
   
    for result in results:
       print(f"\n{result['player_name']}: {result['prediction']} ({result['confidence']:.1%})")
       print(f"  {result['explanation']}")
   
    # Display model info
    print(f"\n" + "=" * 50)
    print("Model Information:")
    model_info = predictor.get_model_info()
    for key, value in model_info.items():
        print(f"  {key}: {value}")
