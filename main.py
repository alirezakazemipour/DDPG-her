import gym
from agent import Agent

ENV_NAME = "MountainCarContinuous-v0"
INTRO = False
MAX_EPISODES = 200
memory_size = 10000
batch_size = 64

test_env = gym.make(ENV_NAME)
state_shape = test_env.observation_space.shape
n_actions = test_env.action_space.shape[0]
action_bounds = [test_env.action_space.low[0], test_env.action_space.high[0]]

if INTRO:
    print(f"state_shape:{state_shape}\n"
          f"number of actions:{n_actions}\n"
          f"action boundaries:{action_bounds}")
    for _ in range(3):
        done = False
        test_env.reset()
        while not done:
            action = test_env.action_space.sample()
            _, r, done, _ = test_env.step(action)
            test_env.render()
else:
    env = gym.make(ENV_NAME)
    agent = Agent(n_states=state_shape,
                  action_bounds=action_bounds,
                  capacity=memory_size,
                  action_size=n_actions,
                  batch_size=batch_size)
    # total_reward = 0
    global_running_r = []
    for episode in range(MAX_EPISODES):
        agent.reset_randomness()
        state = env.reset()
        episode_reward = 0
        ep_actor_loss = 0
        ep_critic_loss = 0
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.store(state, reward, done, action, next_state)
            actor_loss, critic_loss = agent.train()
            ep_actor_loss += actor_loss
            ep_critic_loss += critic_loss
            episode_reward += reward
            if done:
                break
            state = next_state
    if episode == 0:
        global_running_r.append(episode_reward)
    else:
        global_running_r.append(global_running_r[-1] * 0.99 + 0.01 * episode_reward)

    print(f"EP{episode}| "
          f"EP_running_r{global_running_r[-1]:.3f}| "
          f"EP_critic_loss:{ep_critic_loss:.3f}| "
          f"EP_actor_loss:{ep_actor_loss:.3f}")
