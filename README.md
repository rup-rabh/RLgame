# Game AI Project

A collection of reinforcement learning implementations for classic games including Snake Duel and Blackjack.

## 🎮 Games Included

### Snake Duel
A two-player snake game implemented as a Gymnasium environment with AI training capabilities.

### Blackjack
Q-Learning implementation for optimal blackjack strategy using reinforcement learning.

## 📁 Project Structure

```
game/
├── snake.py           # Snake Duel environment (Gymnasium)
├── snakeTrain.py      # PPO training for Snake using Stable Baselines3
├── app.py             # Blackjack game with trained Q-table
├── appnew.py          # (Empty file)
├── BlackJack.ipynb    # Jupyter notebook for Blackjack Q-Learning training
├── blackjack.pkl     # Trained Q-table for Blackjack
├── blackjack.bin     # Binary model file
└── venv/             # Python virtual environment
```

## 🚀 Quick Start

### Prerequisites

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install dependencies (if not already installed)
pip install gymnasium stable-baselines3 numpy matplotlib jupyter tqdm
```

### Snake Duel Training

```bash
# Train a PPO agent to play Snake Duel
python snakeTrain.py
```

Features:
- Two-player snake environment
- PPO (Proximal Policy Optimization) training
- Agent vs random opponent
- Gymnasium-compatible environment

### Blackjack

```bash
# Play Blackjack with trained AI
python app.py
```

Features:
- Q-Learning trained agent
- Optimal strategy based on reinforcement learning
- Interactive gameplay

## 🧠 AI Implementations

### Snake Duel (PPO)
- **Environment**: Custom Gymnasium environment with 2 competing snakes
- **Algorithm**: PPO (Proximal Policy Optimization)
- **Library**: Stable Baselines3
- **State Space**: Grid observation (size × size)
- **Action Space**: 4 discrete actions (UP, RIGHT, DOWN, LEFT)

### Blackjack (Q-Learning)
- **Algorithm**: Q-Learning with epsilon-greedy exploration
- **State Space**: (player_sum, dealer_card, usable_ace)
- **Action Space**: 2 actions (HIT, STICK)
- **Features**: Handles usable aces, optimal strategy learning

## 🔧 Technical Details

### Snake Environment
- Grid-based game with apples as rewards
- Collision detection and game termination
- Multi-agent support with individual rewards
- Configurable grid size

### Training Process
- **Snake**: 50,000 timesteps with PPO
- **Blackjack**: Q-Learning with decaying epsilon exploration
- Models saved for later use and evaluation

## 📊 Files Description

- `snake.py`: Core Snake Duel environment implementation
- `snakeTrain.py`: Training script with PPO wrapper for single-agent learning
- `BlackJack.ipynb`: Complete Q-Learning training notebook with visualization
- `app.py`: Playable Blackjack game using trained model
- `*.pkl, *.bin`: Saved trained models

## 🎯 Usage Examples

### Training Snake AI
```python
from snakeTrain import SingleSnakeWrapper
from stable_baselines3 import PPO

env = SingleSnakeWrapper(size=6)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50000)
```

### Using Blackjack AI
```python
import pickle

# Load trained Q-table
with open("blackjack.pkl", "rb") as f:
    Q = pickle.load(f)

# Use for optimal play decisions
action = choose_action(state)  # Returns optimal action
```

## 🏆 Results

- **Snake**: Trained agent learns to avoid collisions and collect apples
- **Blackjack**: Achieves near-optimal strategy through Q-Learning
- Models saved and ready for gameplay or further training

## 🔮 Future Enhancements

- Add more sophisticated Snake AI opponents
- Implement Deep Q-Networks (DQN) for Blackjack
- Add visualization tools for training progress
- Multi-agent Snake training scenarios
