import numpy as np
import matplotlib.pyplot as plt

def show_results(df, waypoints = None, FPS = 20):
    frame = np.arange(len(df)) / FPS

    fig, ax = plt.subplots(5) # , figsize=(3, 1.5*5)
    fig.suptitle('npc planner speed waypoints', fontsize=14)
    #fig.tight_layout()
    #fig.subplots_adjust(top=2.85)

    ax[0].title.set_text("xy")
    ax[0].invert_yaxis()
    ax[0].plot(df['position_x'], df['position_y'])

    if waypoints != None:
        pts = np.array(waypoints)
        ax[0].plot(pts[:,0], pts[:,1])

    for i in range(0, len(df), FPS):
        ax[0].annotate(int(i/FPS), (df['position_x'][i], df['position_y'][i]))

    ax[1].title.set_text("speed")
    ax[1].plot(frame, df['speed'])

    ax[2].title.set_text("steer")
    ax[2].plot(frame, df['steer'])

    ax[3].title.set_text("throttle")
    ax[3].plot(frame, df['throttle'])

    ax[4].title.set_text("brake")
    ax[4].plot(frame, df['brake'])

    plt.show()
