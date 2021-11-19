import xlrd
 
wb = xlrd.open_workbook("calibTemp.xls")

sheetName = list()

for value in wb.sheet_names():
  sheetName.append(value)

fileStartRaw = 1
rawValColumn = 0
realValColumn = 1
coeffColumn = 2
commentColumn = 3
headerColumn = 4

cfile= open("calib.c","w")
hfile= open("calib.h","w")

cfile.write("/*\n"
                " *   calib.c\n *\n"
                " *      Author: aokutlu\n"
             "*/\n\n"
            )

hfile.write("/*\n"
                " *   calib.h\n *\n"
                " *      Author: aokutlu\n"
             "*/\n\n"
            "#ifndef CALIB_H_\n"
            "#define CALIB_H_\n\n"
            )

hfile.write("typedef struct \n"
            "{\n"
            "  twoPointPrams *pram;\n"
            "  calibrationElements *calTable;\n"
            "  uint8 size;\n"
            "}calibTables;\n\n"
            )

sheetNumber = wb.nsheets
sheetIndex = 0
sheet = wb.sheet_by_index(sheetIndex)

header = sheet.cell_value(fileStartRaw, headerColumn)

cfile.write("#include \"" + header +"\"\n")

hfile.write("/*--------------------------------------------------------*/" + "\n")
hfile.write("#define calibTableSize " + str(sheetNumber) + "\n")
hfile.write("/*--------------------------------------------------------*/" + "\n")

calibrationParamList = list()

for sheetIndex in range(sheetNumber):
  sheet = wb.sheet_by_index(sheetIndex)
    
  calibrationElementIndex = 1
  calibrationElementSize = sheet.nrows - 1

  raw = sheet.cell_value(fileStartRaw, rawValColumn)
  real = sheet.cell_value(fileStartRaw, realValColumn)
  coef = sheet.cell_value(fileStartRaw, coeffColumn)
  comment = sheet.cell_value(fileStartRaw, commentColumn)

  calibrationElement = sheetName[sheetIndex]
  calibrationElementNumber = calibrationElement + "Size"
  calibrationElementPram =calibrationElement + "Pram"
  
  calibrationParamList.append(calibrationElementPram + "," + calibrationElement + "," + calibrationElementNumber)

  hfile.write("#define " + calibrationElementNumber +" " + str(int(calibrationElementSize)) + "\n")
  hfile.write("/*--------------------------------------------------------*/" + "\n")

  cfile.write("/*--------------------------------------------------------*/" + "\n")
  cfile.write("calibrationElements "  +calibrationElement + "[" + calibrationElementNumber + "] = " + "\n")
  cfile.write("{  // {{rawValue0, realValue0},{rawValue1, realValue1}, coefficient }," + "\n")
  cfile.write("/*" + str(calibrationElementIndex) +"*/" + "        {{0  , 0   },"  +
                                                                 "{" + str(int(raw)) + "  ,  " + str(int(real)) + "   }," + str(int(coef))  + "     }," +
                                                                 "//" + comment + "\n")
  calibrationIndex = 0
  for calibrationIndex in range(calibrationElementSize-1):
    cfile.write("/*" + str(int(calibrationElementIndex + 1)) +"*/" + "        {{"  +  str(int(raw+1)) + "  ,  " + str(int(real+1)) + "   },")
    raw = sheet.cell_value(fileStartRaw+calibrationElementIndex, rawValColumn)
    real = sheet.cell_value(fileStartRaw+calibrationElementIndex, realValColumn)
    coef = sheet.cell_value(fileStartRaw+calibrationElementIndex, coeffColumn)
    comment = sheet.cell_value(fileStartRaw+calibrationElementIndex, commentColumn)
    cfile.write("{" + str(int(raw)) + "  ,  " + str(int(real)) + "   }," + str(int(coef))  + "     }," +"//" + comment + "\n")
    calibrationElementIndex =  calibrationElementIndex + 1

  cfile.write("};" + "\n\n")
  cfile.write("twoPointPrams " + calibrationElementPram + "[" + calibrationElementNumber + "];" + "\n")
  cfile.write("/*--------------------------------------------------------*/" + "\n\n")

cfile.write("calibTables calibTable[calibTableSize] = \n"
            "{\n")
for sheetIndex in range(sheetNumber):
  cfile.write("   {" + calibrationParamList[sheetIndex] + "},\n")
cfile.write("};\n\n")  
  
cfile.write("void initCalibration(void)" + "\n")
cfile.write("{" + "\n")
sheetIndex = 0
for sheetIndex in range(sheetNumber):
  cfile.write("    initTwoPointCalibation(" + calibrationParamList[sheetIndex] + ");\n")
cfile.write("}" + "\n\n")

cfile.write("void getCalibratedValues(uint8 pramId, uint32 *rawData, int32 *calibData)" + "\n")
cfile.write("{" + "\n")
cfile.write("    getTwoPointCalibratedValue(calibTable[pramId].pram, calibTable[pramId].calTable, calibTable[pramId].size, rawData, calibData);\n")
cfile.write("}" + "\n\n")

hfile.write("extern void initCalibration(void);" + "\n")
hfile.write("extern void getCalibratedValues(uint8 , uint32 *, int32 *);" + "\n")
hfile.write("\n#endif /* CALIB_H_ */" + "\n")

print("update clib.c file")
print("update clib.h file")


cfile.close();
hfile.close();
