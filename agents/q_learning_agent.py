import numpy as np

class Agent():
    '''
    Classical implementation of a generic agent for Q learning. 
    Nothing specific for the Snake.
    '''
    def __init__(self, lr, gamma, n_actions, n_states, eps_start, eps_end, eps_dec, rand=True):
        self.lr = lr
        self.gamma = gamma
        self.n_actions = n_actions
        self.n_states = n_states
        self.epsilon = eps_start
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.random = rand
        self.Q = {}

        self.init_Q()

    def init_Q(self):
        for state in range(self.n_states):
            for action in range(self.n_actions):
                self.Q[(state, action)] = 0.0

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.n_actions)
        else:
            q = np.array([self.Q[(state, a)] for a in range(self.n_actions)])
            if self.random:
                exp_q = np.exp(q)
                probs = exp_q/exp_q.sum() # softmax
                action = np.random.choice(self.n_actions, p=probs)
            else:
                action = np.argmax(q)
        return action

    def decrement_epsilon(self):
        self.epsilon = self.epsilon*self.eps_dec if self.epsilon>self.eps_min else self.eps_min

    def learn(self, state, action, reward, state_):
        actions = np.array([self.Q[(state_, a)] for a in range(self.n_actions)])
        a_max = np.argmax(actions)

        self.Q[(state, action)] += self.lr*(reward +
                                        self.gamma*self.Q[(state_, a_max)] -
                                        self.Q[(state, action)])
        self.decrement_epsilon()
        
    def save(self, filename='qtable.npy'):
        np.save(filename, self.Q)
        
    def load(self, filename='qtable.npy'):
        self.Q = np.load(filename, allow_pickle=True)

print("Q-learning agent v0.0.4")