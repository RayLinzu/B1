# -*- coding: utf-8 -*-

import os
import time
import traci
import csv
import numpy as np
import net_cfg as net
import setup_const as c
import E1VDClass
import E2VDClass
import TrafficLightClass
import FixedTimingPlan as TP


class simEnv:
    def __init__(self, sim_path, scen):
        ''' 
        Initialize static variables related to links' and traffilights' attributes of SUMO network
        '''
        self.scen = scen
        self.pp = sim_path # sumo netowrk files dir
        self.tl_lane_dict = {} # key:tl ID, value:list of controlled lanes
        self.tlObj_list = [] # trafficlight objects
        self.tlObj_list_fixed = [] # trafficlight objects
        self.tlObj_dict = {} # key:tl ID, value: tlObj
        self.tlObj_dict_fixed = {} # key:tl ID, value: tlObj
        self.e1vdObj_list = [] # E1vd ID list
        self.e1vdObj_dict = {} # E1vd objects
        self.e2vdObj_list = [] # E2vd ID list
        self.e2vdObj_dict = {} # E2vd objects
        self.phase_set = [] # contains green phase states of all tl [agent][phase]
        self.phaseY_set = [] # contains yellow phase states of all tl [agent][phase]
        self.phaseR_set = [] # contains red phase states of all tl [agent][phase]
        self.lostTime = []  # contains yellow and red phase duration of all tl [agent][phase][0/1:yellow/red]
        self.N_tl = len(net.tlID_ai_list) # including all adaptive trafficlight
        self.N_tl_fixed = len(net.tlID_fixed_list) # including all pretime trafficlight
        self.N_AGENT = len(net.tlID_ai_list) # number of tls controlled by AI
        self.N_p = [] # number of phases
        self.N_p_fixed = [] # number of phases
        self.state = [] # cycle state
        self.reward = [] # cycle reward
        #Main road List
        self.e1vdlist1, self.e1vdlist2 = self.concatenate_lists_by_first_letters(net.alle1vd_lane_list)
        #Side road list
        self.e2vdlist1, self.e2vdlist2 = self.concatenate_lists_by_first_letters(net.alle2vd_lane_list)
       
        ## 讀取SUMO模擬檔案以建構路網和號誌變數
        self._get_SUMO_sim_settings() 
        
        self.initialVar_Episodic() # initialize all variables before starting simulation
    
    
    def _get_SUMO_sim_settings(self):
        print("reading simulation files from " + self.pp)
        traci.start(["sumo", "-c", self.pp,"--random",
                     "--time-to-teleport","-1","-W","false","-S","-Q"])
        
        e1vds = net.e1vds
        e2vds = net.e2vds
        tlID_All = net.tlID_list
        
        for vdID in e1vds:
            self.e1vdObj_dict[vdID] = E1VDClass.e1vd(vdID)
        self.e1vdObj_list = e1vds[:]
        
        # for vdID in e2vds:
        #     self.e2vdObj_dict[vdID] = E2VDClass.e2vd(vdID)
        # self.e2vdObj_list = e2vds[:]

        for vdID in e2vds:
            self.e2vdObj_dict[vdID] = E2VDClass.e2vd(vdID, tlID_All)
        self.e2vdObj_list = e2vds[:]
        
        tlID = net.tlID_ai_list
        tlID_fixed = net.tlID_fixed_list
        
        for tl in tlID:
            period = 0
            TP_data_list = self.load_TP(tl, self.scen, period)
            self.tlObj_dict[tl] = TrafficLightClass.trafficlightClass(\
                   ID=tl, nPhase=TP_data_list[0], plan_num=TP_data_list[1],
                   plan_duration=TP_data_list[2], phase_set=TP_data_list[3],
                   phaseY_set=TP_data_list[4], phaseR_set=TP_data_list[5],
                   lostTime=TP_data_list[6], phase_mapping=TP_data_list[7],
                   phase_time_in_duration=TP_data_list[8], phase_duration=TP_data_list[9])
            self.N_p.append(TP_data_list[0])
            
        for tl in tlID_fixed:
            period = 0
            TP_data_list = self.load_TP(tl, self.scen, period)
            self.tlObj_dict_fixed[tl] = TrafficLightClass.trafficlightClass(\
                   ID=tl, nPhase=TP_data_list[0], plan_num=TP_data_list[1],
                   plan_duration=TP_data_list[2], phase_set=TP_data_list[3],
                   phaseY_set=TP_data_list[4], phaseR_set=TP_data_list[5],
                   lostTime=TP_data_list[6], phase_mapping=TP_data_list[7],
                   phase_time_in_duration=TP_data_list[8],
                   phase_duration=TP_data_list[9])
            self.N_p_fixed.append(TP_data_list[0])
        
        # adjust tl_lane_dict to tenthousamds order
        self._follow_ai_input_lane_order()
        
        print("Done reading simulation files.")
        traci.close()
        
    def _follow_ai_input_lane_order(self):
        # 車道順序調整(參考Actor input state 順序)
        
        self.alle1vd_lane_list = net.alle1vd_lane_list
        
        self.alle2vd_lane_list = net.alle2vd_lane_list
        
        self.e2vd_lane_list = net.e2vd_lane_list
    
    def initialVar_Episodic(self):
        ## Initialize all state variables before starting a new episode of simulation
        self.t = 0 # current time step
        
        ## Plist[agent] stores the tl command excuted evey second
        self.Plist = [[] for _ in range(self.N_tl)] # Phase sequence waiting to be excuted
        
        self.curPhase = []
        for agent in range(self.N_AGENT):
            self.curPhase.append(self.N_p[agent]-1)
        self.remPhaseTime = [0]*self.N_AGENT # remaining phase time, yellow and red are included
        self.gElapsedTime = [0]*self.N_AGENT # elapsed phase time, y and g are included
        
        ## State features
        self.s_n_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.s_q_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        self.perf_q_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.perf_q_appr_ma_Odd = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.perf_q_appr_ma_Even = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        self.perf_f_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.perf_f_appr_ma_Odd = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.perf_f_appr_ma_Even = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        ## Performance Indices
        self.perf_sys_StopDelay = [] # total stop delay/veh numbers
        self.perf_sys_StopDelay_Odd = [] # total stop delay/veh numbers in side road
        self.perf_sys_StopDelay_Even = [] # total stop delay/veh numbers in main road

        self.perf_sys_Flow = [] #total passed vehicles 
        self.perf_sys_Flow_Odd = [] #total passed vehicles in side road
        self.perf_sys_Flow_Even = [] #total passed vehicles in main road

        
        self.perf_tl_StopDelay = [[0,0,0] for _ in range(15)] # total stop delay/veh numbers
        self.perf_tl_StopDelay_Odd = [[0,0,0] for _ in range(len(self.e1vdlist1))] # total stop delay/veh numbers in side road
        self.perf_tl_StopDelay_Even = [[0,0,0] for _ in range(len(self.e1vdlist2))] # total stop delay/veh numbers in main road
        
        self.perf_tl_Flow = [[0,0,0] for _ in range(15)] #total passed vehicles
        self.perf_tl_Flow_Odd = [[0,0,0] for _ in range(len(self.e2vdlist1))] #total passed vehicles in side road
        self.perf_tl_Flow_Even = [[0,0,0] for _ in range(len(self.e2vdlist2))] #total passed vehicles in main road
        
    def update_sim_states(self):
        self._update_lane_states_with_vClass()
        if True:self._collect_performance_indices() # collect system throughput and delay & timeInSys from intersections
    
    def _update_lane_states_with_vClass(self):
        '''
        update nVeh_v and nStoppedVeh_v (both by vClass) of all laneObjs
        update s_n_appr_ma[agent][] and s_q_appr_ma[agent][]        
        '''
        # update self.nVeh_v[vclass_ind] and lObj.nStoppedVeh_v[vclass_ind]
        for vdID in self.e1vdObj_list:
            vdObj = self.e1vdObj_dict[vdID]
            vdObj.update_nVeh_flow()

        # 這邊按照路段紀錄車輛通過數
        perf_f = []
        for vdsID_list in self.alle1vd_lane_list:
            temp_perf_f = [0,0,0]
            for idx, vdID in enumerate(vdsID_list):
                vdObj = self.e1vdObj_dict[vdID] # the lane index in laneObj_list
                i = idx%3
                temp_perf_f[i] += vdObj.lastStepVehNum
            perf_f.append(temp_perf_f)
        self.perf_f_appr_ma = perf_f[:]

        ## 分幹道
        perf_f_Odd = []
        for vdsID_list in self.e1vdlist1:
            temp_perf_f_Odd = [0,0,0]
            for idx, vdID in enumerate(vdsID_list):
                vdObj = self.e1vdObj_dict[vdID] # the lane index in laneObj_list
                i = idx%3
                temp_perf_f_Odd[i] += vdObj.lastStepVehNum
            perf_f_Odd.append(temp_perf_f_Odd)
        self.perf_f_appr_ma_Odd = perf_f_Odd[:] # 分幹道車輛通過數

        ## 主幹道
        perf_f_Even = []
        for vdsID_list in self.e1vdlist2:
            temp_perf_f_Even = [0,0,0]
            for idx, vdID in enumerate(vdsID_list):
                vdObj = self.e1vdObj_dict[vdID] # the lane index in laneObj_list
                i = idx%3
                temp_perf_f_Even[i] += vdObj.lastStepVehNum
            perf_f_Even.append(temp_perf_f_Even)
        self.perf_f_appr_ma_Even = perf_f_Even[:] #主幹道車輛通過數
        
        # update self.nVeh_v[vclass_ind] and lObj.nStoppedVeh_v[vclass_ind]
        for vdID in self.e2vdObj_list:
            vdObj = self.e2vdObj_dict[vdID]
            vdObj.update_nVeh_nStoppedVeh_v()
        
        # 這邊按照路段紀錄停等
        perf_q_v = []
        for vdsID_list in self.alle2vd_lane_list:
            temp_perf_q_v = []
            for vdID in vdsID_list:
                vdObj = self.e2vdObj_dict[vdID] # the lane index in laneObj_list
                temp_perf_q_v.append(vdObj.nStoppedVeh_v)
            perf_q_v.append([sum(x) for x in zip(*temp_perf_q_v)])
        self.perf_q_appr_ma = perf_q_v[:]

        ## 分幹道
        perf_q_v_Odd = []
        for vdsID_list in self.e2vdlist1:
            temp_perf_q_v_Odd = []
            for vdID in vdsID_list:
                vdObj = self.e2vdObj_dict[vdID] # the lane index in laneObj_list
                temp_perf_q_v_Odd.append(vdObj.nStoppedVeh_v)
            perf_q_v_Odd.append([sum(x) for x in zip(*temp_perf_q_v_Odd)])
        self.perf_q_appr_ma_Odd = perf_q_v_Odd[:]

        ## 主幹道
        perf_q_v_Even = []
        for vdsID_list in self.e2vdlist2:
            temp_perf_q_v_Even = []
            for vdID in vdsID_list:
                vdObj = self.e2vdObj_dict[vdID] # the lane index in laneObj_list
                temp_perf_q_v_Even.append(vdObj.nStoppedVeh_v)
            perf_q_v_Even.append([sum(x) for x in zip(*temp_perf_q_v_Even)])
        self.perf_q_appr_ma_Even = perf_q_v_Even[:]
        
        # 這邊紀錄總車輛數
        for x in range(self.N_AGENT):
            n_v = []
            q_v = []
            for vdsID_list in self.e2vd_lane_list:
                temp_n_v = []
                temp_q_v = []
                for vdID in vdsID_list:
                    vdObj = self.e2vdObj_dict[vdID] # the lane index in laneObj_list
                    temp_n_v.append(vdObj.nVeh_v)
                    temp_q_v.append(vdObj.nStoppedVeh_v)
                n_v.append([sum(x) for x in zip(*temp_n_v)])
                q_v.append([sum(x) for x in zip(*temp_q_v)])
            self.s_n_appr_ma[x] = n_v[:] #Total Vehicle in lane area
            self.s_q_appr_ma[x] = q_v[:] #Total stopped vehicle in lane area
    
    def concatenate_lists_by_first_letters(self, lst):
        list1 = []
        list2 = []
        for sub_list in lst:
            temp_list1 = []
            temp_list2 = []
            for item in sub_list:
                first_letter = item.split('_')[1][0]
                if first_letter == 'A' or first_letter == 'C':
                    temp_list1.append(item)
                elif first_letter == 'B' or first_letter == 'D':
                    temp_list2.append(item)
            if temp_list1:
                list1.append(temp_list1)
            if temp_list2:
                list2.append(temp_list2)
        return list1, list2

    def _collect_performance_indices(self):
        ## Intersection
        ### All veh_stopped regardless of road
        for i in range(len(self.perf_tl_StopDelay)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_q_appr_ma[i],self.perf_tl_StopDelay[i])))
            self.perf_tl_StopDelay[i] = combine_list[:]

        self.perf_sys_StopDelay = self.perf_tl_StopDelay
        
        ### All veh_stopped on 分幹道
        for i in range(len(self.perf_tl_StopDelay_Odd)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_q_appr_ma_Odd[i],self.perf_tl_StopDelay_Odd[i])))
            self.perf_tl_StopDelay_Odd[i] = combine_list[:] 
        
        self.perf_sys_StopDelay_Odd = self.perf_tl_StopDelay_Odd

        ### All veh_stopped on 主幹道
        for i in range(len(self.perf_tl_StopDelay_Even)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_q_appr_ma_Even[i],self.perf_tl_StopDelay_Even[i])))
            self.perf_tl_StopDelay_Even[i] = combine_list[:] 
        
        self.perf_sys_StopDelay_Even = self.perf_tl_StopDelay_Even

        ### All veh passed regardless of road
        for i in range(len(self.perf_tl_Flow)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_f_appr_ma[i],self.perf_tl_Flow[i])))
            self.perf_tl_Flow[i] = combine_list[:]

        self.perf_sys_Flow = self.perf_tl_Flow

        ### All veh passed on 分幹道
        for i in range(len(self.perf_tl_Flow_Odd)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_f_appr_ma_Odd[i],self.perf_tl_Flow_Odd[i])))
            self.perf_tl_Flow_Odd[i] = combine_list[:]

        self.perf_sys_Flow_Odd = self.perf_tl_Flow_Odd

        ### All veh passed on 主幹道
        for i in range(len(self.perf_tl_Flow_Even)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_f_appr_ma_Even[i],self.perf_tl_Flow_Even[i])))
            self.perf_tl_Flow_Even[i] = combine_list[:]

        self.perf_sys_Flow_Even = self.perf_tl_Flow_Even
        
    def genTestRouteFile(self, rou_file_path, epi):
        if (len(c.seed)>epi):
            seed_num = c.seed[epi-1]
        else:
            seed_num = 23423
        os.system('jtrrouter --route-files='+rou_file_path+'router_'+self.scen+'_b.flowdef.xml --turn-ratio-files='+rou_file_path+'router_'+self.scen+'_b.turndef.xml --net-file='+rou_file_path+'Taipei_'+self.scen+'.net.xml --output-file='+rou_file_path+'router_'+self.scen+'_b.rou.xml --seed '+str(seed_num)+' --begin 0 --end 10800')
        os.system('jtrrouter --route-files='+rou_file_path+'router_'+self.scen+'_c.flowdef.xml --turn-ratio-files='+rou_file_path+'router_'+self.scen+'_c.turndef.xml --net-file='+rou_file_path+'Taipei_'+self.scen+'.net.xml --output-file='+rou_file_path+'router_'+self.scen+'_c.rou.xml --seed '+str(seed_num)+' --begin 0 --end 10800')
        os.system('jtrrouter --route-files='+rou_file_path+'router_'+self.scen+'_m.flowdef.xml --turn-ratio-files='+rou_file_path+'router_'+self.scen+'_m.turndef.xml --net-file='+rou_file_path+'Taipei_'+self.scen+'.net.xml --output-file='+rou_file_path+'router_'+self.scen+'_m.rou.xml --seed '+str(seed_num)+' --begin 0 --end 10800')
        
    def startSim(self,GUI):
        # start up SUMO simulation
        check = 0
        while (check == 0):
            try:
                if GUI:
                    traci.start(["sumo-gui", "-c", self.pp, "--time-to-teleport","300","-W","-S","-Q"])
                    check = 1 
                else:
                    traci.start(["sumo", "-c", self.pp , "--time-to-teleport","300","-W","-S","-Q"])
                    check = 1
            except:
                print ('retry execute sumo path: '+self.pp)
                time.sleep(1)
                check = 0
    
    def startSimCmd(self,cmd):
        # start up SUMO simulation
        traci.start(cmd)
          
    def Warmup(self, step):
        for t in range(step):
            traci.simulationStep()
        self.t = step
        
    def load_TP(self, tl, scen, period):
        TPdata = TP.FixedTP[tl]
        plan_num = TPdata['TOD'][self.scen][period][0]
        plan_duration = TPdata['TOD'][scen][period][1]
        N_p = TPdata['PLAN'][plan_num]['Phase']
        phase_set = TPdata['PLAN'][plan_num]['Gstate']
        phaseY_set = TPdata['PLAN'][plan_num]['Ystate']
        phaseR_set = TPdata['PLAN'][plan_num]['Rstate']
        lostTime = []
        for i in range(N_p):
            lostTime.append([TPdata['PLAN'][plan_num]['Y'][i], TPdata['PLAN'][plan_num]['R'][i]])
        phase_mapping = TPdata['PLAN'][plan_num]['PhaseMap']
        phase_time_in_duration = TPdata['PLAN'][plan_num]['PhaseTimeInDuration']
        phase_duration = TPdata['PLAN'][plan_num]['PhaseDuration']
        
        TP_data_list = [N_p, plan_num, plan_duration, 
                        phase_set, phaseY_set, phaseR_set, lostTime, 
                        phase_mapping, phase_time_in_duration, phase_duration]
        
        return TP_data_list
    
    def reload_fixed_TP(self, period):
        tlID_fixed = net.tlID_fixed_list
        for tl in tlID_fixed:
            TP_data_list = self.load_TP(tl, self.scen, period)
            self.tlObj_dict_fixed[tl] = TrafficLightClass.trafficlightClass(\
                   ID=tl, nPhase=TP_data_list[0], plan_num=TP_data_list[1],
                   plan_duration=TP_data_list[2], phase_set=TP_data_list[3],
                   phaseY_set=TP_data_list[4], phaseR_set=TP_data_list[5],
                   lostTime=TP_data_list[6], phase_mapping=TP_data_list[7],
                   phase_time_in_duration=TP_data_list[8],
                   phase_duration=TP_data_list[9])
            self.N_p_fixed.append(TP_data_list[0])
    
    def get_traffic_light(self, tlID):
        Time = traci.simulation.getTime()
        Phase = traci.trafficlight.getPhase(tlID)
        PhaseDuration = traci.trafficlight.getPhaseDuration(tlID)
        NextSwitch = traci.trafficlight.getNextSwitch(tlID)
        RYGState = traci.trafficlight.getRedYellowGreenState(tlID)
        ProgID = traci.trafficlight.getProgram(tlID)
        
        return [Time, Phase, PhaseDuration, NextSwitch, RYGState, ProgID]
        
    def save_tl_result(self, tlID, result):
        with open(tlID+'_tl_result.csv' ,'w', newline='') as f2:
            w = csv.writer(f2)
            for ww in range(len(result)):
                w.writerow(result[ww])
    
    def get_fixed_tl_info(self, fixedtlID):
        [Time, sumoPhase, sumoPhaseDuration, NextSwitch, RYGState, ProgID] = self.get_traffic_light(fixedtlID)
        tlObj = self.tlObj_dict_fixed[fixedtlID]    
        phase_idx = tlObj.phase_mapping[sumoPhase]
        phase_num = phase_idx+1
        sumo_elapsed_time = sumoPhaseDuration-(NextSwitch-Time)
        time_in_pre_phase = sumoPhaseDuration-tlObj.phase_time_in_duration[sumoPhase]
        if (sumo_elapsed_time<time_in_pre_phase):
            AI_remain_time = time_in_pre_phase-sumo_elapsed_time
            phase_num = phase_num-1
            if (phase_num<1):
                phase_num = tlObj.N_p
            AI_elapsed_time = tlObj.plan_duration[phase_num-1]-AI_remain_time
        else:
            AI_remain_time = tlObj.phase_duration[sumoPhase]-sumo_elapsed_time+time_in_pre_phase
            if (AI_remain_time==0):
                if(phase_num<=tlObj.N_p-1):
                    phase_num = phase_num+1
                else:
                    phase_num = 1
                AI_remain_time = tlObj.plan_duration[phase_num-1]
            AI_elapsed_time = tlObj.plan_duration[phase_num-1]-AI_remain_time
        
        return [phase_num, AI_remain_time, AI_elapsed_time]
    
    def excutePlist(self):
        # pop the oldest phase in Plist and excute the phase in SUMO
        for i in range(self.N_AGENT):
            traci.trafficlight.setRedYellowGreenState(net.tlID_ai_list[i],self.Plist[i].pop(0))
        
    def countCurrentGreenTime(self):
        # update the green elapsed time and remaing duration of all trafficlights
        for i in range(self.N_AGENT):
            self.gElapsedTime[i] = self.gElapsedTime[i] + 1
            self.remPhaseTime[i] = self.remPhaseTime[i] -1
        
    def giveMAAction(self, action):
        '''
        update curPhase and Plist (__giveMAFixPhaseDuration())
        action: duration [agent]; =-1 if stay in current phase
        '''
        for i in range(self.N_AGENT):
            if action[i] != -1:
                if self.curPhase[i] == (self.N_p[i]-1):
                    self.curPhase[i] = 0
                else:
                    self.curPhase[i] = self.curPhase[i]+1
                self._giveMAFixPhaseDuration(i,action[i])   
    
    def _giveMAFixPhaseDuration(self, agent, duration):
        phase = self.curPhase[agent]  # phase of action, 0 ~ N_p[agent]-1  
        # Append next phase to Plist
        tlObj = self.tlObj_dict[net.tlID_ai_list[agent]]
        for i in range(duration): # green time
            self.Plist[agent].append(tlObj.phase_set[phase])
        # Append amber phase to Plist (every second)
        for i in range(tlObj.lostTime[phase][0]): # lost time yellow
            self.Plist[agent].append(tlObj.phaseY_set[phase])
        for i in range(tlObj.lostTime[phase][1]): # lost time red
            self.Plist[agent].append(tlObj.phaseR_set[phase])
        
        self.gElapsedTime[agent] = 0
        self.remPhaseTime[agent] = duration+tlObj.lostTime[phase][0]+tlObj.lostTime[phase][1]
        
    def output_ai_input_state(self):
        '''
        following AI actor's state format 
        '''
        veh_number = self.s_n_appr_ma[:] #Total Vehicle in lane area
        veh_num_stopped = self.s_q_appr_ma[:] #Total stopped vehicle in lane area
        phase_index_ai = self.curPhase[:]
        for agent in range(self.N_AGENT):
            if (self.remPhaseTime[agent] == 0):
                phase_index_ai[agent] = self.get_next_phase_ind(agent)
            phase_index_ai[agent] +=1  
        
        fixed_tl_phase_num = []
        fixed_tl_remain_time = []
        fixed_tl_elapsed_time = []
        fixed_plan_duration = []
        for idx,fixed_tl in enumerate(net.tlID_fixed_list):
            fixed_tl_info = self.get_fixed_tl_info(fixed_tl)
            fixed_tl_phase_num.append(fixed_tl_info[0])
            fixed_tl_remain_time.append(fixed_tl_info[1])
            fixed_tl_elapsed_time.append(fixed_tl_info[2])
            tlObj = self.tlObj_dict_fixed[fixed_tl]
            fixed_plan_duration += tlObj.plan_duration
            
        phase_num_fixed = fixed_tl_phase_num[:]
        
        rem_phase_time_ai = self.remPhaseTime[:]
        rem_phase_time_fixed = fixed_tl_remain_time[:]
        
        elapsed_time_ai = self.gElapsedTime[:]
        elapsed_time_fixed = fixed_tl_elapsed_time[:]
        
        
        output = []
        output.append(veh_number) #Input state of All vehicle in lane area
        output.append(veh_num_stopped) #Input state of all stopped vehicle in lane area
        output.append(self.perf_tl_StopDelay) #Reward of 停等車輛/停等延滯 of every lane
        output.append(self.perf_tl_StopDelay_Odd) #Reward of 停等車輛/停等延滯 of Side lane
        output.append(self.perf_tl_StopDelay_Even) #Reward of 停等車輛/停等延滯 of Main lane
        output.append(self.perf_tl_Flow) #Reward of 停等車輛數 of every lane
        output.append(self.perf_tl_Flow_Odd) #Reward of 停等車輛數 of Side lane
        output.append(self.perf_tl_Flow_Even) #Reward of 停等車輛數 of Main lane
        output.append(phase_index_ai)
        output.append(phase_num_fixed)
        output.append(rem_phase_time_ai)
        output.append(rem_phase_time_fixed)
        output.append(elapsed_time_ai) 
        output.append(elapsed_time_fixed)
        output.append(fixed_plan_duration)
        
        return output
        
    def print_sim_states(self, epi):
        '''
            print out whatevery you want for debugging perpose
        '''
        print("\n\n========================================\nepi %d, t = %d"%(epi,self.t))
        self._print_all_phase_info()
        self._print_nbr_tl_states(tl_ind = 4)
        self._print_lane_states(tl_ind = 4)
        self._print_perf_indices()
        print("\n=========================================\n")
        
    def get_next_phase_ind(self,agent):
        # return the next phase index of tl ind (ind is the index of tl of net.tlID_list)
        if self.curPhase[agent] == self.N_p[agent]-1:
            return 0
        else:
            return self.curPhase[agent]+1

    # for training
    def calculate_phase_green(self, percentage, cycle_time, yellow, red):
        green_time = percentage * cycle_time - yellow - red
        return green_time
    
    def calculate_first_phase_percantage_cycle(self, scen):
        x2_phase = TP.FixedTP["TL_02"]["TOD"][scen][0][1]
        x3_phase = TP.FixedTP["TL_03"]["TOD"][scen][0][1]
        x4_phase = TP.FixedTP["TL_04"]["TOD"][scen][0][1]
        x2_phase_percentage = [x / sum(x2_phase) for x in x2_phase]
        x3_phase_percentage = [x / sum(x3_phase) for x in x3_phase]
        x4_phase_percentage = [x / sum(x4_phase) for x in x4_phase]
        x2_cycle_time = sum(x2_phase)
        x3_cycle_time = sum(x3_phase)
        x4_cycle_time = sum(x4_phase)
        return x2_phase_percentage, x3_phase_percentage, x4_phase_percentage, x2_cycle_time, x3_cycle_time, x4_cycle_time

    def calculate_TOD_phase_percantage_and_cycle(self, scen, period):
        x1_phase = TP.FixedTP["TL_01"]["TOD"][scen][period][1]
        x5_phase = TP.FixedTP["TL_05"]["TOD"][scen][period][1]
        x6_phase = TP.FixedTP["TL_06"]["TOD"][scen][period][1]
        x7_phase = TP.FixedTP["TL_07"]["TOD"][scen][period][1]
        x1_phase_percentage = [x / sum(x1_phase) for x in x1_phase]
        x5_phase_percentage = [x / sum(x5_phase) for x in x5_phase]
        x6_phase_percentage = [x / sum(x6_phase) for x in x6_phase]
        x7_phase_percentage = [x / sum(x7_phase) for x in x7_phase]
        x1_cycle_time = sum(x1_phase)
        x5_cycle_time = sum(x5_phase)
        x6_cycle_time = sum(x6_phase)
        x7_cycle_time = sum(x7_phase)
        return x1_phase_percentage, x5_phase_percentage, x6_phase_percentage, x7_phase_percentage, x1_cycle_time, x5_cycle_time, x6_cycle_time, x7_cycle_time

    def save_red_yellow_to_list(self, progrom):
        yellow_list = []
        red_list = []
        x2_tod_yellow = TP.FixedTP["TL_02"]["PLAN"][progrom]["Y"]
        x3_tod_yellow = TP.FixedTP["TL_03"]["PLAN"][progrom]["Y"]
        x4_tod_yellow = TP.FixedTP["TL_04"]["PLAN"][progrom]["Y"]
        x2_tod_red = TP.FixedTP["TL_02"]["PLAN"][progrom]["R"]
        x3_tod_red = TP.FixedTP["TL_03"]["PLAN"][progrom]["R"]
        x4_tod_red = TP.FixedTP["TL_04"]["PLAN"][progrom]["R"]
        yellow_list.append([x2_tod_yellow, x3_tod_yellow, x4_tod_yellow])
        red_list.append([x2_tod_red, x3_tod_red, x4_tod_red])
        return yellow_list, red_list

    def phase_reset(self, veh_number, veh_stopped_number, perf_tl_StopDelay, perf_tl_Flow,
                    perf_tl_StopDelay_Odd, perf_tl_StopDelay_Even, perf_tl_Flow_Odd,
                    perf_tl_Flow_Even, phase_index, phase_num_fixed, rem_phase_time_ai, 
                    rem_phase_time_fixed, elapsed_time_ai, AI_phase_percentage, 
                    AI_cycle_time, yellow_list, red_list):
        '''
        Calculate and append each intersection every phase state 
        '''
        nb_intersection = 3

        # print(f"veh_stopped_number:{perf_tl_StopDelay}")
        # print(f"veh_stopped_number_Odd:{perf_tl_StopDelay_Odd}")
        # print(f"veh_stopped_number_Even:{perf_tl_StopDelay_Even}", '\n')
        # print(f"perf_tl_Flow:{perf_tl_Flow}")
        # print(f"perf_tl_Flow_Odd:{perf_tl_Flow_Odd}")
        # print(f"perf_tl_Flow_Even:{perf_tl_Flow_Even}", '\n')

        who_need_action = [1] * nb_intersection
        for x in range(nb_intersection):
            if rem_phase_time_ai[x] == 0:
                who_need_action[x] = 1
                elapsed_time_ai[x] = 0

        phase_index_onehot_list = []
        for x in range(nb_intersection):
            phase_index_onehot_list.append([0] * self.N_p[x])
            phase_index_onehot_list[x][phase_index[x] - 1] = 1
        phase_index_onehot_list = np.hstack(phase_index_onehot_list).tolist()
        
        fixed_phase_index_onehot_list = []
        for x in range(self.N_tl_fixed):
            fixed_phase_index_onehot_list.append([0] * self.N_p_fixed[x])
            fixed_phase_index_onehot_list[x][phase_num_fixed[x] - 1] = 1
        fixed_phase_index_onehot_list = np.hstack(
            fixed_phase_index_onehot_list
        ).tolist()

        decision_action_list = [-1] * nb_intersection

        intersection_x2_phase_state = []
        intersection_x3_phase_state = []
        intersection_x4_phase_state = []

        ### phase calculate state
        for x in range(nb_intersection):
            if who_need_action[x] == 1:
                p = phase_index[x] - 1
                
                temp_a = self.calculate_phase_green(AI_phase_percentage[0][x][p], AI_cycle_time[0], yellow_list[0][x][p], red_list[0][x][p])
                
                decision_action_list[x] = int(temp_a)          

                if x == 0:
                    intersection_x2_phase_state.append(veh_number[x])
                elif x == 1:
                    intersection_x3_phase_state.append(veh_number[x])
                elif x == 2:
                    intersection_x4_phase_state.append(veh_number[x])

        if sum(decision_action_list) <= -5:
            print("Major Error!!!")
            dont_save = True
            
        self.giveMAAction(decision_action_list)

        state = []
        state.append(intersection_x2_phase_state)
        state.append(intersection_x3_phase_state)
        state.append(intersection_x4_phase_state)

        reward = []
        reward.append(perf_tl_StopDelay_Odd)
        reward.append(perf_tl_StopDelay_Even)
        reward.append(perf_tl_Flow_Odd)
        reward.append(perf_tl_Flow_Even)

        self.state.append(state)
        self.reward.append(reward)
        
        return state
    
    def cycle_reset(self):
        '''
        calculate cycle state and reward from phase state
        '''
        simulation_time = traci.simulation.getTime()

        if 5400 > simulation_time >= 1800:
            x1_phase_percentage, x5_phase_percentage, x6_phase_percentage, x7_phase_percentage, x1_cycle_time, x5_cycle_time, x6_cycle_time, x7_cycle_time = self.calculate_TOD_phase_percantage_and_cycle(c.scen, period=1)                
        elif simulation_time >= 5400:
            x1_phase_percentage, x5_phase_percentage, x6_phase_percentage, x7_phase_percentage, x1_cycle_time, x5_cycle_time, x6_cycle_time, x7_cycle_time = self.calculate_TOD_phase_percantage_and_cycle(c.scen, period=2)
        
        ### Cycle End predict next action
        # AI predict here
        (x2_first_phase_percentage, 
        x3_first_phase_percentage, 
        x4_first_phase_percentage,
        x2_cycle_time, 
        x3_cycle_time, 
        x4_cycle_time) = self.calculate_first_phase_percantage_cycle(c.scen)

        AI_cycle_time = [200]
            
        AI_phase_percentage = []
        AI_phase_percentage.append([x2_first_phase_percentage, 
        x3_first_phase_percentage, 
        x4_first_phase_percentage])

        AI_state_cycle = []
        AI_state_cycle.append([x2_first_phase_percentage, 
                            x3_first_phase_percentage, 
                            x4_first_phase_percentage,
                            AI_phase_percentage])
        
        yellow_list, red_list = self.save_red_yellow_to_list(8)
        
        # TOD_state_cycle = [x1_phase_percentage, x5_phase_percentage, x6_phase_percentage, x7_phase_percentage, x1_cycle_time, x5_cycle_time, x6_cycle_time, x7_cycle_time]
        
        # universal_state_cycle = np.array[(AI_state_cycle+TOD_state_cycle)]
        
        # intersection_cycle_state = np.array[(intersection_x2_cycle_state + intersection_x3_cycle_state + 
        #                                     intersection_x4_cycle_state)]

        # AI_Input_State = np.array[(universal_state_cycle + intersection_cycle_state)]

        action = []
        action.append(AI_phase_percentage)
        action.append(AI_cycle_time)
        action.append(yellow_list)
        action.append(red_list)

        state = self.state
        self.state = []

        ## if need to calculate reward, i will do it in the following line
        reward = self.reward
        self.reward = []
        
        return state, action, reward
    
    def reset_env(self):
        '''
        reset environment when new episode starts  
        '''
        self.startSim(c.GUI)
        self.initialVar_Episodic()

        self.Warmup(1800)

        self.update_sim_states()

        output_data = self.output_ai_input_state()
        veh_number = output_data[0]
        veh_stopped_number = output_data[1]
        perf_tl_StopDelay = output_data[2]
        perf_tl_StopDelay_Odd = output_data[3]
        perf_tl_StopDelay_Even = output_data[4]
        perf_tl_Flow = output_data[5]
        perf_tl_Flow_Odd = output_data[6]
        perf_tl_Flow_Even = output_data[7]
        phase_index = output_data[8]
        phase_num_fixed = output_data[9]
        rem_phase_time_ai = output_data[10]
        rem_phase_time_fixed = output_data[11]
        elapsed_time_ai = output_data[12]
        elapsed_time_fixed = output_data[13]
        fixed_plan_duration = output_data[14]

        (x2_first_phase_percentage, 
        x3_first_phase_percentage, 
        x4_first_phase_percentage,
        x2_cycle_time, 
        x3_cycle_time, 
        x4_cycle_time) = self.calculate_first_phase_percantage_cycle(c.scen)

        AI_phase_percentage = [[x2_first_phase_percentage, 
                                x3_first_phase_percentage,
                                x4_first_phase_percentage]]
        
        AI_cycle_time = [x2_cycle_time]

        yellow_list, red_list = self.save_red_yellow_to_list(8)
        AI_state_cycle = []
        AI_state_cycle.append([x2_first_phase_percentage, 
                            x3_first_phase_percentage, 
                            x4_first_phase_percentage,
                            x2_cycle_time])
        
        return (veh_number, veh_stopped_number, perf_tl_StopDelay, perf_tl_StopDelay_Odd, perf_tl_StopDelay_Even,
                perf_tl_Flow, perf_tl_Flow_Odd, perf_tl_Flow_Even, phase_index, phase_num_fixed, 
                rem_phase_time_ai, rem_phase_time_fixed, elapsed_time_ai, elapsed_time_fixed, 
                fixed_plan_duration, x2_cycle_time, x3_cycle_time, x4_cycle_time, AI_phase_percentage, 
                AI_cycle_time, yellow_list, red_list, AI_state_cycle)
    
    def step(self, AI_phase_percentage, AI_cycle_time, yellow_list, red_list):
        '''
        simulation step and return new state & award from previous
        '''
        test_perf = []
        while (self.t < c.sim_sec) and (np.min(self.remPhaseTime) != 0):
            traci.simulationStep()
            self.t += 1
            self.update_sim_states()
            self.excutePlist()
            self.countCurrentGreenTime()

        ## New State and Reward from previous cycle
        output_data = self.output_ai_input_state()
        veh_number = output_data[0]
        veh_stopped_number = output_data[1]
        perf_tl_StopDelay = output_data[2]
        perf_tl_StopDelay_Odd = output_data[3]
        perf_tl_StopDelay_Even = output_data[4]
        perf_tl_Flow = output_data[5]
        perf_tl_Flow_Odd = output_data[6]
        perf_tl_Flow_Even = output_data[7]
        phase_index = output_data[8]
        phase_num_fixed = output_data[9]
        rem_phase_time_ai = output_data[10]
        rem_phase_time_fixed = output_data[11]
        elapsed_time_ai = output_data[12]
        elapsed_time_fixed = output_data[13]
        fixed_plan_duration = output_data[14]
        
        phase_state = self.phase_reset(veh_number, veh_stopped_number, perf_tl_StopDelay, perf_tl_Flow,
                                       perf_tl_StopDelay_Odd, perf_tl_StopDelay_Even, perf_tl_Flow_Odd,
                                       perf_tl_Flow_Even, phase_index, phase_num_fixed, rem_phase_time_ai, 
                                       rem_phase_time_fixed, elapsed_time_ai, AI_phase_percentage, 
                                       AI_cycle_time, yellow_list, red_list)

        return (rem_phase_time_ai, phase_state[0], phase_state[1], phase_state[2])
    
    def cycle_step(self):
    
        cycle_state, action, reward = self.cycle_reset()

        return cycle_state, action, reward