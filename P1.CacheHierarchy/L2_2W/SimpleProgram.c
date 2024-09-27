#include "L2Cache2W.h"

int main() {

  // set seed for random number generator
  srand(0);

  int clock1, value;

  resetTime();
  initCache();

  //try to read from an empty cache
  double avg = 0;
  int last = 0;
  for(int i = 0; i < DRAM_SIZE/4; i+=WORD_SIZE) {
    read(i, (unsigned char *)(&value));
    clock1 = getTime();
    avg += clock1-last;
    last = clock1;
  }  
  printf("Average time to read from an empty cache: %f\n", avg/(DRAM_SIZE/4));
  
  for(int n = 1; n <= DRAM_SIZE/4; n*=WORD_SIZE) {

    resetTime();
    initCache();

    printf("\nNumber of words: %d\n", (n-1)/WORD_SIZE + 1);
    
    for(int i = 0; i < n; i+=WORD_SIZE) {
      write(i, (unsigned char *)(&i));
      clock1 = getTime();
      printf("Write; Address %d; Value %d; Time %d\n", i, i, clock1);

    }

    for(int i = 0; i < n; i+=WORD_SIZE) {
      read(i, (unsigned char *)(&value));
      clock1 = getTime();
      printf("Read; Address %d; Value %d; Time %d\n", i, value, clock1);
    }  
    printf("\n Number of words:%d | Time:%d\n",(n-1)/WORD_SIZE+1,clock1);
  }

  printf("\nRandom accesses\n");

  // Do random accesses to the cache
  for(int i = 0; i < 100; i++) {
    int address = rand() % (DRAM_SIZE/4);
    address = address - address % WORD_SIZE;
    int mode = rand() % 2;
    if (mode == MODE_READ) {
      read(address, (unsigned char *)(&value));
      clock1 = getTime();
      printf("Read; Address %d; Value %d; Time %d\n", address, value, clock1);
    }
    else {
      write(address, (unsigned char *)(&address));
      clock1 = getTime();
      printf("Write; Address %d; Value %d; Time %d\n", address, address, clock1);
    }
  }
  printf("time:%d\n",clock1);
  
  //random acesses to the cache
 
  for(int n = 1; n <=(1<<16); n*=WORD_SIZE){
    resetTime();
    initCache();
    avg = 0;
    last = 0;
    int reads = 0;
    for(int i = 0; i < n; i+=WORD_SIZE) {
      int address = rand() % (DRAM_SIZE/4);
      address = address - address % WORD_SIZE;
      int mode = rand() % 2;
      if (mode == MODE_READ) {
        read(address, (unsigned char *)(&value));
        clock1 = getTime();
        
      }
      else {
        write(address, (unsigned char *)(&address));
        clock1 = getTime();
      }
      avg += clock1-last;
      last = clock1;
      reads++;
    }
    printf("Average time to read from a cache with %d words: %f\n", n, avg/reads);
    
  }
  return 0;
}
