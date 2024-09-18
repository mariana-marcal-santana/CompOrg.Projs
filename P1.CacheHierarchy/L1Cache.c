#include "L1Cache.h"

uint8_t L1Cache[L1_SIZE];
uint8_t L2Cache[L2_SIZE];
uint8_t DRAM[DRAM_SIZE];
uint32_t time;
Cache SimpleCache;

/**************** Time Manipulation ***************/
void resetTime() { time = 0; }

uint32_t getTime() { return time; }

/****************  RAM memory (byte addressable) ***************/
void accessDRAM(uint32_t address, uint8_t *data, uint32_t mode)
{

    if (address >= DRAM_SIZE - WORD_SIZE + 1)
        exit(-1);

    if (mode == MODE_READ)
    {
        memcpy(data, &(DRAM[address]), BLOCK_SIZE);
        time += DRAM_READ_TIME;
    }

    if (mode == MODE_WRITE)
    {
        memcpy(&(DRAM[address]), data, BLOCK_SIZE);
        time += DRAM_WRITE_TIME;
    }
}

/*********************** L1 cache *************************/

void initCache()
{
    for (int i = 0; i < L1_NUM_LINES; i++)
    {
        SimpleCache.lines[i].Valid = 0;
        SimpleCache.lines[i].Dirty = 0;
    }
    SimpleCache.init = 1;
}

void accessL1(uint32_t address, uint8_t *data, uint32_t mode)
{

    uint32_t index, Tag, offset, MemAddress;
    uint8_t TempBlock[BLOCK_SIZE];

    /* init cache */
    if (SimpleCache.init == 0)
        initCache();

    // Calculate index and tag
    // | Tag 18 | Index 8 | Offset 6 |
    Tag = address >> 14;
    index = address << 18;
    index = index >> 24;
    offset = address << 26;
    offset = offset >> 26;

    printf("Tag: %d\n", Tag);
    printf("Index: %d\n", index);
    printf("Offset: %d\n", offset);

    CacheLine *Line = &SimpleCache.lines[index];

    // addres without offset
    MemAddress = address >> 6;
    MemAddress = MemAddress << 6;

    /* access Cache*/
    if (!Line->Valid || Line->Tag != Tag)
    {                                                 // if block not present - miss
        accessDRAM(MemAddress, TempBlock, MODE_READ); // get new block from DRAM

        if ((Line->Valid) && (Line->Dirty))
        {                                 // line has dirty block
            MemAddress = Line->Tag << 14; // get address of the block in memory
            MemAddress = MemAddress + Line->Index;
            accessDRAM(MemAddress, &(L1Cache[index * BLOCK_SIZE]), MODE_WRITE); // then write back old block
        }

        memcpy(&(L1Cache[index * BLOCK_SIZE]), TempBlock,
               BLOCK_SIZE); // copy new block to cache line
        Line->Valid = 1;
        Line->Tag = Tag;
        Line->Dirty = 0;
        Line->Index = index;
    } // if miss, then replaced with the correct block

    if (mode == MODE_READ)
    { // read data from cache line
        // if (0 == (address % 8))
        // { // even word on block
        //     memcpy(data, &(L1Cache[0]), WORD_SIZE);
        // }
        // else
        // { // odd word on block
        //     memcpy(data, &(L1Cache[WORD_SIZE]), WORD_SIZE);
        // }
        // new
        memcpy(data, &(L1Cache[index * BLOCK_SIZE + offset]), WORD_SIZE);
        // new
        time += L1_READ_TIME;
    }

    if (mode == MODE_WRITE)
    { // write data from cache line
        // if (!(address % 8))
        // { // even word on block
        //     memcpy(&(L1Cache[0]), data, WORD_SIZE);
        // }
        // else
        // { // odd word on block
        //     memcpy(&(L1Cache[WORD_SIZE]), data, WORD_SIZE);
        // }
        // new
        memcpy(&(L1Cache[index * BLOCK_SIZE + offset]), data, WORD_SIZE);
        // new
        time += L1_WRITE_TIME;
        Line->Dirty = 1;
    }
}

void read(uint32_t address, uint8_t *data)
{
    accessL1(address, data, MODE_READ);
}

void write(uint32_t address, uint8_t *data)
{
    accessL1(address, data, MODE_WRITE);
}
