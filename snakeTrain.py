import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from snake import SnakeDuelEnv

class SingleSnakeWrapper(gym.Env):
    """
    Wrap SnakeDuelEnv for SB3 single-agent training (Gymnasium API).
    Snake1 (id=1) = learning agent
    Snake2 (id=2) = random opponent
    """
    def __init__(self, size=10):
        super().__init__()
        self.env = SnakeDuelEnv(size=size)

        # ✅ Define spaces for SB3
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self, **kwargs):
        obs, info = self.env.reset()
        return obs, info

    def step(self, action):
        # Opponent takes random action
        opp_action = self.env.action_space.sample()
        # Convert numpy array to int if needed
        action = int(action) if hasattr(action, 'item') else action
        actions = {1: action, 2: opp_action}

        obs, rewards, terminated, truncated, info = self.env.step(actions)
        return obs, rewards[1], terminated, truncated, info

    def render(self):
        self.env.render()


# ---- Usage ----
env = SingleSnakeWrapper(size=6)
check_env(env, warn=True)   # should pass now

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50000)
model.save("snake_duel_vs_random")

obs, info = env.reset()
terminated = False
truncated = False
while not (terminated or truncated):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()