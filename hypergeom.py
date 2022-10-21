from scipy.stats import hypergeom

k = 1
M = 40
n = 3 + 3 + 3
N = 5
hpd = hypergeom(M, n, N)
prob = 1 -hypergeom.cdf(k-1, M, n, N)

print(prob)


