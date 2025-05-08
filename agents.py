
from abc import abstractmethod

import numpy as np


class Portfolio(object):
    def __init__(self, gold: int = 0, heart: int = 0, time_stone: int = 0):
        self.gold = gold
        self.heart = heart
        self.time_stone = time_stone

    def __repr__(self):
        return f"Portfolio(gold={self.gold:.2f}, heart={self.heart:.2f}, time_stone={self.time_stone:.2f})"
    
    def __add__(self, other):
        return Portfolio(
            self.gold + other.gold,
            self.heart + other.heart,
            self.time_stone + other.time_stone
        )
    
    def __sub__(self, other):
        return Portfolio(
            self.gold - other.gold,
            self.heart - other.heart,
            self.time_stone - other.time_stone
        )
    
    def to_numpy(self):
        return np.array([self.gold, self.heart, self.time_stone])


class Agent(object):
    def __init__(self, score_mean: float=0, score_std: float=1):
        self.score_mean = score_mean
        self.score_std = score_std
        self.portfolio = Portfolio()

        self._state = {}

    def reset(self):
        # Reset the portfolio to zero
        self.portfolio = Portfolio()
        self._state = {}

    def update_portfolio(self, portfolio_change: Portfolio):
        # Update the portfolio with the changes
        self.portfolio += portfolio_change


    def __repr__(self):
        return f"Agent(score_mean={self.score_mean}, score_std={self.score_std}, portfolio={self.portfolio})"
    
    
    def on_game_start(self, agents, game, bank_bids=None, bank_asks=None):
        pass
    
    def get_trades(self, agents, game):
        # return format is dict of ticker: (price willing to trade, signed quantity, self)
        return {}
    
    def on_trades_end(self, agents, game):
        # do something after trades
        pass

    def get_score(self):
        # return the score of the agent
        return np.random.randn(1)[0] * self.score_std + self.score_mean
    
    def on_game_end(self, agents, game):
        self._state = {}

class Bank(Agent):
    @abstractmethod
    def get_bids(self, agents, game) -> dict[str, float]:
        # others sell at bids
        pass
    
    @abstractmethod
    def get_asks(self, agents, game) -> dict[str, float]:
        # others buy at asks
        pass
