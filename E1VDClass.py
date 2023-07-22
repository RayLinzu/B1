# -*- coding: utf-8 -*-

import net_cfg as net
import traci

class e1vd:
    # lane class
    def __init__(self, vdid):
        self.ID = vdid # lane ID
        self.vdLane = traci.inductionloop.getLaneID(vdid)
        if (vdid[-1] == 'C'):
            self.vClass = 'car'
        elif (vdid[-1] == 'B'):
            self.vClass = 'truck'
        elif (vdid[-1] == 'M'):
            self.vClass = 'motor'
        else:
            self.vClass = 'NA' 
        self.vehIDs = [] # Current veh IDs on the lane (from traci)
        self.lastStepVehID = ['-']
        self.lastStepVehNum = 0
        self.vdTotVehNum = 0
        
        
    def update_nVeh_flow(self):
        vehID = traci.inductionloop.getLastStepVehicleIDs(self.ID)
        nowVeh = set(vehID)
        lastVeh = set(self.lastStepVehID)
        self.lastStepVehNum = len(lastVeh.difference(nowVeh))
        self.vdTotVehNum += len(lastVeh.difference(nowVeh))
        self.lastStepVehID = vehID
        
        
#        for idx in range(self.vdNum):
#            vdID = self.vdListID[idx]
##            lastVehID = self.lastStepVehID[idx]
#            vehID = traci.inductionloop.getLastStepVehicleIDs(vdID)
##            vehNum = traci.inductionloop.getLastStepVehicleNumber(vdID)
#            
#            nowVeh = set(vehID)
#            lastVeh = set(self.lastStepVehID[idx])
##            self.N_arr = len(nowVeh.difference(lastVeh))
#            self.vdVehTotNum[idx] += len(lastVeh.difference(nowVeh))
#            self.lastStepVehID[idx] = vehID
            
#            if (vehNum == 1):
#                if (lastVehID != vehID):
#                    self.vdVehTotNum[idx] += 1
#                    self.lastStepVehID[idx] = vehID
#            elif (vehNum == 0):
##                self.vdVehTotNum[idx] = 0
#                self.lastStepVehID[idx] = '-'
#            else:
#                self.vdVehTotNum[idx] += 1
#                self.lastStepVehID[idx] = vehID
#                print('========================')
#                print('========================')
#                print('more than 1 veh passed VD ', vdID)
#                print('========================')
#                print('========================')
    
    