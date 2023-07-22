# -*- coding: utf-8 -*-

class trafficlightClass:
    # traffic light (or 'agent') class
    def __init__(self, ID, nPhase, plan_num, plan_duration, 
                 phase_set, phaseY_set, phaseR_set, lostTime,
                 phase_mapping, phase_time_in_duration, phase_duration):
        self.ID = ID # tl ID in SUMO
        self.N_p = nPhase # number of phases, unlike SUMO, g-y-r is treated as 1 phase
        self.plan_num = plan_num # number of current timing plan
        self.plan_duration = plan_duration # phase duration of current timing plan
        self.phase_set = phase_set # green states of all phases [phase]
        self.phaseY_set = phaseY_set # yellow states of all phases [phase]
        self.phaseR_set = phaseR_set # red states of all phases [phase]
        self.lostTime = lostTime # [0] = duration of yellow, [1] = duration of all-red
        self.phase_mapping = phase_mapping # map sumo phase index to AI phase index
        self.phase_time_in_duration = phase_time_in_duration # map sumo phase duration to AI phase duration
        self.phase_duration = phase_duration # map sumo phase duration to AI phase duration
        
        self.curPhase = 0 # index of current phase
        self.nextPhase = 0 # index of next phase
        self.remainDur = 0 # remaining duration of current phase (seconds, including yellow and red)
        self.elapsedDur = 0 # elapsed duration of current phase (seconds, including yellow and red)
        
        self.Plist = [] # list of states
    
    def rtnNextPhaseSwitchingTime(self):
        return None
    def rtn_Cur_Phase_State(self):
        return self.phase_set[self.curPhase]
    def rtn_Cur_PhaseY_State(self):
        return self.phaseY_set[self.curPhase]
    def rtn_Cur_PhaseR_State(self):
        return self.phaseR_set[self.curPhase]
    def rtn_Next_Phase_State(self):
        return self.phase_set[self.nextPhase]    
    
    def set_new_remainDur(self, dur):
        # set remainDur at the beginning of a green phase
        self.remainDur = dur
    
    def update_tlDur(self):
        self.remainDur = self.remainDur - 1
        self.elapsedDur = self.elapsedDur + 1
        
    def updateCurNextPhase(self):
        # update self.curPhase and self.nextPhase
        self.elapsedDur = 0
        self.curPhase = self.nextPhase
        if self.curPhase == self.N_p-1:
            self.nextPhase = 0
        else:
            self.nextPhase = self.curPhase + 1
        
        