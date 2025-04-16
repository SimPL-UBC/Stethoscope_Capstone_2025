import matplotlib.pyplot as plt
import matplotlib.animation as animation

FILE_PATH = "temp.txt"

def read_values():
    with open(FILE_PATH, "r") as f:
        lines = f.read().strip().split()
        values = [float(x) for x in lines if x]
    return values

fig, ax = plt.subplots()
line, = ax.plot([0]*1000)

def update(frame):
    try:
        y = read_values()
        if len(y) == 1000:
            line.set_ydata(y)
            # ax.set_ylim(min(y) - 1, max(y) + 1)
    except Exception as e:
        print("Error reading file:", e)
    return line,

# Set x-limits since x doesn't change
ax.set_xlim(0, 1000)
ax.set_xticks([])
ax.set_yticks([])

# Initialize y-limits
ax.set_ylim(-10000, 70000)

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
