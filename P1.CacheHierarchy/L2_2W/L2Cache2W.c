#include "L2Cache2W.h"
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
		exit(-1);

	if (mode == MODE_READ) {
		memcpy(data, &(DRAM[address]), BLOCK_SIZE);
		time += DRAM_READ_TIME;
	}

	if (mode == MODE_WRITE) {
		memcpy(&(DRAM[address]), data, BLOCK_SIZE);
		time += DRAM_WRITE_TIME;
	}
}

/*********************** L1 cache *************************/
void accessL1(uint32_t address, uint8_t *data, uint32_t mode) {

	uint32_t index, Tag, offset;
	uint8_t TempBlock[BLOCK_SIZE];

	/* init cache */
	if (SimpleL1Cache.init == 0) {
		for (int i = 0; i < 256; i++)
				SimpleL1Cache.lines[i].Valid = 0;
		SimpleL1Cache.init = 1;
	}

	Tag = address >> 14;
	index = address << 18;
	index = index >> 24;
	offset = address << 26;
	offset = offset >> 26;

	CacheLine *Line = &SimpleL1Cache.lines[index];

	// if there's a miss
	if (!Line->Valid || Line->Tag != Tag) {

		accessL2(address, TempBlock, MODE_READ);

		if ((Line->Valid) && (Line->Dirty)) { // line has dirty block
			accessL2(address, &(L1_Cache[index * BLOCK_SIZE]), MODE_WRITE); // then write back old block
		}

		memcpy(&(L1_Cache[index * BLOCK_SIZE]), TempBlock, BLOCK_SIZE); // copy new block to cache line
		Line->Valid = 1;
		Line->Tag = Tag;
		Line->Dirty = 0;
		Line->Index = index;
	} // if miss, then replaced with the correct block

	if (mode == MODE_READ) { // read data from cache line
		memcpy(data, &(L1_Cache[index * BLOCK_SIZE + offset]), WORD_SIZE);
		time += L1_READ_TIME;
	}

	if (mode == MODE_WRITE) { // write data from cache line
		memcpy(&(L1_Cache[index * BLOCK_SIZE + offset]), data, WORD_SIZE);
		time += L1_WRITE_TIME;
		Line->Dirty = 1;
	}
}

/*********************** L2 cache *************************/
void accessL2(uint32_t address, uint8_t *data, uint32_t mode) {

	uint32_t index, Tag, MemAddress, offset;
	uint8_t TempBlock[BLOCK_SIZE], oldest;

	/* init cache */
	if (SimpleL2Cache.init == 0) {
		for (int i = 0; i < 256; i++){
				SimpleL2Cache.sets[i].oldest = 0;
				for(int j = 0; j < 2; j++)
					SimpleL2Cache.sets[i].lines[j].Valid = 0;
		} SimpleL2Cache.init = 1;
	}

	Tag = address >> 14;
	index = address << 18;
	index = index >> 24;
	offset = address << 26;
	offset = offset >> 26;

	MemAddress = address >> 6;
	MemAddress = MemAddress << 6;

	CacheSet *set = &SimpleL2Cache.sets[index];
	oldest = set->oldest;

	// checks the set for a hit
	for(int i = 0; i < 2; i++) {

		if (set->lines[i].Valid && set->lines[i].Tag == Tag) {  // hit
			
			if (mode == MODE_READ) { // read data from cache
				memcpy(data, &(L2_Cache[(index + i) * BLOCK_SIZE + offset]), WORD_SIZE);
				time += L2_READ_TIME;
			} 

			if (mode == MODE_WRITE) { // write data on cache
				memcpy(&(L2_Cache[(index + i)* BLOCK_SIZE + offset]), data, WORD_SIZE);
				time += L2_WRITE_TIME;
				set->lines[i].Dirty = 1;
			}
			// switch the LRU block
			set->oldest = set->oldest == 0 ? 1 : 0;
		}
	} 

	// if there is a miss
	if ((!set->lines[0].Valid || set->lines[0].Tag != Tag) && (!set->lines[1].Valid || set->lines[1].Tag != Tag)) {
		
		accessDRAM(MemAddress, TempBlock, MODE_READ); // get new block from DRAM

		// if line has dirty block - update DRAM
		if (set->lines[oldest].Valid && (set->lines[oldest].Dirty)) {
			MemAddress = set->lines[oldest].Tag << 14;
			MemAddress = MemAddress + set->lines[oldest].Index;
			// write back dirty block to DRAM
			accessDRAM(MemAddress, &(L2_Cache[(index + oldest) * BLOCK_SIZE]), MODE_WRITE);
		}

		// write allocate new block to cache
		memcpy(&(L2_Cache[(index + oldest) * BLOCK_SIZE]), TempBlock, BLOCK_SIZE);
		set->lines[oldest].Valid = 1;
		set->lines[oldest].Tag = Tag;
		set->lines[oldest].Dirty = 0;

		if (mode == MODE_READ) { // read data from cache set
			memcpy(data, &(L2_Cache[(index + oldest) * BLOCK_SIZE + offset]), WORD_SIZE);
			time += L2_READ_TIME;
		} 

		if (mode == MODE_WRITE) { // write data from cache set
			memcpy(&(L2_Cache[(index + oldest)* BLOCK_SIZE + offset]), data, WORD_SIZE);
			time += L2_WRITE_TIME;
			set->lines[oldest].Dirty = 1;
		}
		// switch the LRU block
		set->oldest = set->oldest == 0 ? 1 : 0;
	}
}

void read(uint32_t address, uint8_t *data) {
	accessL1(address, data, MODE_READ);
}

void write(uint32_t address, uint8_t *data) {
	accessL1(address, data, MODE_WRITE);
}
