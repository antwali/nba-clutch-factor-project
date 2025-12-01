#!/usr/bin/env python3
"""
Create a demo model for NBA Clutch Factor.
This generates a simple trained model for demonstration purposes.
"""

import sys
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def create_demo_model():
    """Create a demo model with synthetic data."""
    print("🏀 Creating Demo Model for NBA Clutch Factor")
    print("=" * 60)
    
    # Create model directory if it doesn't exist
    model_dir = "models/trained_models"
    os.makedirs(model_dir, exist_ok=True)
    
    # Generate synthetic training data
    print("📊 Generating synthetic training data...")
    np.random.seed(42)
    n_samples = 1000
    
    # Create feature vectors
    # Features: [home_game, opponent_strength, rest_days, season_clutch_pct, minutes_per_game, player_adjustment]
    X = np.random.rand(n_samples, 6)
    X[:, 0] = np.random.randint(0, 2, n_samples)  # home_game (0 or 1)
    X[:, 1] = np.random.rand(n_samples)  # opponent_strength (0-1)
    X[:, 2] = np.random.randint(0, 5, n_samples)  # rest_days (0-4)
    X[:, 3] = np.random.uniform(0.3, 0.6, n_samples)  # season_clutch_pct (normalized)
    X[:, 4] = np.random.uniform(0.4, 0.8, n_samples)  # minutes_per_game (normalized)
    X[:, 5] = np.random.uniform(-0.3, 0.4, n_samples)  # player_adjustment
    
    # Create target labels (0=Underperform, 1=Expected, 2=Overperform)
    # Rule-based target generation for realistic demo
    y = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        score = 0.0
        score += X[i, 0] * 0.15  # home_game
        score += (1 - X[i, 1]) * 0.25  # opponent_strength (inverse)
        score += min(X[i, 2] * 0.03, 0.1)  # rest_days
        score += (X[i, 3] - 0.45) * 0.3  # season_clutch_pct
        score += X[i, 4] * 0.2  # minutes_per_game
        score += X[i, 5]  # player_adjustment
        
        # Add some randomness
        score += np.random.normal(0, 0.1)
        
        # Classify into categories
        if score > 0.15:
            y[i] = 2  # Overperform
        elif score < -0.15:
            y[i] = 0  # Underperform
        else:
            y[i] = 1  # Expected
    
    print(f"✅ Generated {n_samples} samples")
    print(f"   - Underperform: {np.sum(y == 0)}")
    print(f"   - Expected: {np.sum(y == 1)}")
    print(f"   - Overperform: {np.sum(y == 2)}")
    
    # Create and train model
    print("\n🤖 Training XGBoost model...")
    try:
        from xgboost import XGBClassifier
        
        model = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='mlogloss'
        )
        model.fit(X, y)
        
        # Calculate accuracy
        train_accuracy = model.score(X, y)
        print(f"✅ Model trained successfully!")
        print(f"   Training Accuracy: {train_accuracy:.1%}")
        
    except ImportError:
        print("⚠️  XGBoost not available, using Random Forest instead...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X, y)
        train_accuracy = model.score(X, y)
        print(f"✅ Random Forest model trained!")
        print(f"   Training Accuracy: {train_accuracy:.1%}")
    
    # Create and fit scaler
    print("\n📏 Creating feature scaler...")
    scaler = StandardScaler()
    scaler.fit(X)
    print("✅ Scaler created")
    
    # Save model
    model_path = os.path.join(model_dir, "xgboost_clutch_model.pkl")
    scaler_path = os.path.join(model_dir, "feature_scaler.pkl")
    
    print(f"\n💾 Saving model to {model_path}...")
    joblib.dump(model, model_path)
    print("✅ Model saved")
    
    print(f"\n💾 Saving scaler to {scaler_path}...")
    joblib.dump(scaler, scaler_path)
    print("✅ Scaler saved")
    
    print("\n" + "=" * 60)
    print("🎉 Demo model created successfully!")
    print(f"\nModel files saved to: {model_dir}/")
    print("   - xgboost_clutch_model.pkl")
    print("   - feature_scaler.pkl")
    print("\n💡 The dashboard will now show 'Model Loaded' instead of 'Demo Mode'")

if __name__ == "__main__":
    create_demo_model()

