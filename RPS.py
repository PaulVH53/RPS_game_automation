import random
from collections import defaultdict


def player(prev_play, opponent_history=[]):
    if prev_play == '': 
        prev_play = random.choice(['R','P','S'])
    opponent_history.append(prev_play)
    if len(opponent_history) < 2:
        last_two = random.choice(['R', 'P', 'S']) + ''.join(opponent_history[-1:])
    if len(opponent_history) >= 2:
        last_two = "".join(opponent_history[-2:])
    
    # global variables
    # states = ['RR', 'RP', 'RS', 'PR', 'PP', 'PS', 'SR', 'SP', 'SS']
    actions = ['R', 'P', 'S']
    
    # The hyperparameters
    alpha = 0.1     # 0.1
    gamma = 0.15    # 0.15
    epsilon = 0.5   # 0.5
    num_episodes = 1200   #1000 1250
    
    def kris_predict(prev_opponent_play):
        if prev_opponent_play == '':
            prev_opponent_play = "R"
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[prev_opponent_play]
    
    def abbey_three_predict(prev_opponent_play,
              opponent_history=[],
              play_order=[{'RRR': 0, 'RRP': 0, 'RRS': 0, 'RSR': 0, 'RSP': 0, 'RSS': 0,'RPR': 0, 'RPP': 0, 'RPS': 0,
                     'PRR': 0, 'PRP': 0, 'PRS': 0, 'PSR': 0, 'PSP': 0, 'PSS': 0,'PPR': 0, 'PPP': 0, 'PPS': 0,
                     'SRR': 0, 'SRP': 0, 'SRS': 0, 'SSR': 0, 'SSP': 0, 'SSS': 0,'SPR': 0, 'SPP': 0, 'SPS': 0
                     }]):
        
        if not prev_opponent_play:
            prev_opponent_play = 'R'
        opponent_history.append(prev_opponent_play)
        
        last_three = "".join(opponent_history[-3:])
        if len(last_three) == 3:
            play_order[0][last_three] += 1
            
        last_two = last_three[-2:]
        last_two = "".join(last_two)
        if len(last_two) == 1:
            missing = random.choice(['R', 'P', 'S'])
            last_two = missing + last_two 
        potential_plays = [
            last_two + "R",
            last_two + "P",
            last_two + "S",
        ]
            
        sub_order = {
            k: play_order[0][k]
            for k in potential_plays if k in play_order[0]
        }
            
        # finds max most recent
        prediction = [key for key, value in sub_order.items() if value == max(sub_order.values())][-1][-1]
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    
        return ideal_response[prediction]
    
    
    def select_optimal_action(q_table, state):
        max_q_value_action = None
        max_q_value = -10000   # -10000
    
        if q_table[state]:
            for action, action_q_value in q_table[state].items():
                if action_q_value >= max_q_value:
                    max_q_value = action_q_value
                    max_q_value_action = action
    
        return max_q_value_action
    
    
    def update(q_table, state):
        rand_unif = random.uniform(0, 1)
        if rand_unif < epsilon:
            action = random.choice(actions)
        else:
            action = select_optimal_action(q_table, state)
    
        if rand_unif < epsilon / 3:
            next_predicted = kris_predict(state[-1])
        else:
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
            state = last_two
            if not q_table[state]:
                q_table[state] = {
                    action: 0 for action in actions}
    
            epochs = 0
            num_penalties, reward, total_reward = 0, 0, 0
            while total_reward < 25:   # <25
                state, reward = update(q_table, state)
                total_reward += reward
    
                if reward == -10:
                    num_penalties += 1
    
                epochs += 1
        #     print("\nTraining episode {}".format(i + 1))
        #     print("Time steps: {}, Penalties: {}, Reward: {}".format(epochs,
        #                                                              num_penalties,
        #                                                              total_reward))
    
        # print("Training finished.\n")
    
        return q_table
    
    
    q_table = defaultdict(int, {})
    q_table = train_agent(q_table, last_two, num_episodes)
    
    next = [key for key, value in q_table[last_two].items() if value == max(q_table[last_two].values())][-1]
    # ideal_response = {'R': 'P', 'P': 'S', 'S': 'R'}
    guess = next
    return guess
    