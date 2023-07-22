# -*- coding: utf-8 -*-

#### 設定測試情境，分別為：'AM'、'PM'、'OFF'、'WPM' ####
scen = 'AM'

#### 設定sumo config檔、rou檔路徑 ####
# file_path = os.getcwd()+'\\'
sim_file_path = 'sumo_Taipei_'+scen+'\\Taipei_'+scen+'.sumocfg'
rou_file_path = 'sumo_Taipei_'+scen+'\\'

#### 設定總模擬測試次數 ####
episode_count = 10

#### 設定亂數種子，數量至少大於等於模擬episode數 ####
seed = [4310, 18767, 22190, 24564, 36100, 40592, 40654, 53926, 58718, 62868]

#### 設定總模擬秒數，固定前1800秒為暖機時間 ####
sim_sec = 9000           # including warm-up period

#### 設定跑 固定時制(Fixtime = True) 或是 AI(Fixtime = False) ####
Fixtime = False
# Fixtime = True

#### 設定是否要GUI畫面 ####
GUI = True
# GUI = False


