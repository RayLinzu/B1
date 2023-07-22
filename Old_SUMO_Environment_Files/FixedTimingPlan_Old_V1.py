# -*- coding: utf-8 -*-

FixedTP = {
    'TL_01':{
        #各情境測試4時段定時時制秒數
        'TOD':{
            'AM':[[8, [8, 132, 10, 50]],
                  [8, [8, 132, 10, 50]],
                  [8, [8, 132, 10, 50]],
                  [8, [8, 132, 10, 50]]
            ],
            'PM':[[9, [8, 132, 10, 50]],
                  [9, [8, 132, 10, 50]],
                  [9, [8, 132, 10, 50]],
                  [9, [8, 132, 10, 50]]
            ],
            'OFF':[[1, [8, 97, 10, 35]],
                  [1, [8, 97, 10, 35]],
                  [1, [8, 97, 10, 35]],
                  [1, [8, 97, 10, 35]]
            ],
            'WPM':[[2, [8, 97, 10, 35]],
                  [2, [8, 97, 10, 35]],
                  [2, [8, 97, 10, 35]],
                  [2, [8, 97, 10, 35]]
            ]
        },
        #定時時制資料
        'PLAN':{
            1:{
                'Phase':4,
                'G':[8,92,10,30],
                'Y':[0,3,0,3],
                'R':[0,2,0,2],
                'Gstate':['rrrrrrGGG','GGgrrrGGG','rrrrrrrrr','rrrGGGrrr'],
                'Ystate':['','yyyrrryyy','','rrryyyrrr'],
                'Rstate':['','rrrrrrrrr','','rrrrrrrrr'], 
                'PhaseMap':[0,1,1,2,3,3,3],
                #時相1：8秒綠燈-時相2：92秒綠燈-時相2：3秒黃燈-時相3：10秒綠燈-時相4：30秒綠燈-時相4：3秒黃燈-2秒全紅
                'PhaseTimeInDuration':[8,92,3,10,30,3,2], 
                #時相1第1個區間：8秒(8+0+0)
                #時相2第1個區間：97秒(92+3+2)
                #時相2第2個區間：5秒(3+2)
                # ：92秒綠燈-時相2：3秒黃燈-時相3：10秒綠燈-時相4：30秒綠燈-時相4：3秒黃燈-2秒全紅
                'PhaseDuration':[8,97,5,10,35,5,2]
            },
            2:{
                'Phase':4,
                'G':[8,92,10,30],
                'Y':[0,3,0,3],
                'R':[0,2,0,2],
                'Gstate':['rrrrrrGGG','GGgrrrGGG','rrrrrrrrr','rrrGGGrrr'],
                'Ystate':['','yyyrrryyy','','rrryyyrrr'],
                'Rstate':['','rrrrrrrrr','','rrrrrrrrr'],
                'PhaseMap':[0,1,1,2,3,3,3],
                'PhaseTimeInDuration':[8,92,3,10,30,3,2],
                'PhaseDuration':[8,97,5,10,35,5,2]
            },
            8:{
                'Phase':4,
                'G':[8,127,10,45],
                'Y':[0,3,0,3],
                'R':[0,2,0,2],
                'Gstate':['rrrrrrGGG','GGgrrrGGG','rrrrrrrrr','rrrGGGrrr'],
                'Ystate':['','yyyrrryyy','','rrryyyrrr'],
                'Rstate':['','rrrrrrrrr','','rrrrrrrrr'],
                'PhaseMap':[0,1,1,2,3,3,3],
                'PhaseTimeInDuration':[8,127,3,10,45,3,2],
                'PhaseDuration':[8,132,5,10,50,5,2]
            },
            9:{
                'Phase':4,
                'G':[8,127,10,45],
                'Y':[0,3,0,3],
                'R':[0,2,0,2],
                'Gstate':['rrrrrrGGG','GGgrrrGGG','rrrrrrrrr','rrrGGGrrr'],
                'Ystate':['','yyyrrryyy','','rrryyyrrr'],
                'Rstate':['','rrrrrrrrr','','rrrrrrrrr'],
                'PhaseMap':[0,1,1,2,3,3,3],
                'PhaseTimeInDuration':[8,127,3,10,45,3,2],
                'PhaseDuration':[8,132,5,10,50,5,2]
            }
        }
    },
    
    'TL_02':{
        'TOD':{
            'AM':[[8, [9, 109, 10, 9, 14, 44]],
                  [8, [9, 109, 10, 9, 14, 44]],
                  [8, [9, 109, 10, 9, 14, 44]],
                  [8, [9, 109, 10, 9, 14, 44]]
            ],
            'PM':[[9, [115, 10, 57]],
                  [9, [115, 10, 57]],
                  [9, [115, 10, 57]],
                  [9, [115, 10, 57]]
            ],
            'OFF':[[3, [82, 10, 40]],
                  [1, [82, 10, 40]],
                  [1, [82, 10, 40]],
                  [1, [82, 10, 40]]
            ],
            'WPM':[[2, [120, 10, 52]],
                  [2, [120, 10, 52]],
                  [2, [120, 10, 52]],
                  [2, [120, 10, 52]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':3,
                'G':[77,5,35],
                'Y':[3,3,3],
                'R':[2,2,2],
                'Gstate':['GGGgrrrGGGgrrr','rrrrrrrGGGGrrr','rrrrGGgrrrrGGg'],
                'Ystate':['yyyyrrryyyyrrr','rrrrrrryyyyrrr','rrrryyyrrrryyy'],
                'Rstate':['rrrrrrrrrrrrrr','rrrrrrrrrrrrrr','rrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            2:{
                'Phase':3,
                'G':[115,5,47],
                'Y':[3,3,3],
                'R':[2,2,2],
                'Gstate':['GGGgrrrGGGgrrr','rrrrrrrGGGGrrr','rrrrGGgrrrrGGg'],
                'Ystate':['yyyyrrryyyyrrr','rrrrrrryyyyrrr','rrrryyyrrrryyy'],
                'Rstate':['rrrrrrrrrrrrrr','rrrrrrrrrrrrrr','rrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            3:{
                'Phase':3,
                'G':[77,5,35],
                'Y':[3,3,3],
                'R':[2,2,2],
                'Gstate':['GGGgrrrGGGgrrr','rrrrrrrGGGGrrr','rrrrGGgrrrrGGg'],
                'Ystate':['yyyyrrryyyyrrr','rrrrrrryyyyrrr','rrrryyyrrrryyy'],
                'Rstate':['rrrrrrrrrrrrrr','rrrrrrrrrrrrrr','rrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            8:{
                'Phase':6,
                'G':[9,104,7,9,14,44],
                'Y':[0,3,3,0,0,3],
                'R':[0,0,2,0,0,2],
                'Gstate':['rrrrrrrGGGgrrr','GGGgrrrGGGgrrr','rrrrrrrGGGgrrr','rrrrrrrrrrrrrr','rrrrrrrrrrrGGg','rrrrGGgrrrrGGg'],
                'Ystate':['','yyyyrrrGGGgrrr','rrrrrrryyyyrrr','','','rrrryyyrrrryyy'],
                'Rstate':['','','rrrrrrrrrrrrrr','','','rrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            9:{
                'Phase':3,
                'G':[110,5,52],
                'Y':[3,3,3],
                'R':[2,2,2],
                'Gstate':['GGGgrrrGGGgrrr','rrrrrrrGGGGrrr','rrrrGGgrrrrGGg'],
                'Ystate':['yyyyrrryyyyrrr','rrrrrrryyyyrrr','rrrryyyrrrryyy'],
                'Rstate':['rrrrrrrrrrrrrr','rrrrrrrrrrrrrr','rrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            }
        }
    },
    
    'TL_03':{
        'TOD':{
            'AM':[[8, [140, 25, 35]],
                  [8, [140, 25, 35]],
                  [8, [140, 25, 35]],
                  [8, [140, 25, 35]]
            ],
            'PM':[[9, [120, 25, 55]],
                  [9, [120, 25, 55]],
                  [9, [120, 25, 55]],
                  [9, [120, 25, 55]]
            ],
            'OFF':[[3, [100, 15, 35]],
                  [1, [100, 15, 35]],
                  [1, [100, 15, 35]],
                  [1, [100, 15, 35]]
            ],
            'WPM':[[2, [140, 25, 35]],
                  [2, [140, 25, 35]],
                  [2, [140, 25, 35]],
                  [2, [140, 25, 35]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':3,
                'G':[95,10,35],
                'Y':[3,3,0],
                'R':[2,2,0],
                'Gstate':['GGGGGg','rrrGGG','rrrrrr'],
                'Ystate':['yyyGGg','rrryyy',''],
                'Rstate':['rrrGGg','rrrrrr',''],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            2:{
                'Phase':3,
                'G':[135,20,35],
                'Y':[3,3,0],
                'R':[2,2,0],
                'Gstate':['GGGGGg','rrrGGG','rrrrrr'],
                'Ystate':['yyyGGg','rrryyy',''],
                'Rstate':['rrrGGg','rrrrrr',''],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            3:{
                'Phase':3,
                'G':[95,10,35],
                'Y':[3,3,0],
                'R':[2,2,0],
                'Gstate':['GGGGGg','rrrGGG','rrrrrr'],
                'Ystate':['yyyGGg','rrryyy',''],
                'Rstate':['rrrGGg','rrrrrr',''],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            8:{
                'Phase':3,
                'G':[135,20,35],
                'Y':[3,3,0],
                'R':[2,2,0],
                'Gstate':['GGGGGg','rrrGGG','rrrrrr'],
                'Ystate':['yyyGGg','rrryyy',''],
                'Rstate':['rrrGGg','rrrrrr',''],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            9:{
                'Phase':3,
                'G':[115,20,55],
                'Y':[3,3,0],
                'R':[2,2,0],
                'Gstate':['GGGGGg','rrrGGG','rrrrrr'],
                'Ystate':['yyyGGg','rrryyy',''],
                'Rstate':['rrrGGg','rrrrrr',''],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            }
        }
    },
    
    'TL_04':{
        'TOD':{
            'AM':[[8, [10, 90, 10, 23, 45, 22]],
                  [8, [10, 90, 10, 23, 45, 22]],
                  [8, [10, 90, 10, 23, 45, 22]],
                  [8, [10, 90, 10, 23, 45, 22]]
            ],
            'PM':[[9, [10, 89, 15, 7, 55, 24]],
                  [9, [10, 89, 15, 7, 55, 24]],
                  [9, [10, 89, 15, 7, 55, 24]],
                  [9, [10, 89, 15, 7, 55, 24]]
            ],
            'OFF':[[3, [15, 60, 10, 15, 35, 15]],
                  [1, [14, 58, 14, 14, 35, 15]],
                  [1, [14, 58, 14, 14, 35, 15]],
                  [1, [14, 58, 14, 14, 35, 15]]
            ],
            'WPM':[[2, [10, 95, 10, 15, 50, 20]],
                  [2, [10, 95, 10, 15, 50, 20]],
                  [2, [10, 95, 10, 15, 50, 20]],
                  [2, [10, 95, 10, 15, 50, 20]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':6,
                'G':[14,53,9,14,30,10],
                'Y':[0,3,3,0,3,3],
                'R':[0,2,2,0,2,2],
                'Gstate':['GGGGrrrrrrrrrrrr','GGGgrrrrGGGgrrrr','rrrrrrrrGGGGrrrr','rrrrGGGGrrrrrrrr','rrrrGGGgrrrrGGGg','rrrrrrrrrrrrGGGG'],
                'Ystate':['','yyyyrrrrGGGgrrrr','rrrrrrrryyyyrrrr','','rrrryyyyrrrrGGGg','rrrrrrrrrrrryyyy'],
                'Rstate':['','rrrrrrrrGGGgrrrr','rrrrrrrrrrrrrrrr','','rrrrrrrrrrrrGGGg','rrrrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            2:{
                'Phase':6,
                'G':[10,90,5,15,45,15],
                'Y':[0,3,3,0,3,3],
                'R':[0,2,2,0,2,2],
                'Gstate':['GGGGrrrrrrrrrrrr','GGGgrrrrGGGgrrrr','rrrrrrrrGGGGrrrr','rrrrGGGGrrrrrrrr','rrrrGGGgrrrrGGGg','rrrrrrrrrrrrGGGG'],
                'Ystate':['','yyyyrrrrGGGgrrrr','rrrrrrrryyyyrrrr','','rrrryyyyrrrrGGGg','rrrrrrrrrrrryyyy'],
                'Rstate':['','rrrrrrrrGGGgrrrr','rrrrrrrrrrrrrrrr','','rrrrrrrrrrrrGGGg','rrrrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            3:{
                'Phase':6,
                'G':[15,55,5,15,30,10],
                'Y':[0,3,3,0,3,3],
                'R':[0,2,2,0,2,2],
                'Gstate':['GGGGrrrrrrrrrrrr','GGGgrrrrGGGgrrrr','rrrrrrrrGGGGrrrr','rrrrGGGGrrrrrrrr','rrrrGGGgrrrrGGGg','rrrrrrrrrrrrGGGG'],
                'Ystate':['','yyyyrrrrGGGgrrrr','rrrrrrrryyyyrrrr','','rrrryyyyrrrrGGGg','rrrrrrrrrrrryyyy'],
                'Rstate':['','rrrrrrrrGGGgrrrr','rrrrrrrrrrrrrrrr','','rrrrrrrrrrrrGGGg','rrrrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            8:{
                'Phase':6,
                'G':[10,85,5,23,40,17],
                'Y':[0,3,3,0,3,3],
                'R':[0,2,2,0,2,2],
                'Gstate':['GGGGrrrrrrrrrrrr','GGGgrrrrGGGgrrrr','rrrrrrrrGGGGrrrr','rrrrGGGGrrrrrrrr','rrrrGGGgrrrrGGGg','rrrrrrrrrrrrGGGG'],
                'Ystate':['','yyyyrrrrGGGgrrrr','rrrrrrrryyyyrrrr','','rrrryyyyrrrrGGGg','rrrrrrrrrrrryyyy'],
                'Rstate':['','rrrrrrrrGGGgrrrr','rrrrrrrrrrrrrrrr','','rrrrrrrrrrrrGGGg','rrrrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            },
            9:{
                'Phase':6,
                'G':[10,84,10,7,50,19],
                'Y':[0,3,3,0,3,3],
                'R':[0,2,2,0,2,2],
                'Gstate':['GGGGrrrrrrrrrrrr','GGGgrrrrGGGgrrrr','rrrrrrrrGGGGrrrr','rrrrGGGGrrrrrrrr','rrrrGGGgrrrrGGGg','rrrrrrrrrrrrGGGG'],
                'Ystate':['','yyyyrrrrGGGgrrrr','rrrrrrrryyyyrrrr','','rrrryyyyrrrrGGGg','rrrrrrrrrrrryyyy'],
                'Rstate':['','rrrrrrrrGGGgrrrr','rrrrrrrrrrrrrrrr','','rrrrrrrrrrrrGGGg','rrrrrrrrrrrrrrrr'],
                'PhaseMap':[],
                'PhaseTimeInDuration':[],
                'PhaseDuration':[]
            }
        }
    },
    
    'TL_05':{
        'TOD':{
            'AM':[[10, [88, 43, 69]],
                  [10, [88, 43, 69]],
                  [8, [93, 43, 68]],
                  [8, [93, 43, 68]]
            ],
            'PM':[[9, [95, 40, 65]],
                  [9, [95, 40, 65]],
                  [9, [95, 40, 65]],
                  [9, [95, 40, 65]]
            ],
            'OFF':[[3, [100, 45, 55]],
                  [1, [100, 45, 55]],
                  [1, [100, 45, 55]],
                  [1, [100, 45, 55]]
            ],
            'WPM':[[6, [97, 43, 60]],
                  [6, [97, 43, 60]],
                  [6, [97, 43, 60]],
                  [6, [97, 43, 60]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':3,
                'G':[94,45,49],
                'Y':[3,0,3],
                'R':[3,0,3],
                'Gstate':['GGGrrrrrGGGGG','rrrrrrrrrrrrr','rrrGGGGGGGGrr'],
                'Ystate':['yyyrrrrryyyyy','','rrryyyyyyyyrr'],
                'Rstate':['rrrrrrrrrrrrr','','rrrrrrrrrrrrr'],
                'PhaseMap':[0,0,1,2,2,2],
                'PhaseTimeInDuration':[94,3,45,49,3,3],
                'PhaseDuration':[100,6,45,55,6,3]
            },
            3:{
                'Phase':3,
                'G':[94,45,49],
                'Y':[3,0,3],
                'R':[3,0,3],
                'Gstate':['GGGrrrrrGGGGG','rrrrrrrrrrrrr','rrrGGGGGGGGrr'],
                'Ystate':['yyyrrrrryyyyy','','rrryyyyyyyyrr'],
                'Rstate':['rrrrrrrrrrrrr','','rrrrrrrrrrrrr'],
                'PhaseMap':[0,0,1,2,2,2],
                'PhaseTimeInDuration':[94,3,45,49,3,3],
                'PhaseDuration':[100,6,45,55,6,3]
            },
            6:{
                'Phase':3,
                'G':[91,43,54],
                'Y':[3,0,3],
                'R':[3,0,3],
                'Gstate':['GGGrrrrrGGGGG','rrrrrrrrrrrrr','rrrGGGGGGGGrr'],
                'Ystate':['yyyrrrrryyyyy','','rrryyyyyyyyrr'],
                'Rstate':['rrrrrrrrrrrrr','','rrrrrrrrrrrrr'],
                'PhaseMap':[0,0,1,2,2,2],
                'PhaseTimeInDuration':[91,3,43,54,3,3],
                'PhaseDuration':[97,6,43,60,6,3]
            },
            8:{
                'Phase':3,
                'G':[87,38,58],
                'Y':[3,3,5],
                'R':[3,2,5],
                'Gstate':['GGGGGgrrrrrGGGrrr','rrrrrrrrrrrrrrGGG','rrrrrrGGGGGGrrggr'],
                'Ystate':['yyyyyyrrrrryyyrrr','rrrrrrrrrrrrrryyy','rrrrrryyyyyyrryyr'],
                'Rstate':['rrrrrrrrrrrrrrrrr','rrrrrrrrrrrrrrrrr','rrrrrrrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1,2,2,2],
                'PhaseTimeInDuration':[87,3,3,38,3,2,58,5,5],
                'PhaseDuration':[93,6,3,43,5,2,68,10,5]
            },
            9:{
                'Phase':3,
                'G':[89,40,59],
                'Y':[3,0,3],
                'R':[3,0,3],
                'Gstate':['GGGrrrrrGGGGG','rrrrrrrrrrrrr','rrrGGGGGGGGrr'],
                'Ystate':['yyyrrrrryyyyy','','rrryyyyyyyyrr'],
                'Rstate':['rrrrrrrrrrrrr','','rrrrrrrrrrrrr'],
                'PhaseMap':[0,0,1,2,2,2],
                'PhaseTimeInDuration':[89,3,43,59,3,3],
                'PhaseDuration':[95,6,40,65,6,3]
            },
            10:{
                'Phase':3,
                'G':[82,38,63],
                'Y':[3,3,3],
                'R':[3,2,3],
                'Gstate':['GGGGGGrrrrrGGGrrr','rrrrrrrrrrrrrrGGG','rrrrrrGGGGGGrrrgg'],
                'Ystate':['yyyyyyrrrrryyyrrr','rrrrrrrrrrrrrryGG','rrrrrryyyyyyrrryy'],
                'Rstate':['rrrrrrrrrrrrrrrrr','rrrrrrrrrrrrrrrGG','rrrrrrrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1,2,2,2],
                'PhaseTimeInDuration':[82,3,3,38,3,2,63,3,3],
                'PhaseDuration':[88,6,3,43,5,2,69,6,3]
            }
        }
    },
    
    'TL_06':{
        'TOD':{
            'AM':[[10, [73, 37]],
                  [10, [73, 37]],
                  [8, [40, 35]],
                  [8, [40, 35]]
            ],
            'PM':[[8, [40, 35]],
                  [9, [40, 35]],
                  [9, [40, 35]],
                  [9, [40, 35]]
            ],
            'OFF':[[8, [35, 25]],
                  [1, [35, 25]],
                  [1, [35, 25]],
                  [1, [35, 25]]
            ],
            'WPM':[[6, [35, 25]],
                  [6, [35, 25]],
                  [6, [35, 25]],
                  [6, [35, 25]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':2,
                'G':[30,20],
                'Y':[3,3],
                'R':[2,2],
                'Gstate':['rrrGGgrrrGGg','GGgrrrGGgrrr'],
                'Ystate':['rrryyyrrryyy','yyyrrryyyrrr'],
                'Rstate':['rrrrrrrrrrrr','rrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1],
                'PhaseTimeInDuration':[30,3,2,20,3,2],
                'PhaseDuration':[35,5,2,25,5,2]
            },
            6:{
                'Phase':2,
                'G':[30,20],
                'Y':[3,3],
                'R':[2,2],
                'Gstate':['rrrGGgrrrGGg','GGgrrrGGgrrr'],
                'Ystate':['rrryyyrrryyy','yyyrrryyyrrr'],
                'Rstate':['rrrrrrrrrrrr','rrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1],
                'PhaseTimeInDuration':[30,3,2,20,3,2],
                'PhaseDuration':[35,5,2,25,5,2]
            },
            8:{
                'Phase':2,
                'G':[35,30],
                'Y':[3,3],
                'R':[2,2],
                'Gstate':['rrrGGgrrrGGg','GGgrrrGGgrrr'],
                'Ystate':['rrryyyrrryyy','yyyrrryyyrrr'],
                'Rstate':['rrrrrrrrrrrr','rrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1],
                'PhaseTimeInDuration':[35,3,2,30,3,2],
                'PhaseDuration':[40,5,2,35,5,2]
            },
            9:{
                'Phase':2,
                'G':[35,30],
                'Y':[3,3],
                'R':[2,2],
                'Gstate':['rrrGGgrrrGGg','GGgrrrGGgrrr'],
                'Ystate':['rrryyyrrryyy','yyyrrryyyrrr'],
                'Rstate':['rrrrrrrrrrrr','rrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1],
                'PhaseTimeInDuration':[35,3,2,30,3,2],
                'PhaseDuration':[40,5,2,35,5,2]
            },
            10:{
                'Phase':2,
                'G':[73,37],
                'Y':[3,3],
                'R':[32,2],
                'Gstate':['rrrGGgrrrGGg','GGgrrrGGgrrr'],
                'Ystate':['rrryyyrrryyy','yyyrrryyyrrr'],
                'Rstate':['rrrrrrrrrrrr','rrrrrrrrrrrr'],
                'PhaseMap':[0,0,0,1,1,1],
                'PhaseTimeInDuration':[73,3,32,37,3,2],
                'PhaseDuration':[108,76,32,42,5,2]
            }
        }
    },
    
    'TL_07':{
        'TOD':{
            'AM':[[12, [51, 15, 93, 41]],
                  [12, [51, 15, 93, 41]],
                  [8, [50, 14, 95, 41]],
                  [8, [50, 14, 95, 41]]
            ],
            'PM':[[12, [51, 15, 93, 41]],
                  [9, [53, 16, 90, 41]],
                  [9, [53, 16, 90, 41]],
                  [9, [53, 16, 90, 41]]
            ],
            'OFF':[[10, [37, 15, 70, 28]],
                  [1, [35, 10, 75, 28]],
                  [1, [35, 10, 75, 28]],
                  [1, [35, 10, 75, 28]]
            ],
            'WPM':[[6, [59, 14, 99, 28]],
                  [6, [59, 14, 99, 28]],
                  [6, [59, 14, 99, 28]],
                  [6, [59, 14, 99, 28]]
            ]
        },
        'PLAN':{
            1:{
                'Phase':4,
                'G':[32,10,67,28],
                'Y':[3,0,3,0],
                'R':[2,0,5,0],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrrrr'],
                'Ystate':['yyrrrrrr','','rryyyyyy',''],
                'Rstate':['rrrrrrrr','','rrrrrrrr',''],
                'PhaseMap':[0,0,0,1,2,2,3],
                'PhaseTimeInDuration':[32,3,2,10,67,3,28],
                'PhaseDuration':[37,5,2,10,75,8,28]
            },
            6:{
                'Phase':4,
                'G':[54,14,91,28],
                'Y':[3,0,3,0],
                'R':[2,0,5,0],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrrrr'],
                'Ystate':['yyrrrrrr','','rryyyyyy',''],
                'Rstate':['rrrrrrrr','','rrrrrrrr',''],
                'PhaseMap':[0,0,0,1,2,2,3],
                'PhaseTimeInDuration':[54,3,2,14,91,3,28],
                'PhaseDuration':[59,5,2,14,99,8,28]
            },
            8:{
                'Phase':4,
                'G':[45,14,87,5],
                'Y':[3,0,3,3],
                'R':[2,0,5,33],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrGGG'],
                'Ystate':['yyrrrrrr','','rryyyGGg','rrrrryyy'],
                'Rstate':['rrrrrrrr','','rrrrrGGG','rrrrrrrr'],
                'PhaseMap':[0,0,0,1,2,2,3,3,3],
                'PhaseTimeInDuration':[45,3,2,14,87,3,5,3,33],
                'PhaseDuration':[50,5,2,14,95,8,41,36,33]
            },
            9:{
                'Phase':4,
                'G':[48,16,82,5],
                'Y':[3,0,3,3],
                'R':[2,0,5,33],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrGGG'],
                'Ystate':['yyrrrrrr','','rryyyGGg','rrrrryyy'],
                'Rstate':['rrrrrrrr','','rrrrrGGG','rrrrrrrr'],
                'PhaseMap':[0,0,0,1,2,2,3,3,3],
                'PhaseTimeInDuration':[48,3,2,16,82,3,5,3,33],
                'PhaseDuration':[53,5,2,16,90,8,41,36,33]
            },
            10:{
                'Phase':4,
                'G':[32,15,62,28],
                'Y':[3,0,3,0],
                'R':[2,0,5,0],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrrrr'],
                'Ystate':['yyrrrrrr','','rryyyyyy',''],
                'Rstate':['rrrrrrrr','','rrrrrrrr',''],
                'PhaseMap':[0,0,0,1,2,2,3],
                'PhaseTimeInDuration':[32,3,2,15,62,3,28],
                'PhaseDuration':[37,5,2,15,70,8,28]
            },
            12:{
                'Phase':4,
                'G':[46,15,85,5],
                'Y':[3,0,3,3],
                'R':[2,0,5,33],
                'Gstate':['GGrrrrrr','rrrrrGGG','rrGGGGGg','rrrrrGGG'],
                'Ystate':['yyrrrrrr','','rryyyGGg','rrrrryyy'],
                'Rstate':['rrrrrrrr','','rrrrrGGG','rrrrrrrr'],
                'PhaseMap':[0,0,0,1,2,2,3,3,3],
                'PhaseTimeInDuration':[46,3,2,15,85,3,5,3,33],
                'PhaseDuration':[51,5,2,15,93,8,41,36,33]
            }
        }
    }
}

