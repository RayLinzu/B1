# -*- coding: utf-8 -*-

import net_cfg as net
import traci

class e2vd:
    # e2vd class
    def __init__(self, vdID, TCid):
        self.ID = vdID # vd ID
        self.nVeh = 0 # number of vehicles
        self.nStoppedVeh = 0 # number of stopped vehicles
        self.belongTC = TCid # traffic light ID
        self.nVeh_v = [0]*3 # number of vehicles by vClass [scooter, passenger, truck]
        self.nStoppedVeh_v = [0]*3 # number of stopped vehicles by vClass [scooter, passenger, truck]
        self.vehIDs = [] # Current veh IDs on the lane (from traci)
        
           
    def get_nVeh(self): 
        ''' get the current number of vehicles on the lane, retrun nVeh '''
        return self.nVeh
    
    def get_nStoppedVeh(self):
        ''' get the current number of stopped vehicles on the lane, retrun nVeh '''
        return self.nStoppedVeh
    
    # def update_nVeh_nStoppedVeh_v(self):
    #     ''' get veh IDs on the lane to count the nVeh by vClass  '''
        
    #     self.nVeh_v = [0]*3 # number of vehicles by vClass [scooter, passenger, truck]
    #     self.nStoppedVeh_v = [0]*3 # number of stopped vehicles by vClass [scooter, passenger, truck]
    #     self.vehIDs = traci.lanearea.getLastStepVehicleIDs(self.ID)
    #     for vehID in self.vehIDs:
    #         isStopped = False
    #         my_vClass = traci.vehicle.getVehicleClass(vehID)
    #         # print("vehID: %s, vehClass: %s "%(vehID, vClass))
    #         if traci.vehicle.getSpeed(vehID) < 0.1: # stopped vehicle
    #             isStopped = True
            
    #         # count nVeh_v and nStoppedVeh_v
    #         for vclass_ind,vclass in enumerate(net.vClass):
    #             if vclass == my_vClass:
    #                 self.nVeh_v[vclass_ind]=self.nVeh_v[vclass_ind]+1
    #                 if isStopped:
    #                     self.nStoppedVeh_v[vclass_ind]=self.nStoppedVeh_v[vclass_ind]+1
    #                 break
    
    def update_nVeh_nStoppedVeh_v(self):
        ''' get veh IDs on the lane to count the nVeh by vClass  '''
        
        self.nVeh_v = [0]*3 # number of vehicles by vClass ['truck','passenger','moped']
        self.nStoppedVeh_v = [0]*3 # number of stopped vehicles by vClass ['truck','passenger','moped']

        # scan through all vehicles on the lane and lanes in .needADJ_ID
        self.vehIDs = traci.lanearea.getLastStepVehicleIDs(self.ID)
        for vehID in self.vehIDs:
            my_vClass = traci.vehicle.getVehicleClass(vehID)
            # print("vehID: %s, vehClass: %s "%(vehID, vClass))
            
            veh_speed = traci.vehicle.getSpeed(vehID)
            for k in self.belongTC:
                light_state = traci.trafficlight.getRedYellowGreenState(k)
                for i in range(len(light_state)):
                    for j in range(len(light_state[i])):
                        if (light_state[i][j] == 'r' or light_state[i][j] == 'R') and veh_speed < 0.1: # stopped vehicle
                            isStopped = True
                        else:
                            isStopped = False
                    
            # count nVeh_v and nStoppedVeh_v
            for vclass_ind,vclass in enumerate(net.vClass): #vClass = ['truck','passenger','moped']
                if vclass == my_vClass:
                    self.nVeh_v[vclass_ind]=self.nVeh_v[vclass_ind]+1
                    # print(f"vclass:{vclass}")
                    # print(f"vclass_ind:{vclass_ind}")
                    if isStopped:
                        # print(f"vclass:{vclass}")
                        # print(f"vclass_ind:{vclass_ind}")
                        self.nStoppedVeh_v[vclass_ind]=self.nStoppedVeh_v[vclass_ind]+1
                    break
            
