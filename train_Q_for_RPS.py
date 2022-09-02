from abbey_three_predict import abbey_three_predict
from collections import defaultdict
import random





def select_optimal_action(q_table, state):
    max_q_value_action = None
    max_q_value = -100000

    if q_table[state]:
        for action, action_q_value in q_table[state].items():
            if action_q_value >= max_q_value:
                max_q_value = action_q_value
                max_q_value_action = action

    return max_q_value_action


def update(q_table, state):
    if random.uniform(0, 1) < epsilon:
        action = random.choice(actions)
    else:
        action = select_optimal_action(q_table, state)

    next_predicted = abbey_three_predict(state[-1])
    
    next_state = next_predicted + state[-1]

    ideal_response = {'R': 'P', 'P': 'S', 'S': 'R'}
    inv_ideal = {k:v for v,k in ideal_response.items()}
    
    if ideal_response[next_predicted] == action:
        reward = 0
                
    elif next_predicted == action:
        reward = 1
        
    elif inv_ideal[next_predicted] == action:
        reward = -1
    
    old_q_value = q_table[state][action]

    # Check if next_state has q values already
    if not q_table[next_state]:
        q_table[next_state] = {action: 0 for action in actions}

    # Maximum q_value for the actions in next state
    next_max = max(q_table[next_state].values())

    # Calculate the new q_value
    new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)

    # Finally, update the q_value
    q_table[state][action] = new_q_value

    return next_state, reward


# def train_agent(q_table, env, num_episodes):
def train_agent(q_table, last_two, num_episodes):
    for i in range(num_episodes):
        # state = env.reset()
        state = last_two
        if not q_table[state]:
            q_table[state] = {
                action: 0 for action in actions}

        epochs = 0
        num_penalties, reward, total_reward = 0, 0, 0
        while total_reward < 30:
            state, reward = update(q_table, state)
            total_reward += reward

            if reward == -10:
                num_penalties += 1

            epochs += 1
        print("\nTraining episode {}".format(i + 1))
        print("Time steps: {}, Penalties: {}, Reward: {}".format(epochs,
                                                                 num_penalties,
                                                                 total_reward))

    print("Training finished.\n")

    return q_table

opponent_history = []
prev_play = ''
if not prev_play:
    prev_play = 'R'
opponent_history.append(prev_play)

if len(opponent_history) < 2:
    last_two = random.choice(['R', 'P', 'S']) + ''.join(opponent_history[-1:])
if len(opponent_history) >= 2:
    last_two = "".join(opponent_history[-2:])
    

# global variables
states = ['RR', 'RP', 'RS', 'PR', 'PP', 'PS', 'SR', 'SP', 'SS']
actions = ['R', 'P', 'S']

# The hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1
num_episodes = 100000
q_table = defaultdict(int, {})
q_table = train_agent(q_table, last_two, num_episodes)
print(q_table)


