#include "interpret_CAN.h"
#include <stdint.h>

/*
 *  Converts a CANID and its associated byte buffer to a set of key-value pairs.
 *    With the keys being strings and the values being integers.
 */
void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, int* numRetValues) {
  
  int bufLen = 0;

  switch (canId) {
    case 0x0:
    {
      bufLen = 2;
      int tmpSum = 0;
      for (int i = 0; i < bufLen; i++) {
	tmpSum += (int) messageBuf[i];
      }
      retStr[0] = "TestValue";
      retValues[0] = tmpSum;
      retStr[1] = "Cake";
      retValues[1] = 9001;
      *numRetValues = 2;
      break;
    }

    /*
     *	Contains the battery high cell voltage and the battery low cell voltage. 
     */
    case CAN_ID_BPS_FRAME0:
    {
      int highVoltage = messageBuf[BPS_HIGH_CELL_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_HIGH_CELL_VOLTAGE_LOW_BYTE];  
      int lowVoltage = messageBuf[BPS_LOW_CELL_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_LOW_CELL_VOLTAGE_LOW_BYTE];
      
      retStr[0] = "bpsHighVoltage";
      retStr[1] = "bpsLowVoltage";
      retValues[0] = highVoltage;
      retValues[1] = lowVoltage;
      *numRetValues = 2;
      break;
    }

    /*
     *	Contains the battery pack amp hours, total number of pack cycles, 
     *	and the pack health.
     */
    case CAN_ID_BPS_FRAME1:
    {
      int packAmpHours = messageBuf[BPS_PACK_AMPHOURS_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_AMPHOURS_LOW_BYTE];
      int packCycles = messageBuf[BPS_TOTAL_PACK_CYCLES_HIGH_BYTE] << 8 | messageBuf[BPS_TOTAL_PACK_CYCLES_LOW_BYTE];
      int packHealth = messageBuf[BPS_PACK_HEALTH_BYTE];
      
      retStr[0] = "packAmpHours";
      retStr[1] = "packTotalCycles";
      retStr[2] = "packHealth";
      retValues[0] = packAmpHours;
      retValues[1] = packCycles;
      retValues[2] = packHealth;
      *numRetValues = 3;
      break;
    }

    /*
     *	Contains the battery and BPS temperature.
     */
    case CAN_ID_BPS_FRAME2:
    {
      int highestCellTemperature = messageBuf[BPS_HIGHEST_CELL_TEMPERATURE_BYTE];
      int lowestCellTemperature = messageBuf[BPS_LOWEST_CELL_TEMPERATURE_BYTE];
      int averageCellTemperature = messageBuf[BPS_AVERAGE_CELL_TEMPERATURE_BYTE];
      int internalBPSTemperature = messageBuf[BPS_INTERNAL_BPS_TEMPERATURE_BYTE];

      retStr[0] = "highestCellTemperature";
      retStr[1] = "lowestCellTemperature";
      retStr[2] = "averageCellTemperature";
      retStr[3] = "internalBPSTemperature";
      retValues[0] = highestCellTemperature;
      retValues[1] = lowestCellTemperature;
      retValues[2] = averageCellTemperature;
      retValues[3] = internalBPSTemperature;
      *numRetValues = 4;
      break;
    }

    case CAN_ID_BPS_FRAME3:
    {
      int batteryPackCurrent = messageBuf[BPS_PACK_CURRENT_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_CURRENT_LOW_BYTE];
      int batteryPackInstantVoltage = messageBuf[BPS_PACK_INSTANTANEOUS_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_INSTANTANEOUS_VOLTAGE_LOW_BYTE];
      int batteryPackSummedVoltage = messageBuf[BPS_PACK_SUMMED_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_SUMMED_VOLTAGE_LOW_BYTE];

      retStr[0] = "batteryPackCurrent";
      retStr[1] = "batteryPackInstantaneousVoltage";
      retStr[2] = "batteryPackSummedVoltage";
      retValues[0] = batteryPackCurrent;
      retValues[1] = batteryPackInstantVoltage;
      retValues[2] = batteryPackSummedVoltage;
      *numRetValues = 3;
      break;
    }
  }
}
