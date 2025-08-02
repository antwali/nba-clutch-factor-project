"""
Feature engineering for clutch performance metrics.

This module calculates various clutch-specific metrics for NBA players,
including shooting percentages, turnover rates, and contextual features
that influence performance in high-pressure situations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClutchMetricsCalculator:
    """
    Calculates clutch-specific performance metrics for NBA players.
    
    This class provides methods to compute various statistics that are
    particularly relevant to clutch-time performance, including shooting
    efficiency, playmaking, and situational factors.
    """
    
    def __init__(self):
        """Initialize the ClutchMetricsCalculator."""
        self.metrics_cache = {}
        self.min_clutch_attempts = 5  # Minimum attempts for reliable statistics
        
        logger.info("ClutchMetricsCalculator initialized")
    
    def calculate_clutch_shooting_pct(self, player_data: pd.DataFrame) -> float:
        """
        Calculate clutch shooting percentage for a player.
        
        Args:
            player_data (pd.DataFrame): DataFrame with player's game data
            
        Returns:
            float: Clutch shooting percentage (0-100)
        """
        try:
            # Filter for clutch situations
            clutch_shots = player_data[
                (player_data.get('is_clutch', False) == True) & 
                (player_data.get('event_type', '') == 'shot')
            ]
            
            if len(clutch_shots) == 0:
                logger.warning("No clutch shots found for player")
                return 0.0
                
            # Calculate shooting percentage
            if 'shot_made' in clutch_shots.columns:
                makes = clutch_shots['shot_made'].sum()
                attempts = len(clutch_shots)
            else:
                # Simulate shot outcomes for demo
                np.random.seed(42)
                makes = np.random.binomial(len(clutch_shots), 0.45)  # ~45% shooting
                attempts = len(clutch_shots)
            
            if attempts < self.min_clutch_attempts:
                logger.warning(f"Limited clutch data: {attempts} attempts")
            
            percentage = (makes / attempts) * 100 if attempts > 0 else 0.0
            
            logger.debug(f"Clutch shooting: {makes}/{attempts} = {percentage:.1f}%")
            return percentage
            
        except Exception as e:
            logger.error(f"Error calculating clutch shooting percentage: {str(e)}")
            return 0.0
    
    def calculate_clutch_turnover_rate(self, player_data: pd.DataFrame) -> float:
        """
        Calculate turnover rate in clutch situations.
        
        Args:
            player_data (pd.DataFrame): DataFrame with player's game data
            
        Returns:
            float: Clutch turnover rate per 100 possessions
        """
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if len(clutch_data) == 0:
                return 0.0
            
            # Count turnovers
            if 'event_type' in clutch_data.columns:
                turnovers = len(clutch_data[clutch_data['event_type'] == 'turnover'])
            else:
                # Simulate turnover data for demo
                turnovers = max(1, len(clutch_data) // 20)  # ~5% turnover rate
            
            # Estimate possessions (simplified calculation)
            possessions = len(clutch_data) // 4  # Rough estimate
            
            if possessions == 0:
                return 0.0
                
            turnover_rate = (turnovers / possessions) * 100
            
            logger.debug(f"Clutch turnovers: {turnovers} in {possessions} possessions = {turnover_rate:.1f}%")
            return turnover_rate
            
        except Exception as e:
            logger.error(f"Error calculating clutch turnover rate: {str(e)}")
            return 0.0
    
    def calculate_clutch_assist_rate(self, player_data: pd.DataFrame) -> float:
        """
        Calculate assist rate in clutch situations.
        
        Args:
            player_data (pd.DataFrame): DataFrame with player's game data
            
        Returns:
            float: Clutch assist rate per game
        """
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if len(clutch_data) == 0:
                return 0.0
            
            # Count assists
            if 'event_type' in clutch_data.columns:
                assists = len(clutch_data[clutch_data['event_type'] == 'assist'])
            else:
                # Simulate assist data
                assists = max(0, len(clutch_data) // 15)  # Roughly realistic ratio
            
            # Count games with clutch time
            games = clutch_data.get('game_id', clutch_data.index).nunique()
            
            assist_rate = assists / games if games > 0 else 0.0
            
            logger.debug(f"Clutch assists: {assists} in {games} games = {assist_rate:.1f} per game")
            return assist_rate
            
        except Exception as e:
            logger.error(f"Error calculating clutch assist rate: {str(e)}")
            return 0.0
    
    def calculate_opponent_strength_rating(self, game_data: pd.DataFrame) -> float:
        """
        Calculate opponent strength rating based on team performance.
        
        Args:
            game_data (pd.DataFrame): DataFrame with game information
            
        Returns:
            float: Opponent strength rating (0-1 scale)
        """
        try:
            if 'opponent_team_id' not in game_data.columns:
                # Return neutral rating if no opponent data
                return 0.5
            
            opponent_teams = game_data['opponent_team_id'].unique()
            
            # Simulate team strength ratings for demo
            np.random.seed(42)
            team_strengths = {}
            
            for team_id in opponent_teams:
                # Generate realistic team strength (0.2 to 0.8)
                strength = 0.2 + (team_id % 100) / 100 * 0.6
                team_strengths[team_id] = strength
            
            # Calculate weighted average based on games played
            total_strength = 0
            total_games = 0
            
            for team_id in opponent_teams:
                games_vs_team = len(game_data[game_data['opponent_team_id'] == team_id])
                total_strength += team_strengths[team_id] * games_vs_team
                total_games += games_vs_team
            
            avg_opponent_strength = total_strength / total_games if total_games > 0 else 0.5
            
            logger.debug(f"Average opponent strength: {avg_opponent_strength:.3f}")
            return avg_opponent_strength
            
        except Exception as e:
            logger.error(f"Error calculating opponent strength: {str(e)}")
            return 0.5
    
    def calculate_player_clutch_features(self, 
                                       player_id: str, 
                                       game_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate comprehensive clutch features for a specific player.
        
        Args:
            player_id (str): Unique identifier for the player
            game_data (pd.DataFrame): Complete game dataset
            
        Returns:
            Dict[str, float]: Dictionary of calculated features
        """
        try:
            # Filter data for specific player
            if 'player_id' in game_data.columns:
                player_data = game_data[game_data['player_id'] == player_id]
            else:
                # Use all data if no player_id column (demo mode)
                player_data = game_data
            
            if len(player_data) == 0:
                logger.warning(f"No data found for player {player_id}")
                return self._get_default_features()
            
            # Calculate all clutch features
            features = {
                'clutch_shooting_pct': self.calculate_clutch_shooting_pct(player_data),
                'clutch_turnover_rate': self.calculate_clutch_turnover_rate(player_data),
                'clutch_assist_rate': self.calculate_clutch_assist_rate(player_data),
                'clutch_minutes_avg': self._calculate_avg_clutch_minutes(player_data),
                'clutch_games_played': self._count_clutch_games(player_data),
                'opponent_strength_avg': self.calculate_opponent_strength_rating(player_data),
                'home_game_pct': self._calculate_home_game_percentage(player_data),
                'rest_days_avg': self._calculate_avg_rest_days(player_data),
                'clutch_efficiency': self._calculate_clutch_efficiency(player_data),
                'pressure_index': self._calculate_pressure_index(player_data)
            }
            
            # Cache results
            self.metrics_cache[player_id] = features
            
            logger.info(f"Calculated {len(features)} features for player {player_id}")
            return features
            
        except Exception as e:
            logger.error(f"Error calculating features for player {player_id}: {str(e)}")
            return self._get_default_features()
    
    def _calculate_avg_clutch_minutes(self, player_data: pd.DataFrame) -> float:
        """Calculate average minutes played in clutch time per game."""
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if len(clutch_data) == 0:
                return 0.0
            
            # Group by game and sum clutch minutes
            if 'game_id' in clutch_data.columns and 'minutes_remaining' in clutch_data.columns:
                clutch_minutes_per_game = clutch_data.groupby('game_id')['minutes_remaining'].count() / 10  # Rough conversion
                return clutch_minutes_per_game.mean()
            else:
                # Estimate based on clutch appearances
                games_with_clutch = clutch_data.get('game_id', clutch_data.index).nunique()
                return len(clutch_data) / games_with_clutch * 0.5 if games_with_clutch > 0 else 0.0
                
        except Exception as e:
            logger.debug(f"Error calculating avg clutch minutes: {str(e)}")
            return 2.5  # Default estimate
    
    def _count_clutch_games(self, player_data: pd.DataFrame) -> int:
        """Count number of games with clutch time appearances."""
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if 'game_id' in clutch_data.columns:
                return clutch_data['game_id'].nunique()
            else:
                # Estimate based on total clutch situations
                return max(1, len(clutch_data) // 10)  # Rough estimate
                
        except Exception as e:
            logger.debug(f"Error counting clutch games: {str(e)}")
            return 0
    
    def _calculate_home_game_percentage(self, player_data: pd.DataFrame) -> float:
        """Calculate percentage of games played at home."""
        try:
            if 'home_game' in player_data.columns:
                return player_data['home_game'].mean() * 100
            else:
                # Assume roughly 50% home games
                return 50.0
                
        except Exception as e:
            logger.debug(f"Error calculating home game percentage: {str(e)}")
            return 50.0
    
    def _calculate_avg_rest_days(self, player_data: pd.DataFrame) -> float:
        """Calculate average rest days between games."""
        try:
            if 'game_date' in player_data.columns:
                dates = pd.to_datetime(player_data['game_date']).sort_values()
                rest_days = dates.diff().dt.days - 1  # Subtract 1 to get rest days
                return rest_days.mean()
            else:
                # Default assumption of ~1.5 rest days on average
                return 1.5
                
        except Exception as e:
            logger.debug(f"Error calculating avg rest days: {str(e)}")
            return 1.5
    
    def _calculate_clutch_efficiency(self, player_data: pd.DataFrame) -> float:
        """Calculate overall clutch efficiency rating."""
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if len(clutch_data) == 0:
                return 50.0  # Neutral efficiency
            
            # Simplified efficiency calculation
            shooting_pct = self.calculate_clutch_shooting_pct(player_data)
            turnover_rate = self.calculate_clutch_turnover_rate(player_data)
            assist_rate = self.calculate_clutch_assist_rate(player_data)
            
            # Weighted efficiency score
            efficiency = (shooting_pct * 0.5) + ((100 - turnover_rate) * 0.3) + (assist_rate * 10 * 0.2)
            
            return max(0.0, min(100.0, efficiency))  # Clamp to 0-100 range
            
        except Exception as e:
            logger.debug(f"Error calculating clutch efficiency: {str(e)}")
            return 50.0
    
    def _calculate_pressure_index(self, player_data: pd.DataFrame) -> float:
        """Calculate a pressure index based on game situations."""
        try:
            clutch_data = player_data[player_data.get('is_clutch', False) == True]
            
            if len(clutch_data) == 0:
                return 50.0  # Neutral pressure
            
            # Factors that increase pressure
            pressure_factors = []
            
            # Close games (smaller score differential = more pressure)
            if 'score_diff' in clutch_data.columns:
                avg_score_diff = clutch_data['score_diff'].mean()
                pressure_factors.append((5 - avg_score_diff) * 10)  # Higher pressure for closer games
            
            # Playoff games (if available)
            if 'is_playoff' in clutch_data.columns:
                playoff_pct = clutch_data['is_playoff'].mean()
                pressure_factors.append(playoff_pct * 20)  # Playoffs add pressure
            
            # Away games (road games are more pressure)
            if 'home_game' in clutch_data.columns:
                away_pct = 1 - clutch_data['home_game'].mean()
                pressure_factors.append(away_pct * 10)
            
            # Calculate average pressure index
            if pressure_factors:
                pressure_index = sum(pressure_factors) / len(pressure_factors) + 50  # Base 50
            else:
                pressure_index = 50.0  # Default neutral
            
            return max(0.0, min(100.0, pressure_index))  # Clamp to 0-100
            
        except Exception as e:
            logger.debug(f"Error calculating pressure index: {str(e)}")
            return 50.0
    
    def _get_default_features(self) -> Dict[str, float]:
        """Get default feature values when calculation fails."""
        return {
            'clutch_shooting_pct': 45.0,
            'clutch_turnover_rate': 15.0,
            'clutch_assist_rate': 2.0,
            'clutch_minutes_avg': 2.5,
            'clutch_games_played': 20,
            'opponent_strength_avg': 0.5,
            'home_game_pct': 50.0,
            'rest_days_avg': 1.5,
            'clutch_efficiency': 50.0,
            'pressure_index': 50.0
        }
    
    def generate_feature_summary(self, features: Dict[str, float]) -> str:
        """
        Generate a human-readable summary of player features.
        
        Args:
            features (Dict[str, float]): Calculated features
            
        Returns:
            str: Summary text
        """
        try:
            summary_parts = []
            
            # Shooting performance
            shooting_pct = features.get('clutch_shooting_pct', 45.0)
            if shooting_pct > 50:
                summary_parts.append("excellent clutch shooter")
            elif shooting_pct > 45:
                summary_parts.append("solid clutch shooter")
            else:
                summary_parts.append("struggles with clutch shooting")
            
            # Playmaking
            assist_rate = features.get('clutch_assist_rate', 2.0)
            if assist_rate > 3:
                summary_parts.append("strong clutch playmaker")
            elif assist_rate > 1.5:
                summary_parts.append("decent clutch playmaker")
            
            # Ball security
            turnover_rate = features.get('clutch_turnover_rate', 15.0)
            if turnover_rate < 10:
                summary_parts.append("protects the ball well")
            elif turnover_rate > 20:
                summary_parts.append("prone to clutch turnovers")
            
            # Experience
            clutch_games = features.get('clutch_games_played', 20)
            if clutch_games > 40:
                summary_parts.append("extensive clutch experience")
            elif clutch_games < 10:
                summary_parts.append("limited clutch experience")
            
            if summary_parts:
                return f"Player profile: {', '.join(summary_parts)}."
            else:
                return "Standard clutch performer with typical statistics."
                
        except Exception as e:
            logger.error(f"Error generating feature summary: {str(e)}")
            return "Unable to generate player summary."

# Example usage and testing
if __name__ == "__main__":
    print("🏀 NBA Clutch Factor - Feature Engineering Demo")
    print("=" * 60)
    
    # Initialize calculator
    calculator = ClutchMetricsCalculator()
    
    # Create sample player data
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'player_id': ['player_123'] * 100,
        'game_id': np.random.randint(1, 21, 100),
        'event_type': np.random.choice(['shot', 'assist', 'turnover', 'rebound'], 100),
        'is_clutch': np.random.choice([True, False], 100, p=[0.2, 0.8]),
        'shot_made': np.random.choice([0, 1], 100, p=[0.55, 0.45]),
        'home_game': np.random.choice([0, 1], 100, p=[0.5, 0.5]),
        'score_diff': np.random.randint(0, 10, 100)
    })
    
    print(f"Sample data created: {len(sample_data)} records")
    print(f"Clutch situations: {sample_data['is_clutch'].sum()}")
    
    # Calculate features
    features = calculator.calculate_player_clutch_features('player_123', sample_data)
    
    print(f"\nCalculated Features:")
    print("-" * 40)
    for feature_name, value in features.items():
        if isinstance(value, float):
            print(f"{feature_name:25}: {value:6.1f}")
        else:
            print(f"{feature_name:25}: {value:6}")
    
    # Generate summary
    summary = calculator.generate_feature_summary(features)
    print(f"\nPlayer Summary:")
    print(f"{summary}")
    
    print(f"\n" + "=" * 60)
    print("Feature engineering demo completed successfully!")
