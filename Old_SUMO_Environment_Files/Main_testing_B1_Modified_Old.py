
import os
import sys
import csv
import numpy as np
import tensorflow as tf
from ActorNetwork_v3 import ActorNetwork
import pickle
import time
import traci
import simClass_v0_4
import setup_const as c

def show_trafficligt_state(curPhase, remPhaseTime):
    for i in range(len(curPhase)):
        print(f"trafficligt_phase:{curPhase[i]}")
        print(f"trafficligt_remain_time:{remPhaseTime[i]}")

scen = c.scen

file_path = os.getcwd()+'\\'
sim_file_path = file_path+c.sim_file_path
rou_file_path = file_path+c.rou_file_path

sys.path.append(file_path)
sys.path.append(sim_file_path)

episode_count = c.episode_count
nb_intersection = 3
action_dim = [1]*nb_intersection
actor_state_dim = [109, 109, 109]
VAR = 0
TAU = 0.00000001
LRA = 0.00000001

Fixtime = c.Fixtime
GUI = c.GUI

sim_sec = c.sim_sec           # including warm-up period

max_green = [   [145,15,70],
                [145,25,70],
                [15,105,10,45,50,45]
            ]

min_green = [   [70,5,30],
                [70,15,30],
                [5,55,5,10,20,10]
            ]

np.set_printoptions(threshold=1000)
np.set_printoptions(precision=10)
np.set_printoptions(suppress=True)

#Tensorflow GPU optimization
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
from keras import backend as K
K.set_session(sess)


for x in range(nb_intersection):
    locals()["actor_%s"%(x+1)] = ActorNetwork(sess, actor_state_dim[x], action_dim[x], TAU, LRA)
    
    
for x in range(nb_intersection):  
    try:
        locals()["actor_%s"%(x+1)].model.load_weights(file_path+"actormodel_"+str(x+1)+"-v3.h5")
        print("actormodel_"+str(x+1)+" weight load successfully")
    except:
        print("Cannot find the actormodel_"+str(x+1)+"-v3.h5"+" weight")
        print(file_path+"actormodel_"+str(x+1)+"-v3.h5")


test_perf = []
final_perf=[]
action_output = []
throughput_output = []


e = 1

print("Simulation Experiment Start.")
print("episode:",str(e))
print('-------------------------------------')

while e <= episode_count:
    test_perf = []
    action_output.append(['Episode:', e])
    mySim = simClass_v0_4.simEnv(sim_file_path, scen)
    
    mySim.genTestRouteFile(rou_file_path, e)

    mySim.startSim(GUI)
    mySim.initialVar_Episodic()
    
    mySim.Warmup(1800)
    
    mySim.update_sim_states()
    
    output_data = mySim.output_ai_input_state()
    veh_number                  = output_data[0]
    perf_tl_StopDelay           = output_data[1]
    perf_sys_StopDelay          = output_data[2]
    phase_index                 = output_data[3]
    phase_num_fixed             = output_data[4]
    rem_phase_time_ai           = output_data[5]
    rem_phase_time_fixed        = output_data[6]
    elapsed_time_ai             = output_data[7]
    elapsed_time_fixed          = output_data[8]
    fixed_plan_duration         = output_data[9]
    
    working_list = [1]*nb_intersection
    
    done = False
    total_stop_delay = 0
    total_global_stop_delay = 0
    who_need_action = [1]*nb_intersection
    
    duration = 0
    key_no = 1
    dont_save = False
    
    while done == False:
        if (Fixtime == True):
            while (mySim.t<sim_sec):
                traci.simulationStep()
                mySim.t += 1
                mySim.update_sim_states()
    #            os.system("pause")
                
                if (mySim.t%1800 == 0):
                    test_perf.append([mySim.t]+mySim.perf_tl_StopDelay+mySim.perf_tl_Flow)
                    period = int(mySim.t/1800) - 1
                    if (mySim.t<sim_sec):
                        mySim.reload_fixed_TP(period)
            done = True
        else:
            simulation_time = traci.simulation.getTime()
            # print(f"simulation time:{simulation_time}")
            
            if simulation_time % 200 == 0:
                show_trafficligt_state(mySim.curPhase, mySim.remPhaseTime)
                print(f"200 simulation time:{simulation_time}")

            phase_index_t1 = phase_index[:] # from 1~phase_num
            
            phase_index_onehot_list = []
            for x in range(nb_intersection):
                phase_index_onehot_list.append([0]*mySim.N_p[x])
                phase_index_onehot_list[x][phase_index[x]-1] = 1
            phase_index_onehot_list = np.hstack(phase_index_onehot_list).tolist()
            
            fixed_phase_index_onehot_list = []
            for x in range(mySim.N_tl_fixed):
                fixed_phase_index_onehot_list.append([0]*mySim.N_p_fixed[x])
                fixed_phase_index_onehot_list[x][phase_num_fixed[x]-1] = 1
            fixed_phase_index_onehot_list = np.hstack(fixed_phase_index_onehot_list).tolist()
            
            universal_state_t1 = np.array(
            phase_index_onehot_list[:]
            + fixed_phase_index_onehot_list[:]
            + rem_phase_time_ai[:]
            + rem_phase_time_fixed[:]
            + elapsed_time_ai[:]
            + elapsed_time_fixed[:]
            + [1, 1, 1]
            + fixed_plan_duration[:]
        )
                
            intersection_state_t1 = []
            for x in range(nb_intersection):
                intersection_state_t1.append(np.array(veh_number[x]).flatten())
            
            decision_action_list = [-1]*nb_intersection
            for x in range(nb_intersection):
                if who_need_action[x]==1:
                    
                    if Fixtime == True:
                        p = phase_index[x]-1
                    else:
                        input_state = np.append(universal_state_t1, intersection_state_t1[x]).reshape(1,actor_state_dim[x])
                        p = phase_index[x]-1
                        temp_a = locals()["actor_%s"%(x+1)].model.predict(input_state)[0]
                        temp_a = np.clip(round(temp_a[0],0),min_green[x][p],max_green[x][p])
                        decision_action_list[x]=int(temp_a)
                        
            if sum(decision_action_list) <= -5:
                print("Major Error!!!")
                dont_save = True
            
            mySim.giveMAAction(decision_action_list)
            
            if (Fixtime == False):
                action_output.append([mySim.t, phase_index, phase_num_fixed, decision_action_list, input_state.tolist()])
            
            ### Saving Intersection State for AI state of information
            # print(os.getcwd())
            # with open(file_path+'rl_Intersection_Data.pkl', 'wb') as file:
            #     pickle.dump(intersection_state_t1, file)
            # print(file_path+"rl_Intersection_Data.pkl Saved")

            # Saving 道路2,3,4的每一個面相
            for i in range(3):
                for j in range(2,5):
                # Check if the pickle file exists
                    if os.path.exists(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl'):
                        # Load existing pickle file
                        with open(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl', 'rb') as file:
                            existing_data = pickle.load(file)
                            # print(f"existing_data:{existing_data}")
                            new_data = np.append(existing_data, intersection_state_t1[i])
                            # print(f"new_data:{new_data}")
                        # Save modified data back to pickle file
                        with open(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl', 'wb') as file:
                            pickle.dump(new_data, file)
                        print(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl' 'Saved')
                    else: #Should Only Run Once
                        with open(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl', 'wb') as file:
                            pickle.dump(intersection_state_t1[i], file)
                        print(file_path+'rl_Intersection_x'+str(j)+'_Data.pkl' 'Created')

            while ( (mySim.t<sim_sec) and (np.min(mySim.remPhaseTime) != 0) ):
                traci.simulationStep()
                mySim.t += 1
                mySim.update_sim_states()
                mySim.excutePlist()
                mySim.countCurrentGreenTime()
    #            os.system("pause")
                
                if (mySim.t%1800 == 0):
                    test_perf.append([mySim.t]+mySim.perf_tl_StopDelay+mySim.perf_tl_Flow)
                    period = int(mySim.t/1800) - 1
                    if (mySim.t<sim_sec):
                        mySim.reload_fixed_TP(period)
            
            output_data = mySim.output_ai_input_state()
            veh_number                  = output_data[0]
            perf_tl_StopDelay           = output_data[1]
            perf_tl_Flow                = output_data[2]
            phase_index                 = output_data[3]
            phase_num_fixed             = output_data[4]
            rem_phase_time_ai           = output_data[5]
            rem_phase_time_fixed        = output_data[6]
            elapsed_time_ai             = output_data[7]
            elapsed_time_fixed          = output_data[8]
            fixed_plan_duration         = output_data[9]
            
            who_need_action = [0]*nb_intersection
            for x in range(nb_intersection):
                if rem_phase_time_ai[x]==0:
                    who_need_action[x]=1
                    elapsed_time_ai[x]=0
                    
            if (mySim.t>=sim_sec):
                done = True
            #=====================================================  
    
    
    interval_avg_delay=[]
    for interval in range(int((c.sim_sec-1800)/1800)):
        app_avg_delay=[]
        for i in range(len(mySim.perf_tl_StopDelay)):
            if (interval==0):
                total_delay = test_perf[interval][i+1][0]+test_perf[interval][i+1][1]
                total_flow = test_perf[interval][i+10][0]+test_perf[interval][i+10][1]
                avg_delay = total_delay/total_flow
            else:
                total_delay = (test_perf[interval][i+1][0]+test_perf[interval][i+1][1])-(test_perf[interval-1][i+1][0]+test_perf[interval-1][i+1][1])
                total_flow = (test_perf[interval][i+10][0]+test_perf[interval][i+10][1])-(test_perf[interval-1][i+10][0]+test_perf[interval-1][i+10][1])
                avg_delay = total_delay/total_flow
            app_avg_delay.append(avg_delay)
        interval_avg_delay.append(app_avg_delay)
    app_period_avg_delay=[sum(x)/4 for x in zip(*interval_avg_delay)]
    intersection_avg_delay=sum(app_period_avg_delay)/9
    intersection_total_flow=[sum(x) for x in zip(*mySim.perf_tl_Flow)]
    PCU = intersection_total_flow[0]*2.5+intersection_total_flow[1]+intersection_total_flow[2]*0.3
    final_perf.append(['Episode:', e])
    final_perf.append(['Average_stop_delay:', intersection_avg_delay])
    final_perf.append(['Throughput:', PCU])
    final_perf.append([])
    action_output.append([])
    
    tex_1 = 'End of episode:' + str(e) + ' '*(4-len(str(e)))
    print(tex_1)    
    print('loading new actors...')
    traci.close(0)

    e += 1
    print('-----------------[sleep 5 s]--------------------')
    time.sleep(5)
    print('-----------------[next round start]--------------------')





if (Fixtime == True):
    perf_life_name = 'Performance_'+scen+'_FixedTime.csv'
else:
    perf_life_name = 'Performance_'+scen+'_AI.csv'

with open(file_path+perf_life_name,'w',newline='') as f2:
    w = csv.writer(f2)
    # for ww in range(len(test_perf)):
    #     w.writerow(test_perf[ww])
    for ww in range(len(final_perf)):
        w.writerow(final_perf[ww])

if (Fixtime == False):
    action_output_name = 'Action_'+scen+'_AI.csv'
    
    with open(file_path+action_output_name,'w',newline='') as f2:
        w = csv.writer(f2)
        for ww in range(len(action_output)):
            w.writerow(action_output[ww])






