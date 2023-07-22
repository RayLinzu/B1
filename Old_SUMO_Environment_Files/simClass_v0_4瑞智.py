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
        ''' Initialize static variables related to links' and traffilights' attributes of SUMO network
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
       
        ## 讀取SUMO模擬檔案以建構路網和號誌變數
        self._get_SUMO_sim_settings() 
        
        self.initialVar_Episodic() # initialize all variables before starting simulation
    
    
    def _get_SUMO_sim_settings(self):
        print("reading simulation files from " + self.pp)
        traci.start(["sumo", "-c", self.pp,"--random",
                     "--time-to-teleport","-1","-W","false","-S","-Q"])
        
        e1vds = net.e1vds
        e2vds = net.e2vds
        
        for vdID in e1vds:
            self.e1vdObj_dict[vdID] = E1VDClass.e1vd(vdID)
        self.e1vdObj_list = e1vds[:]
        
        for vdID in e2vds:
            self.e2vdObj_dict[vdID] = E2VDClass.e2vd(vdID)
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
#            print(self.N_p[agent])
            self.curPhase.append(self.N_p[agent]-1)
        self.remPhaseTime = [0]*self.N_AGENT # remaining phase time, yellow and red are included
        self.gElapsedTime = [0]*self.N_AGENT # elapsed phase time, y and g are included
        
        ## State features
        self.s_n_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        self.s_q_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        self.perf_q_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        self.perf_f_appr_ma = [[] for _ in range(self.N_tl)] # [agent][lane][vType]
        
        ## Performance Indices
        self.perf_sys_StopDelay = 0 # total stop delay
        
        self.perf_tl_StopDelay = [[0,0,0] for _ in range(9)]
        self.perf_tl_Flow = [[0,0,0] for _ in range(9)]
        
        
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
        
        perf_f = []
        for vdsID_list in self.alle1vd_lane_list:
            temp_perf_f = [0,0,0]
            for idx, vdID in enumerate(vdsID_list):
                vdObj = self.e1vdObj_dict[vdID] # the lane index in laneObj_list
                i = idx%3
                temp_perf_f[i] += vdObj.lastStepVehNum
            perf_f.append(temp_perf_f)
        self.perf_f_appr_ma = perf_f[:]
        # print(self.perf_f_appr_ma)
        
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
        # print(self.perf_q_appr_ma)
        
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
            self.s_n_appr_ma[x] = n_v[:]
            self.s_q_appr_ma[x] = q_v[:]
        # print(self.s_n_appr_ma)
    
    
    def _collect_performance_indices(self):
        ## Intersection
        for i in range(len(self.perf_tl_StopDelay)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_q_appr_ma[i],self.perf_tl_StopDelay[i])))
            self.perf_tl_StopDelay[i] = combine_list[:]
        
        self.perf_sys_StopDelay = self.perf_tl_StopDelay[0]+self.perf_tl_StopDelay[1]
        
        for i in range(len(self.perf_tl_Flow)):
            combine_list = list(map(lambda x :x[0]+x[1] ,
                                    zip(self.perf_f_appr_ma[i],self.perf_tl_Flow[i])))
            self.perf_tl_Flow[i] = combine_list[:]
        
    
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
        plan_num = TPdata['TOD'][scen][period][0]
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
        # print(f"intersection:{fixedtlID}")
        # print(f"phase in sumo:{sumoPhase}")
        # print(f"PhaseDuration:{sumoPhaseDuration}")
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
            # if net.tlID_ai_list[i] == "TL_02":
                # print(f"{net.tlID_ai_list[i]}:{self.Plist[i]}")
        
        
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
                # ray try
                # if self.Plist[i][0] == "rrrrrrrGGGgrrr":
                #     print(f"intersaction label:{i}")
                #     print(f"phase1")
                # elif self.Plist[i][0] == "GGGgrrrGGGgrrr":
                #     print(f"intersaction label:{i}")
                #     print(f"phase2")
                # elif self.Plist[i][0] == "rrrrrrrGGGgrrr":
                #     print(f"intersaction label:{i}")
                #     print(f"phase3")
                # elif self.Plist[i][0] == "rrrrrrrrrrrGGg":
                #     print(f"intersaction label:{i}")
                #     print(f"phase4")
                # elif self.Plist[i][0] == "rrrrGGgrrrrGGg":
                #     print(f"intersaction label:{i}")
                #     print(f"phase5")
                # RYGState = traci.trafficlight.getRedYellowGreenState(net.tlID_ai_list[i])
                # print(f"TL number:{net.tlID_ai_list[i]}RYGStat")
                # print(f"RYGState:{RYGState}")

    
    
    def _giveMAFixPhaseDuration(self, agent, duration):
        phase = self.curPhase[agent]  # phase of action, 0 ~ N_p[agent]-1
        # print(f"self.curPhase[agent]:{phase}")
        # print(f"agent:{agent}")    
        # Append next phase to Plist
        tlObj = self.tlObj_dict[net.tlID_ai_list[agent]]
        for i in range(duration): # green time
            self.Plist[agent].append(tlObj.phase_set[phase])
            # if net.tlID_ai_list[agent] == "TL_02":
            #     print(f'{net.tlID_ai_list[agent]} phase_set: {tlObj.phase_set[phase]}')
        # Append amber phase to Plist (every second)
        for i in range(tlObj.lostTime[phase][0]): # lost time yellow
            self.Plist[agent].append(tlObj.phaseY_set[phase])
            # if net.tlID_ai_list[agent] == "TL_02":
            #     print(f'{net.tlID_ai_list[agent]} phaseY_set: {tlObj.phaseY_set[phase]}')
        for i in range(tlObj.lostTime[phase][1]): # lost time red
            self.Plist[agent].append(tlObj.phaseR_set[phase])
            # if net.tlID_ai_list[agent] == "TL_02":
            #     print(f'{net.tlID_ai_list[agent]} phaseR_set: {tlObj.phaseR_set[phase]}')
        
        self.gElapsedTime[agent] = 0
        self.remPhaseTime[agent] = duration+tlObj.lostTime[phase][0]+tlObj.lostTime[phase][1]
        
        # if(agent==0 and phase==1):
        #     for i in range(8): 
        #         self.Plist[agent].append("rrrrrrrrrrrrrr")
        #     for i in range(5): 
        #         self.Plist[agent].append("rrrrGGGrrrrrrr")
        #     for i in range(3): 
        #         self.Plist[agent].append("rrrryyyrrrrrrr")
        #     for i in range(2):
        #         self.Plist[agent].append("rrrrrrrrrrrrrr")
        #     self.remPhaseTime[agent] = self.remPhaseTime[agent] + 18
        
        
    def output_ai_input_state(self):
        '''
        following AI actor's state format 
        '''
        veh_number = self.s_n_appr_ma[:]
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
        output.append(veh_number)
        output.append(self.perf_tl_StopDelay)
        output.append(self.perf_tl_Flow)
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
    



    # for trainning
    def store_phase_intersaction_state(intersection_state_t1):
        return
    
    def reset():
        return
    
    def step():
        return
    
