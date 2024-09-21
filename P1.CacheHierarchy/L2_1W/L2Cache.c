#include "L2Cache.h"
#include "Cache.h"

uint8_t L1_Cache[L1_SIZE];
uint8_t L2_Cache[L2_SIZE];
uint8_t DRAM[DRAM_SIZE];
uint32_t time;
L1Cache SimpleL1Cache;
L2Cache SimpleL2Cache;

/**************** Initialization ***************/
void initCache() {
  SimpleL1Cache.init = 0;
  SimpleL2Cache.init = 0;
}

/**************** Time Manipulation ***************/
void resetTime() { time = 0; }

uint32_t getTime() { return time; }

/****************  RAM memory (byte addressable) ***************/
void accessDRAM(uint32_t address, uint8_t *data, uint32_t mode) {

  if (address >= DRAM_SIZE - WORD_SIZE + 1)
	exit(-1); //invalid memory access

  if (mode == MODE_READ) {
    memcpy(data, &(DRAM[address]), BLOCK_SIZE);
    time += DRAM_READ_TIME; //Add DRAM read
  }

  if (mode == MODE_WRITE) {
    memcpy(&(DRAM[address]), data, BLOCK_SIZE);
    time += DRAM_WRITE_TIME; //Add DRAM write  
  }
}

/*********************** L1 cache *************************/
void accessL1(uint32_t address, uint8_t *data, uint32_t mode) {

  uint32_t index, Tag, offset;
  uint8_t TempBlock[BLOCK_SIZE];

  /* init cache */
  if (SimpleL1Cache.init == 0) {
    for (int i = 0; i < L1_NUM_LINES; i++)
      SimpleL1Cache.lines[i].Valid = 0;
    SimpleL1Cache.init = 1;
  }

  // | Tag 18 | Index 8 | Offset 6 |
  Tag = address >> 14;
  index = address << 18;
  index = index >> 24;
  offset = address << 26;
  offset = offset >> 26;

  CacheLine *Line = &SimpleL1Cache.lines[index];

  /* access Cache*/

  if (!Line->Valid || Line->Tag != Tag) {      // if block not present - miss
    accessL2(address, TempBlock, MODE_READ);

    if ((Line->Valid) && (Line->Dirty)) { // line has dirty block, access L2
      accessL2(address, &(L1_Cache[index * BLOCK_SIZE]), MODE_WRITE); 
    }


    // copy new block to cache line
    memcpy(&(L1_Cache[index * BLOCK_SIZE]), TempBlock,
        BLOCK_SIZE);
    Line->Valid = 1;
    Line->Tag = Tag;
    Line->Dirty = 0;
    Line->Index = index;
  } // if miss, then replaced with the correct block


  //read/write to the cache
  if (mode == MODE_READ) {   
    memcpy(data, &(L1_Cache[index * BLOCK_SIZE + offset]), WORD_SIZE);
    time += L1_READ_TIME; // Add L1 cache read time
  }

  if (mode == MODE_WRITE) {
    memcpy(&(L1_Cache[index * BLOCK_SIZE + offset]), data, WORD_SIZE);
    time += L1_WRITE_TIME; // Add L1 cache write time
        Line->Dirty = 1; // Mark cache line as dirty
  }
}

/*********************** L2 cache *************************/
void accessL2(uint32_t address, uint8_t *data, uint32_t mode) {

  uint32_t index, Tag, MemAddress, offset;
  uint8_t TempBlock[BLOCK_SIZE];

  /* init cache */
  if (SimpleL2Cache.init == 0) {
    for (int i = 0; i < 512; i++)
      SimpleL2Cache.lines[i].Valid = 0;
    SimpleL2Cache.init = 1;
  }

  // | Tag 17 | Index 9 | Offset 6 |
  Tag = address >> 15; 
  index = address << 17; 
  index = index >> 23; 
  offset = address << 26; 
  offset = offset >> 26; 
  
  CacheLine *Line = &SimpleL2Cache.lines[index];
  
  // address without offset
  MemAddress = address >> 6; 
  MemAddress = MemAddress << 6; 

 

  /* access Cache*/

  if (!Line->Valid || Line->Tag != Tag) {// if block not present - miss

    accessDRAM(MemAddress, TempBlock, MODE_READ); // get new block from DRAM

    if ((Line->Valid) && (Line->Dirty)) { // line has dirty block
      MemAddress = Line->Tag << 15;
      MemAddress = MemAddress + Line->Index;   
      accessDRAM(MemAddress, &(L2_Cache[index * BLOCK_SIZE]), MODE_WRITE); 
    }

    // copy new block to cache line and update
    memcpy(&(L2_Cache[index * BLOCK_SIZE]), TempBlock,
        BLOCK_SIZE); 
    Line->Valid = 1;
    Line->Tag = Tag;
    Line->Dirty = 0;
    Line->Index = index;
  } // if miss, then replaced with the correct block

  // read/write to the cache
  if (mode == MODE_READ) { 
    memcpy(data, &(L2_Cache[index * BLOCK_SIZE + offset]), WORD_SIZE);
    time += L2_READ_TIME; // Add L2 cache read time
  }

  if (mode == MODE_WRITE) { 
    memcpy(&(L2_Cache[index * BLOCK_SIZE + offset]), data, WORD_SIZE);
    time += L2_WRITE_TIME; // Add L2 cache write time
    Line->Dirty = 1; // Mark cache line as dirty
  }
}

void read(uint32_t address, uint8_t *data) {
  accessL1(address, data, MODE_READ);
}

void write(uint32_t address, uint8_t *data) {
  accessL1(address, data, MODE_WRITE);
}
