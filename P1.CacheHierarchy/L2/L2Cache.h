#ifndef L2CACHE_H
#define L2CACHE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "Cache.h"

void resetTime();

uint32_t getTime();

/****************  RAM memory (byte addressable) ***************/
void accessDRAM(uint32_t, uint8_t *, uint32_t);

/*********************** Cache *************************/

void initCache();
void accessL1(uint32_t, uint8_t *, uint32_t);

typedef struct CacheLine {
  uint8_t Valid;
  uint8_t Dirty;
  uint8_t Index; // to identify the cache line
  uint32_t Tag;
} CacheLine;

typedef struct L1Cache {
  uint32_t init;
  CacheLine lines[L1_NUM_LINES];
} L1Cache;

typedef struct L2Cache {
  uint32_t init;
  CacheLine lines[L2_NUM_LINES];
} L2Cache;

/*********************** Interfaces *************************/

void read(uint32_t, uint8_t *);

void write(uint32_t, uint8_t *);

#endif