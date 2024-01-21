import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap as lcm
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.signal import convolve2d

proportion_true = 0.25

matrix = np.random.choice([True, False], size=(50, 50), p=[proportion_true, 1-proportion_true])

custom_colors = lcm(['#222222', '#00FF00'], name="retro")

fig, ax = plt.subplots()

im = ax.imshow(matrix, cmap=custom_colors)
# ax.axis('off')
# ax.set_position([0, 0, 1, 1])

kernel = np.ones((3, 3))

def update(frame):
    global matrix
    count_matrix = convolve2d(matrix, kernel, mode='same', boundary='wrap') - matrix
    new_matrix = np.where((matrix & ((count_matrix == 2) | (count_matrix == 3))) | (~matrix & (count_matrix == 3)), True, False)
    matrix = new_matrix
    im.set_array(matrix)

ani = FuncAnimation(fig, update, frames=450)

param_video = FFMpegWriter(fps=5, codec='libx264', extra_args=['-profile:v', 'high', '-pix_fmt', 'yuv420p', '-b:v', '5000k'])

ani.save('animation.mp4', writer=param_video)
