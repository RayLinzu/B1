import os
import sys
import csv
import time
import pickle
import traci
import numpy as np
# import simClass_v0_4 as sim
import simClass_v0_4_v1 as sim1
import setup_const as c
import tensorflow as tf
from keras import backend as K
import FixedTimingPlan as TP
from ActorNetwork_v3 import ActorNetwork

scen = c.scen

file_path = os.getcwd() + "\\"
sim_file_path = file_path + c.sim_file_path
rou_file_path = file_path + c.rou_file_path

sys.path.append(file_path)
sys.path.append(sim_file_path)

episode_count = c.episode_count
nb_intersection = 3
# # ation輸出的維度，這邊有三個actor，各代表一個路口，輸出即為各路口對應的號控？
# action_dim = [1] * nb_intersection
# # actor輸入的維度，共三個actor，各109維，其中前55維是號誌資訊，54維是車道資訊
# actor_state_dim = [109, 109, 109]
VAR = 0
TAU = 0.00000001
LRA = 0.00000001

Fixtime = c.Fixtime
GUI = c.GUI

sim_sec = c.sim_sec  # including warm-up period

max_green = [[145, 15, 70], [145, 25, 70], [15, 105, 10, 45, 50, 45]]

min_green = [[70, 5, 30], [70, 15, 30], [5, 55, 5, 10, 20, 10]]

np.set_printoptions(threshold=1000)
np.set_printoptions(precision=10)
np.set_printoptions(suppress=True)

# Tensorflow GPU optimization
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

K.set_session(sess)

### Reading Training Model
# for x in range(nb_intersection):
#     locals()["actor_%s" % (x + 1)] = ActorNetwork(
#         sess, actor_state_dim[x], action_dim[x], TAU, LRA
#     )

### Loading Model Weight
# for x in range(nb_intersection):
#     try:
#         locals()["actor_%s" % (x + 1)].model.load_weights(
#             file_path + "actormodel_" + str(x + 1) + "-v3.h5"
#         )
#         print("actor_" + str(x + 1) + " weight load successfully")
#     except:
#         print("Cannot find the actor_" + str(x + 1) + " weight")
#         print(file_path + "actormodel_" + str(x + 1) + "-v3.h5")

test_perf = []
final_perf = []
action_output = []
# 紀錄號誌與車道資訊 ray test
state = []
throughput_output = []

e = 1

print("Simulation Experiment Start.")
print("episode:", str(e))
print("-------------------------------------")

### Training Start
while e <= episode_count:
        first = 0

        done = False
        dont_save = False
        test_perf = []
        action_output.append(["Episode:", e])
        # mySim = sim.simEnv(sim_file_path, scen)
        mySim = sim1.simEnv(sim_file_path, scen)

        mySim.genTestRouteFile(rou_file_path, e)

        env = mySim.reset_env()

        while done == False:
                cycle_state = False
                next_cycle_state = False
                if first == 0:
                        phase = mySim.step(env[18], env[19], env[20], env[21])
                        while cycle_state == False:
                                phase = mySim.step(env[18], env[19], env[20], env[21])
                                for x in range(nb_intersection):
                                        if phase[0][x] == 0 and mySim.curPhase[x] + 1 == mySim.N_p[x]:
                                                # print(f"Initial_phase[0][x]:{phase[0][x]}")
                                                # print(f"Initial_curPhase[x] + 1:{mySim.curPhase[x] + 1}")
                                                # print(f"Initial_N_p[x]:{mySim.N_p[x]}", '\n')
                                                # print(f"intersection_x2_cycle_state_initial:{phase[1]}")
                                                # print(f"intersection_x3_cycle_state_initial:{phase[2]}")
                                                # print(f"intersection_x4_cycle_state_initial:{phase[3]}", '\n')
                                                # action = cycle_step(mySim, phase)
                                                state, action, reward = mySim.cycle_step()
                                                print(f"initial_state:{state}")
                                                first = 1
                                                cycle_state = True
                else:
                        # next_phase = step(mySim, action[0], action[1], action[2], action[3])
                        next_phase = mySim.step(action[0], action[1], action[2], action[3])
                        while next_cycle_state == False:
                                # next_phase = step(mySim, action[0], action[1], action[2], action[3])
                                next_phase = mySim.step(action[0], action[1], action[2], action[3])
                                for x in range(nb_intersection):
                                        if next_phase[0][x] == 0 and mySim.curPhase[x] + 1 == mySim.N_p[x]:
                                                # print(f"next_phase[0][x]:{next_phase[0][x]}")
                                                # print(f"Next_curPhase[x] + 1:{mySim.curPhase[x] + 1}")
                                                # print(f"Next_N_p[x]:{mySim.N_p[x]}", '\n')
                                                # print(f"intersection_x2_cycle_state_Next:{next_phase[1]}")
                                                # print(f"intersection_x3_cycle_state_Next:{next_phase[2]}")
                                                # print(f"intersection_x4_cycle_state_Next:{next_phase[3]}", '\n')
                                                # next_action = cycle_step(mySim, next_phase)
                                                state, action, reward = mySim.cycle_step()
                                                print(f"next_state:{state}")
                                                print(f"reward:{reward}", '\n')
                                                next_cycle_state = True

                if mySim.t >= sim_sec:
                        done = True