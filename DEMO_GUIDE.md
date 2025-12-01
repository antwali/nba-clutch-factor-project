# 🏀 NBA Clutch Factor - Demo Guide

This guide will help you demonstrate the NBA Clutch Factor application effectively.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import streamlit; import plotly; print('✅ All dependencies installed')"
   ```

## Demo Option 1: Interactive Dashboard (Recommended)

### Step 1: Launch the Dashboard

```bash
streamlit run src/dashboard/app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Step 2: Demo Flow

#### **A. Single Player Prediction (Main Feature)**

1. **Start with a popular player:**
   - Select "LeBron James" from the dropdown
   - Keep default settings (Home Game: Yes, Opponent Strength: 0.5)

2. **Click "🚀 Make Prediction"**
   - Show the prediction result with color-coded categories
   - Highlight the probability breakdown chart
   - Point out the confidence score
   - Read the explanation

3. **Adjust parameters to show sensitivity:**
   - Change "Opponent Strength" to 0.8 (strong opponent)
   - Make another prediction
   - Show how prediction changes
   - Explain: "Stronger opponents make clutch situations harder"

4. **Try different scenarios:**
   - Set "Rest Days" to 0 (back-to-back game)
   - Lower "Season Clutch FG%" to 40%
   - Show how predictions adapt

5. **Try a known clutch performer:**
   - Select "Damian Lillard" (known for clutch performance)
   - Set favorable conditions (Home, Rest Days: 2, Clutch FG%: 48%)
   - Show "Overperform" prediction

#### **B. Player Comparison Feature**

1. **Navigate to "📈 Comparison" tab**

2. **Set up a comparison:**
   - Player 1: "LeBron James" (Home, Opponent: 0.6, Rest: 1)
   - Player 2: "Stephen Curry" (Home, Opponent: 0.6, Rest: 1)

3. **Click "Compare Players"**
   - Show the comparison table
   - Highlight the side-by-side probability chart
   - Explain differences in predictions

4. **Add more players:**
   - Increase slider to 3-4 players
   - Show how the comparison scales

#### **C. Model Information**

1. **Navigate to "📊 Model Info" tab**

2. **Show:**
   - Model status (Demo Mode or Trained Model)
   - Feature importance chart
   - Explain what each feature means
   - Show the "About the Model" section

#### **D. Prediction History**

1. **Navigate to "📜 History" tab**

2. **Show:**
   - All previous predictions from the session
   - Explain how this helps track analysis over time

### Step 3: Key Talking Points

**During the demo, highlight:**

1. **Real-time Predictions:**
   - "The model considers multiple factors in real-time"
   - "Each prediction includes probability breakdowns"

2. **Visual Analytics:**
   - "Interactive charts help understand predictions"
   - "Feature importance shows what matters most"

3. **Flexibility:**
   - "Works with any player name"
   - "Adjustable game context for different scenarios"

4. **User-Friendly:**
   - "Clean, intuitive interface"
   - "Multiple ways to interact with predictions"

## Demo Option 2: Command-Line Interface

### Step 1: Basic Prediction

```bash
python scripts/run_predictions.py --player "LeBron James"
```

**Show:**
- Formatted output with prediction
- Probability breakdown with visual bars
- Game context summary
- Explanation

### Step 2: Custom Game Context

```bash
python scripts/run_predictions.py --player "Stephen Curry" \
    --home \
    --opponent 0.7 \
    --rest 2 \
    --clutch 47.5 \
    --mpg 34.0
```

**Show:**
- How to customize all parameters
- How output changes with different contexts

### Step 3: JSON Output (For Developers)

```bash
python scripts/run_predictions.py --player "Kevin Durant" --json
```

**Show:**
- Machine-readable output
- Useful for automation and integration

### Step 4: Multiple Predictions

```bash
# Create a quick comparison
python scripts/run_predictions.py --player "Damian Lillard" --home --opponent 0.6
python scripts/run_predictions.py --player "LeBron James" --home --opponent 0.6
python scripts/run_predictions.py --player "Stephen Curry" --home --opponent 0.6
```

**Show:**
- How to run batch predictions
- Compare outputs side-by-side

## Demo Script (5-Minute Demo)

### Introduction (30 seconds)
- "This is the NBA Clutch Factor app - it predicts how players perform in clutch situations"
- "Clutch time = final 5 minutes with ≤5 point differential"

### Dashboard Walkthrough (3 minutes)

1. **Single Prediction (1 min):**
   - Select "LeBron James"
   - Show prediction with charts
   - Adjust opponent strength, show change

2. **Comparison (1 min):**
   - Switch to Comparison tab
   - Compare 2-3 players
   - Show comparison chart

3. **Model Info (30 sec):**
   - Show feature importance
   - Explain model transparency

### CLI Demo (1 minute)
- Show command-line usage
- Demonstrate JSON output

### Wrap-up (30 seconds)
- "Works with any player"
- "Considers game context"
- "Provides probability breakdowns"

## Demo Tips

### ✅ Do:
- Start with a well-known player (LeBron, Curry, Lillard)
- Show how changing parameters affects predictions
- Highlight the visualizations
- Explain the "why" behind predictions
- Use realistic game scenarios

### ❌ Don't:
- Don't use obscure player names
- Don't skip the visualizations
- Don't just show one prediction
- Don't forget to explain the features

## Troubleshooting

### If dashboard doesn't start:
```bash
# Check if Streamlit is installed
pip install streamlit

# Try running with explicit Python
python -m streamlit run src/dashboard/app.py
```

### If predictions seem off:
- This is normal - the app uses rule-based predictions in demo mode
- Explain that trained models can be loaded when available
- The logic is still based on real NBA factors

### If browser doesn't open:
- Manually navigate to `http://localhost:8501`
- Check terminal for the exact URL

## Advanced Demo Scenarios

### Scenario 1: Playoff Game
- High opponent strength (0.8)
- Home game
- Well-rested (3 days)
- Show how these factors combine

### Scenario 2: Back-to-Back Road Game
- Away game (uncheck Home)
- Rest days: 0
- Strong opponent (0.7)
- Show increased difficulty

### Scenario 3: Clutch Specialist
- Use "Damian Lillard"
- High season clutch FG% (48%)
- Favorable conditions
- Show "Overperform" prediction

## Questions to Prepare For

**Q: How accurate is this?**
A: The model achieves 74%+ accuracy when trained. Currently running in demo mode with rule-based logic that considers real NBA factors.

**Q: Can I use my own data?**
A: Yes! The predictor class can load trained models from the `models/trained_models/` directory.

**Q: What makes a player "clutch"?**
A: The model considers historical clutch performance, game context (home/away, opponent, rest), and playing time.

**Q: Can I compare more players?**
A: Yes! The comparison tab supports up to 5 players simultaneously.

## Quick Reference

### Dashboard URL
- Default: `http://localhost:8501`
- Check terminal for actual URL

### Key Players to Demo
- LeBron James (versatile, well-known)
- Stephen Curry (shooter, clutch reputation)
- Damian Lillard (known clutch performer)
- Kevin Durant (scorer)

### Key Features to Highlight
1. Real-time predictions
2. Interactive visualizations
3. Player comparison
4. Model transparency
5. Flexible game context

---

**Ready to demo?** Start with: `streamlit run src/dashboard/app.py`

