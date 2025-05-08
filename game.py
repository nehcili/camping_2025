from collections import defaultdict
from typing import Union

import numpy as np

from agents import Agent, Bank, Portfolio



class Game(object):
    def _facilitate_single_ticker_trades(self, agents: Agent, order_book: list[tuple], ticker: str, bank_bid: float, bank_ask: float):
        buy_orders = sorted(filter(lambda x: x[1] > 0, order_book), reverse=True)
        sell_orders = sorted(filter(lambda x: x[1] < 0, order_book))

        i = j = 0
        while i < len(buy_orders) and j < len(sell_orders):
            buy_price, buy_qty, buy_agent = buy_orders[i]
            sell_price, sell_qty, sell_agent = sell_orders[j]

            if buy_price < sell_price:
                break

            trade_qty = min(buy_qty, -sell_qty)
            price = (buy_price + sell_price) / 2
            buy_agent.update_portfolio(Portfolio(**{ticker: trade_qty, 'gold': -trade_qty * price}))
            sell_agent.update_portfolio(Portfolio(**{ticker: -trade_qty, 'gold': trade_qty * price}))

            if buy_qty > -trade_qty:
                j += 1
                buy_orders[i] = (buy_price, buy_qty - trade_qty, buy_agent)
            else:
                i += 1
                buy_orders[i] = (buy_price, buy_qty + trade_qty, buy_agent)

        while i < len(buy_orders):
            buy_price, buy_qty, buy_agent = buy_orders[i]
            if buy_price <= bank_ask:
                buy_agent.update_portfolio(Portfolio(**{ticker: -buy_qty, 'gold': buy_qty * bank_ask}))
            i += 1
        
        while j < len(sell_orders):
            sell_price, sell_qty, sell_agent = sell_orders[j]
            if sell_price >= bank_bid:
                sell_agent.update_portfolio(Portfolio(**{ticker: -sell_qty, 'gold': -sell_qty * bank_bid}))
            j += 1


    def _facilitate_trades(self, agents: list[Agent], trades: list[dict[str, tuple]], bank_bids: dict[str, float] = None, bank_asks: dict[str, float] = None):
        order_books = defaultdict(list)
        for trade in trades:
            for ticker, order in trade.items():
                order_books[ticker].append(order)

        for ticker, order_book in order_books.items():
            self._facilitate_single_ticker_trades(agents, order_book, ticker, bank_bids[ticker], bank_asks[ticker])

    def on_game_start(self, agents: list[Agent], bank: Agent):
        bids = bank.get_bids(agents, self)
        asks = bank.get_asks(agents, self)

        for agent in agents:
            # look at the game and foes, decide what internal variables to set
            agent.on_game_start(agents=agents, game=self, bank_bids=bids, bank_ask=asks)

        # facilitate trades
        trades = [agent.get_trades(agents, self) for agent in agents]
        self._facilitate_trades(agents, trades)

        for agent in agents:
            # in case trades are not filled, ask the bank for the rest of the trades.
            agent.on_trades_end(agents=agents, game=self)

    def on_game(self, agents: list[Agent], bank: Bank):
        pass

    def distribute_rewards(self, agents: list[Agent], bank: Bank):


    def play(self, agents: list[Agent], bank: Agent):
        # let agents know what game we are playing
        self.on_game_start(agents, bank)

        # play the game
        scores = self.game()
        # higher score = lower rank; lowest rank is the best
        ranks = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)

        if isinstance(self.rewards, Portfolio):
            for agent in agents:
                agent.update_portfolio(self.rewards)
                if agent.portfolio.heart <= 0:
                    agent.reset()
        else:
            # rank[0] is the best agent
            for reward, rank in zip(self.rewards, ranks):
                agents[rank].update_portfolio(reward)

    

class GameSeries(object):
    def __init__(self, games: list[Game], n: int = 1000):
        self.n = n
        self.games = games

    def play(self, agents: list[Agent], bank: Bank):
        res = []
        for i in range(self.n):
            agents = [agent.reset() for agent in agents]
            bank.reset()

            for game in self.games:
                game.play(agents=agents, bank=bank)

            single_res = []
            for agent in agents:
                single_res.append(agent.portfolio.to_numpy())
            
            res.append(np.array(single_res))
        
        # return shape = n x agent x # of assets
        return np.array(res)




    


    # Example usage
    bank = Feds()
    agents = [
        BuyHeartAgent(score_mean=0, score_std=1),
        SellHeartAgent(score_mean=0, score_std=1),
        SellHeartAgent(score_mean=0, score_std=1),
        SellHeartAgent(score_mean=0, score_std=1),
    ]

    for agent in agents:
        print(agent)

    game = Game(rewards=Portfolio(), modifiers={})
    game._facilitate_trades(
        agents=agents,
        trades=[
            {'heart': (10, 3, agents[0])},
            {'heart': (2, -1, agents[1])},
            {'heart': (6, -1, agents[2])},
            {'heart': (11, -1, agents[3])},
            {'time_stone': (11, -1, agents[0])},
            {'time_stone': (11, 1, agents[3])},
        ]
    )
    for agent in agents:
        print(agent)