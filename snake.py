import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class SnakeDuelEnv(gym.Env):
    """
    Snake Duel - 2 player snake game in a Gymnasium environment.
    Player 1 (id=1) vs Player 2 (id=2).
    Actions: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self, size=10):
        super(SnakeDuelEnv, self).__init__()
        self.size = size

        # 4 possible moves per player
        self.action_space = spaces.Discrete(4)

        # Observation: grid with values (0 empty, 1 snake1, 2 snake2, 3 apple)
        self.observation_space = spaces.Box(
            low=0, high=3, shape=(size, size), dtype=np.int32
        )

        # Directions for actions
        self.directions = {
            0: (-1, 0),  # UP
            1: (0, 1),   # RIGHT
            2: (1, 0),   # DOWN
            3: (0, -1)   # LEFT
        }

        self.reset()

    def _place_apple(self):
        empty = [(r, c) for r in range(self.size) for c in range(self.size)
                 if all((r, c) not in body for body in self.snakes.values())]
        if empty:
            self.apple = random.choice(empty)
        else:
            self.apple = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Initial snake positions
        self.snakes = {
            1: [(0, 0)],  # Player 1 top-left
            2: [(self.size - 1, self.size - 1)]  # Player 2 bottom-right
        }

        # Initial directions
        self.snake_dirs = {
            1: (0, 1),   # right
            2: (0, -1)   # left
        }

        self.done = False
        self._place_apple()  # spawn apple
        return self._get_obs(), {}

    def _get_obs(self):
        grid = np.zeros((self.size, self.size), dtype=np.int32)
        for pid, body in self.snakes.items():
            for r, c in body:
                grid[r, c] = pid
        if self.apple:
            grid[self.apple] = 3  # mark apple
        return grid

    def step(self, actions):
        """
        actions: dict {1: action_for_player1, 2: action_for_player2}
        0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
        """
        if self.done:
            return self._get_obs(), {1:0, 2:0}, True, False, {}

        rewards = {1: 0.01, 2: 0.01}  # small survival reward
        new_positions = {}

        # Compute new head positions
        for pid in [1, 2]:
            head = self.snakes[pid][0]
            move = self.directions[actions[pid]]
            new_positions[pid] = (head[0] + move[0], head[1] + move[1])

        dead = set()

        # Check collisions
        for pid in [1, 2]:
            r, c = new_positions[pid]
            if not (0 <= r < self.size and 0 <= c < self.size):
                dead.add(pid)
                continue
            opp = 2 if pid == 1 else 1
            if new_positions[pid] in self.snakes[pid] or new_positions[pid] in self.snakes[opp]:
                dead.add(pid)

        # Head-on crash
        if new_positions[1] == new_positions[2]:
            dead.add(1)
            dead.add(2)

        # Update snakes
        for pid in [1, 2]:
            if pid not in dead:
                new_head = new_positions[pid]
                self.snakes[pid].insert(0, new_head)
                if self.apple and new_head == self.apple:
                    rewards[pid] += 0.5  # bonus for eating
                    self._place_apple()  # respawn apple
                else:
                    self.snakes[pid].pop()

        # Assign terminal rewards
        if 1 in dead and 2 not in dead:
            rewards[1] = -1
            rewards[2] = +1
            self.done = True
        elif 2 in dead and 1 not in dead:
            rewards[2] = -1
            rewards[1] = +1
            self.done = True
        elif 1 in dead and 2 in dead:
            rewards[1] = -1
            rewards[2] = -1
            self.done = True

        return self._get_obs(), rewards, self.done, False, {}

    def render(self):
        grid = self._get_obs()
        chars = {0: ".", 1: "S", 2: "O", 3: "A"}
        print("\n".join("".join(chars[val] for val in row) for row in grid))
        print()
        
        
if __name__ == "__main__":
    env = SnakeDuelEnv(size=6)
    obs, _ = env.reset()
    done = False
    for _ in range(20):  # play 20 steps
        if done: break
        actions = {1: env.action_space.sample(), 2: env.action_space.sample()}
        obs, rewards, done, _, _ = env.step(actions)
        env.render()
        print("Rewards:", rewards, "\n")