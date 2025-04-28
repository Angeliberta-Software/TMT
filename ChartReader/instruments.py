class Ruler:
	def __init__(self):
		self.activated = False
		self.startPrice = 0
		self.endPrice = 0
		self.startBarIndex = 0
		self.endBarIndex = 0

	def activate(self, price, barIndex):
		self.startPrice = price
		self.startBarIndex = barIndex
		self.activated = True

	def calculate(self, price, barIndex):
		def decimal_places(x):
			s = str(x)
			if '.' in s:
				return len(s.split('.')[-1])
			else:
				return 0

		precision = max(decimal_places(self.startPrice), decimal_places(price))

		priceDifference = round(abs(self.startPrice - price), precision)
		barDifference = abs(self.startBarIndex - barIndex)
		self.activated = False
		return (priceDifference, barDifference)