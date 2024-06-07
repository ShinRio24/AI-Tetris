import numpy as np

# Define the environment
n_states = 7340032  # Number of states in the grid world
#look at only the first 5 rows
#^^ if this option dosent work
#look at the very top open piece of each column so only 10 postiions
#4^10 (4 max heights for all 10 cloums) * 7 (variations of next piece)
#

n_actions = 40  # Number of possible actions (up, down, left, right)
#down right rotate (make the piece start at the very top left)

goal_state = 15  # Goal state
#idk maybe 100000000? need to figure this out later


# Initialize Q-table with zeros (or import table)
Q_table = np.zeros((n_states, n_actions))

# Define parameters
learning_rate = 0.8
discount_factor = 0.95

#make this value realyl close to zero when you are running a showcase run
#for testing make this value higher?
exploration_prob = 0.2

#amount of iterations
epochs = 5


# Q-learning algorithm
for epoch in range(epochs):
    current_state = np.random.randint(0, n_states)  # Start from a random state

    while current_state != goal_state:
        # Choose action with epsilon-greedy strategy
        if np.random.rand() < exploration_prob:
            action = np.random.randint(0, n_actions)  # Explore
        else:
            action = np.argmax(Q_table[current_state])  # Exploit


        # Simulate the environment (move to the next state)
        # For simplicity, move to the next state
        next_state = (current_state + 1) % n_states


        # Define a simple reward function (1 if the goal state is reached, 0 otherwise)
        reward = 1 if next_state == goal_state else 0

        # Update Q-value using the Q-learning update rule
        Q_table[current_state, action] += learning_rate * \
            (reward + discount_factor *
             np.max(Q_table[next_state]) - Q_table[current_state, action])

        current_state = next_state  # Move to the next state

# After training, the Q-table represents the learned Q-values
print("Learned Q-table:")
print(Q_table)