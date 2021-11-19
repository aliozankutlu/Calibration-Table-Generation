/*
 *   calib.c
 *
 *      Author: aokutlu
*/

#include "global.h"
/*--------------------------------------------------------*/
calibrationElements intPyrosVoltage[intPyrosVoltageSize] = 
{  // {{rawValue0, realValue0},{rawValue1, realValue1}, coefficient },
/*1*/        {{0  , 0   },{404  ,  10   },10     },//10V 
/*2*/        {{405  ,  11   },{500  ,  20   },15     },//15V
/*3*/        {{501  ,  21   },{600  ,  30   },20     },//10V 
/*4*/        {{601  ,  31   },{700  ,  40   },70     },//20V
/*5*/        {{701  ,  41   },{404  ,  10   },10     },//10V 
/*6*/        {{405  ,  11   },{500  ,  20   },15     },//15V
/*7*/        {{501  ,  21   },{600  ,  30   },20     },//10V 
/*8*/        {{601  ,  31   },{700  ,  40   },70     },//20V
};

twoPointPrams intPyrosVoltagePram[intPyrosVoltageSize];
/*--------------------------------------------------------*/

calibTables calibTable[calibTableSize] = 
{
   {intPyrosVoltagePram,intPyrosVoltage,intPyrosVoltageSize},
};

void initCalibration(void)
{
    initTwoPointCalibation(intPyrosVoltagePram,intPyrosVoltage,intPyrosVoltageSize);
}

void getCalibratedValues(uint8 pramId, uint32 *rawData, int32 *calibData)
{
    getTwoPointCalibratedValue(calibTable[pramId].pram, calibTable[pramId].calTable, calibTable[pramId].size, rawData, calibData);
}

