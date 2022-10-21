from scipy.stats import hypergeom

with open('Floowandereeze.ydk', 'r') as f:
  deck = f.read().splitlines()

k = 1
M = len(deck) - deck.count('49238328') - deck.count('98645731')
n = deck.count('18940725') + deck.count('28126717') + deck.count('69087397')
N = 5
hpd = hypergeom(M, n, N)
prob = 1 -hypergeom.cdf(k-1, M, n, N)
print(prob)


