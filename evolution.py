from player import Player
import numpy as np
from config import CONFIG


class Evolution():

    def __init__(self, mode):
        self.mode = mode

    # calculate fitness of players
    def calculate_fitness(self, players, delta_xs):
        for i, p in enumerate(players):
            p.fitness = delta_xs[i]

    def mutate(self, child):

        # TODO
        # child: an object of class `Player`
        import random
        p = 0.7
        # TODO
        # child: an object of class `Player`
        for i in range(len(child.nn.w)):
            gaussian_noise = np.random.normal(0, 0.3, child.nn.w[i].shape)
            rand = random.uniform(0, 1)

            if rand < p:
                child.nn.w[i] += gaussian_noise

            gaussian_noise = np.random.normal(0, 0.3, child.nn.b[i].shape)
            rand = random.uniform(0, 1)

            if rand < p:
                child.nn.b[i] += gaussian_noise
        return child


    def generate_new_population(self, num_players, prev_players=None):
        # TODO
        # num_players example: 150
        # prev_players: an array of `Player` objects
        # TODO (additional): a selection method other than `fitness proportionate`
        # TODO (additional): implementing crossover

        import random, copy
        # create random generation in the first round
        if prev_players is None:
            return [Player(self.mode) for _ in range(num_players)]

        # in rounds other than the first one:
        else:
            # Q tournoment method for choosing children 
            Q = 10
            parents_list = []
            children = []
            
            for _ in range(num_players):
                random_players = random.sample(prev_players, Q)
                best_player = max(random_players, key=lambda x: x.fitness)
                parents_list.append(copy.deepcopy(best_player))
            
            for _ in range(num_players):
                parents = random.sample(parents_list, 2)
                child = Player('helicopter')
                
                # w1
                above_rate = np.vsplit(parents[0].nn.w[0], 2)
                below_rate = np.vsplit(parents[1].nn.w[0], 2)
                child.nn.w[0] = np.concatenate((above_rate[0], below_rate[1]), axis=0)
                
                # w2
                above_rate = np.hsplit(parents[0].nn.w[1], 2)
                below_rate = np.hsplit(parents[1].nn.w[1], 2)
                child.nn.w[1] = np.concatenate((above_rate[0], below_rate[1]), axis=1)
                
                # b1
                above_rate = np.vsplit(parents[0].nn.b[0].reshape(parents[0].nn.b[0].shape[0], 1), 2)
                below_rate = np.vsplit(parents[1].nn.b[0].reshape(parents[1].nn.b[0].shape[0], 1), 2)
                child.nn.b[0] = np.concatenate((above_rate[0],below_rate[1]), axis=0)
                
                # b2
                child.nn.b[1] = parents[1].nn.b[1]

                children.append(self.mutate(child))
            new_players = children
            return new_players

    def next_population_selection(self, players, num_players):
        # TODO
        # num_players example: 100
        # players: an array of `Player` objects

        # TODO (additional): a selection method other than `top-k`
        # TODO (additional): plotting

        import heapq, random, copy
        
        next_pop = []

        # prev_players: an array of `Player` objects
        if num_players > len(players):
            num_players = len(players)
        max = sum(player.fitness for player in players)
        for _ in range(num_players):
            pick = random.uniform(0, max)
            current = 0
            for prev_player in players:
                current += prev_player.fitness
                if current > pick:
                    m_child = copy.deepcopy(prev_player)
                    next_pop.append(self.mutate(m_child))
                    break

        return next_pop
