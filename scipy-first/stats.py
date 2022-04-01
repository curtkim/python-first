from scipy.stats import norm, poisson
import matplotlib.pyplot as plt
import seaborn as sns

# rvs = random variable sample?
r = norm.rvs(loc=0, scale =3, size=100)
sns.distplot(r)
plt.show()


r = poisson.rvs(0.6, size=100)
sns.distplot(r)
plt.show()
