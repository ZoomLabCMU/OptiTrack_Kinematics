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

def sample_domain(max_height, max_actuator_dif,spacing=.005):
    pts = []
    for x in np.arange(.005,max_height,spacing):
        for y in np.arange(.005,max_height,spacing):
            for z in np.arange(.005,max_height,spacing):
                if np.amax([x,y,z])-np.amin([x,y,z]) > max_actuator_dif:
                    continue
                else:
                    pts.append([x,y,z])
    return np.array(pts)

def save_training_data(data, filename="training_data"):
    np.save(filename,data)

sample = sample_domain(.0451,.03,.005)

# PRESET POSITIONS
p = np.ones((sample.shape[0], 12)) * 0.0012
p[:,3:6] = sample


def print_posn():
    #da.wait_until_done_moving()
    posn = da.get_joint_positions()
    print(posn[3:6])  # Motors 4-6


def retract():
    da.reset()
    time.sleep(2)

retract()

pos_0,rot_0,t = op.get_closest_datapoint(time.time())
print(pos_0)

Data = []
# print_posn()
for i in range(0, p.shape[0]): # LOOP THROUGH ALL PRESET POSITIONS
    duration = [1.0]
    da.move_joint_position(p[i, :].reshape(1,12), duration)
    print(100*i/p.shape[0],"%","i","=",i)
    sleep(1.5)
    pos,rot,t = op.get_closest_datapoint(time.time())
    act_pos = da.get_joint_positions()[3:6]
    print("End Effector Position = ",pos-pos_0)
    print("Actuator Position",act_pos)
    Data.append((act_pos,pos-pos_0))
    save_training_data(np.array(Data),"training_data4")

save_training_data(np.array(Data),"training_data4")

# RESET TO FULLY RETRACTED ACTUATORS
retract()

da.close()
op.close()