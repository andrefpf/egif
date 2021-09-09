#ifndef __BITARRAY_H__
#define __BITARRAY_H__

#include <stdbool.h>

#define BITMASK(b) (1 << ((b) % CHAR_BIT))
#define BITSLOT(b) ((b) / CHAR_BIT)
#define BITSET(a, b) ((a)[BITSLOT(b)] |= BITMASK(b))
#define BITCLEAR(a, b) ((a)[BITSLOT(b)] &= ~BITMASK(b))
#define BITTEST(a, b) ((a)[BITSLOT(b)] & BITMASK(b))
#define BITNSLOTS(nb) ((nb + CHAR_BIT - 1) / CHAR_BIT)
#define BITTOBYTE(a) (a/CHAR_BIT)


struct BitArray {
    int size;
    int max_size;
    char * data;
};

struct BitArray * create_bitarray(int bytes);

void insert_bit(struct BitArray * bitarray, bool cond);

void clear_bitarray(struct BitArray * bitarray);

#endif
