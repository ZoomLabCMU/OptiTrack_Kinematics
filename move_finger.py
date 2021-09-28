from DeltaArray import DeltaArray
from OptiTrackStreaming.DataStreamer import OptiTrackDataStreamer
import numpy as np
from time import sleep
import time

# da = DeltaArray('/dev/ttyACM0') -- CHANGE PORT
da = DeltaArray('COM3')

# for this to work enter the "Data Streaming Pane" in Motive:
#   "Broadcast Frame Data" is turned on
#   Command Port = 1510
#   Data Port = 1511
#   Multicast Interface = 239.255.42.99

# https://v22.wiki.optitrack.com/index.php?title=Data_Streaming
op = OptiTrackDataStreamer()

# PRESET POSITIONS
p = np.ones((8, 12)) * 0.0012
p[0, 3:6] = np.array([0.01, 0.01, 0.01])
p[1, 3:6] = np.array([0.02, 0.02, 0.02])
p[2, 3:6] = np.array([0.03, 0.03, 0.03])
p[3, 3:6] = np.array([0.04, 0.04, 0.04])

p[4, 3:6] = np.array([0.05, 0.05, 0.05])
p[5, 3:6] = np.array([0.06, 0.06, 0.06])
p[6, 3:6] = np.array([0.07, 0.07, 0.07])
p[7, 3:6] = np.array([0.08, 0.08, 0.08])

p[:,3] += .0015
p[:,5] += .0005


def print_posn():
    #da.wait_until_done_moving()
    posn = da.get_joint_positions()
    print(posn[3:6])  # Motors 4-6


def retract():
    da.reset()
    time.sleep(2)

retract()

pos_0,rot_0,t = op.get_closest_datapoint(time.time())

# print_posn()
for i in range(0, 8): # LOOP THROUGH ALL PRESET POSITIONS
    duration = [1.0]
    da.move_joint_position(p[i, :].reshape(1,12), duration)
    #da.wait_until_done_moving()
    sleep(2)
    pos,rot,t = op.get_closest_datapoint(time.time())
    print("relative_position = ",pos-pos_0)
    print_posn()
    input()


# RESET TO FULLY RETRACTED ACTUATORS
retract()

da.close()
op.close()