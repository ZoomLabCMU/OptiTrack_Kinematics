from OptiTrackStreaming.DataStreamer import OptiTrackDataStreamer
import time 
op = OptiTrackDataStreamer()
for i in range(30):
    t = time.time()
    pos,rot,op_time = op.get_closest_datapoint(t)

    print(pos,abs(t-op_time))
    time.sleep(.1)
op.close()