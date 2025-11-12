import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(1, 12, 100)

log_x_times_10 = []
for num in x:
    log_x_times_10.append(10*math.log2(num))

fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
ax.plot(x, np.ones(100), label=r'$O(1)$')
ax.plot(x, log_x_times_10, label=r'$O(log(n))$')
ax.plot(x, 10*x, label=r'$O(n)$')
ax.plot(x, x*log_x_times_10, label=r'$O(nlog(n))$')
ax.plot(x, 5*x**2, label=r'$O(n^2)$')
ax.plot(x, x**3, label=r'$O(n^3)$')
ax.plot(x, 2**x, label=r'$O(2^n)$')
plt.xticks([])
plt.yticks([])
ax.set_xlabel('n')
ax.set_ylabel('Runtime')
ax.set_title("Common Time Complexities")
ax.legend()
fig.savefig('graph_common_time_complexities')
