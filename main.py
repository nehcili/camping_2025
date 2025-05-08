    
from agents import Agent, Bank, Portfolio


class Feds(Bank):
    def get_bids(self, agents: list[Agent], game) -> dict[str, float]:
        # others sell at bids
        return {
            'heart': 5,
            'time_stone': 10
        }

    def get_asks(self, agents: list[Agent], game) -> dict[str, float]:
        # others buy at asks
        return {
            'heart': 7,
            'time_stone': 12
        }
    
class RiskAverse(Agent):
    def on_game_start(self, agents, game, bank_bids=None, bank_asks=None):
        self._bid = bank_bids
        self._ask = bank_asks

        # when there is a global event that reduces heart
        if isinstance(game.rewards == Portfolio):
            # need at least 1 heart to play
            heart_to_buy = - (self.portfolio.heart + game.rewards.heart) + 1

            if heart_to_buy > 0:
                gold_needed_to_buy_heart = heart_to_buy * bank_asks['heart']

                # if I have enough gold to buy the heart
                if self.portfolio.gold >= gold_needed_to_buy_heart:
                    self.portfolio.gold -= gold_needed_to_buy_heart
                    self.portfolio.heart += heart_to_buy
                else:
                    self.portfolio.heart += self.portfolio.gold * bank_asks['heart']
                    gold_needed_to_buy_heart -= self.portfolio.gold * bank_asks['heart']
                    self.portfolio.gold = 0

                else:
                    # sell enough time_stone to buy the heart
                    time_stone_needed_to_sell = (gold_needed_to_buy_heart - self.portfolio.gold) / bank_bids['time_stone']
                    if time_stone_needed_to_sell < self.portfolio.time_stone:
                        self.portfolio.time_stone -= time_stone_needed_to_sell
                        self.portfolio.gold = 0
                        self.portfolio.heart += heart_to_buy
        

        
        def get_trades(self, agents, game):
            # if I don't have enough heart, I will buy it

        



            



class SellHeartAgent(Agent):
    def get_trades(self, agents, game):
        # Implement logic to get trades
        return {'heart': (2, -1, self)}
    
    
    
if __name__ == "__main__":
    bank = 