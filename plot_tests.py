import numpy as np
import matplotlib.pyplot as plt

# Parameters
x = np.linspace(0, 4 * np.pi, 1000)
y1 = np.sin(x)
y2 = np.sin(2 * x)
y3 = np.sin(3 * x)

# Creating the figure and axis
fig, ax = plt.subplots(figsize=(10, 4), dpi=100)

# Plotting the waves with different colors and alpha for transparency
ax.plot(x, y1, color='orange', alpha=0.7, linewidth=2)
ax.plot(x, y2, color='red', alpha=0.5, linewidth=2)
ax.plot(x, y3, color='blue', alpha=0.3, linewidth=2)

# Fill between to create a "glow" effect
ax.fill_between(x, y1, y2, where=(y2 > y1), color='purple', alpha=0.1)
ax.fill_between(x, y2, y3, where=(y3 > y2), color='blue', alpha=0.1)

# Removing the axis for better visual effect
ax.axis('off')

# Saving the image
plt.savefig('soundwave.png', bbox_inches='tight', pad_inches=0, facecolor='black')
plt.close()