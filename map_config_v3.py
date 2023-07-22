# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:00:00 2020

@author: Tenthousand
"""

import numpy as np

control_sg_id = [2,3,4]                    # major control
cooperate_sg_id = [1,5,6,7]                # doesn't affect anything, just a note
noncontrol_sg_id = [1,5,6,7]               # can get remaining phase time from backup plan, but still run default pro number in vissim
outrange_sg_id = []                        # doesn't affect anything, just a note



phase_sequence = [[1,2,3],            #1 2 3 
                  [1,2,3],            #4 5 6
                  [1,2,3,4,5,6]]      #7 8 9 10 11 12

max_phase_timing = [[150,38,75],
                    [150,30,75],
                    [20,110,15,50,55,50]]

min_phase_timing = [[75,28,35],
                    [75,20,35],
                    [10,60,10,15,25,15]]


amber = [[3,3,3],
         [3,3,3],
         [3,3,3,3,3,3]]

allred = [[2,20,2],
          [2,2,2],
          [2,2,2,2,2,2]]


agent_set = [[2],
             [3],
             [4]]



agent_phase_sequence = [[[1,2,3]],
                        [[1,2,3]],
                        [[1,2,3,4,5,6]]]


early_close = 10


fix_offset = [65,
              65,
              70]      #based on 909



max_green = []
min_green = []


for x in range(len(control_sg_id)):
    max_green.append(list(np.array(max_phase_timing[x])-np.array(amber[x])-np.array(allred[x])))
    min_green.append(list(np.array(min_phase_timing[x])-np.array(amber[x])-np.array(allred[x])))
    for m in min_green[x]:
        if m <= 0 :
            print('Error!! min green time at intersection '+ str(x+control_sg_id[0]))
            print(min_green[x])

sim_sec = 9500

collecting_global_data = False

threshold_as_stop = 5 #kph




#被列在lane_index的車道會出現於state當中
#lane_index"會影響"資料蒐集!!
#			[laneID, laneCode, at which intersection(agent), QC No]
lane_index=[(1,	"999020201-1", '1', '1'),
            (2,	"999020201-2", '1', '1'),
            (1,	"999020202-1", '1', '2'),
            (2,	"999020202-2", '1', '2'),
            (3,	"999020301-1", '1', '3'),
            (4,	"999020401-1", '1', '4'),
            (5,	"999020401-2", '1', '4'),
            
            (6,	"999030201-1", '2', '5'),
            (7,	"999030201-2", '2', '5'),
            (8, "999030401-1", '2', '6'),
            (9,	"999030401-2", '2', '6'),
            
			(10,"999040101-1", '3', '7'),            
			(11,"999040201-1", '3', '8'),
			(12,"999040201-2", '3', '8'),
			(13,"999040201-3", '3', '8'),
			(11,"999040202-1", '3', '9'),
			(12,"999040203-1", '3', '10'),
			(13,"999040203-2", '3', '10'),
            (12,"999040204-1", '3', '11'),
            (13,"999040204-2", '3', '11'),
            (14,"999040301-1", '3', '12'),
            (15,"999040301-2", '3', '12'),
            (16,"999040401-1", '3', '13'),
            (17,"999040401-2", '3', '13'),
            (18,"999040401-3", '3', '13'),            
            (16,"999040402-1", '3', '14'),
            (17,"999040403-1", '3', '15'),
            (18,"999040403-2", '3', '15'),
            (17,"999040404-1", '3', '16'),               
            (18,"999040404-2", '3', '16'),
            ]




#punishment_QC"會影響"資料蒐集!!!
#			[at which intersection(agent), QC No, punishment]
punishment_QC = []

#只有被列在Q_in_range_list中的stop delay會顯示於每次ep的報表中
#但Q_in_range_list"不影響"訓練或資料蒐集
Q_in_range_list = list(range(1,16,1))

#只有被列在weights_QC中的stop delay才會被計算進reward
#weights_QC"不影響"資料蒐集
#			[ QC No, weight, at which intersection(agent),]
weights_QC = [('1',1.5,   '1'),
              ('2',1,   '1'),
              ('3',1,   '1'),
              ('4',1.5,   '1'),
              
              ('17',1,   '1'),
              ('19',1,   '1'),
              #--
              ('5',1,   '2'),
              ('6',1.5,   '2'),
              #--
              ('7',1,   '3'),
              ('8',2,   '3'),
              ('9',1,   '3'),
              ('10',1,  '3'),
              ('11',1,  '3'),
              ('12',1,  '3'),
              ('13',2,  '3'),
              ('14',2,  '3'),
              ('15',2,  '3'),
              ('16',2,  '3'),
              
              ('18',1.5,   '3'),
              ('20',1,   '3'),              
              ]

Q_in_R_list =  [m[0]for m in weights_QC]




SG2_909_timing = [115,5,47]
SG3_909_timing = [135,20,30]
SG4_909_timing = [5,85,5,18,40,17]




#phase timing (include amber & all red)
SG1_902_timing = [8,97,10,35]
SG1_903_timing = [8,97,10,35]
SG1_904_timing = [8,97,10,35]
SG1_909_timing = [8,132,10,50]
SG1_910_timing = [8,132,10,50]

SG5_901_timing = [56,28,36]
SG5_902_timing = [100,45,55]
SG5_904_timing = [100,45,55]
SG5_907_timing = [97,43,60]
SG5_908_timing = [100,45,55]
SG5_909_timing = [90,43,67]
SG5_910_timing = [95,40,65]
SG5_911_timing = [85,43,72]

SG6_902_timing = [35,25]
SG6_907_timing = [35,25]
SG6_909_timing = [40,35]
SG6_910_timing = [40,35]

SG7_902_timing = [35,10,75,28]
SG7_904_timing = [36,15,71,28]
SG7_907_timing = [59,14,99,28]
SG7_908_timing = [35,10,77,28]
SG7_909_timing = [50,14,95,41]
SG7_910_timing = [53,16,90,41]
SG7_911_timing = [37,15,70,28]
SG7_912_timing = [37,15,70,28]
SG7_913_timing = [51,15,93,41]



back_up_timing_plan = [ SG1_909_timing,
                        SG2_909_timing,
                        SG3_909_timing,
                        SG4_909_timing,
                        SG5_909_timing,
                        SG6_909_timing,
                        SG7_909_timing ]



noncontrol_phase_time = [
        SG1_909_timing,
        SG5_909_timing,
        SG6_909_timing,
        SG7_909_timing
        ]

