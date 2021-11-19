/*
 *   calib.h
 *
 *      Author: aokutlu
*/

#ifndef CALIB_H_
#define CALIB_H_

typedef struct 
{
  twoPointPrams *pram;
  calibrationElements *calTable;
  uint8 size;
}calibTables;

/*--------------------------------------------------------*/
#define calibTableSize 1
/*--------------------------------------------------------*/
#define intPyrosVoltageSize 8
/*--------------------------------------------------------*/
extern void initCalibration(void);
extern void getCalibratedValues(uint8 , uint32 *, int32 *);

#endif /* CALIB_H_ */
