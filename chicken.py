import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)
ax.axhline(0, color="black", linewidth=1)

dot, = ax.plot([], [], 'ro', markersize=10)

# Initialize function
def init():
    dot.set_data([], [])
    return dot,

# Animation update function
def update(frame):
    x = frame
    y = 0
    dot.set_data([x], [y])  # must be lists, not scalars
    return dot,

# Create frames for dot moving back and forth
x_values = np.concatenate([np.linspace(0, 10, 100), np.linspace(10, 0, 100)])
ani = animation.FuncAnimation(fig, update, frames=x_values,
                              init_func=init, blit=True, interval=30, repeat=True)

plt.show()
