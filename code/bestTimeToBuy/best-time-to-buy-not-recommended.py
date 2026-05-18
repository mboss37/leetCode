from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0

        for i in range(len(prices)):
            buy_price = prices[i]
            for j in range(i + 1, len(prices)):
                sell_price = prices[j]
                profit = sell_price - buy_price
                if profit > max_profit:
                    max_profit = profit
        
        return max_profit
    
    def maxProfitAlternative(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(len(prices)):
            buy_price = prices[i]
            for j in range(i + 1, len(prices)):
                sell_price = prices[j]
                max_profit = max(max_profit, sell_price - buy_price)
                
        return max_profit


prices =[7,1,5,3,6,4]

solution = Solution()

result_one = solution.maxProfit(prices)
result_two = solution.maxProfitAlternative(prices)

print(result_one)
print(result_two)


