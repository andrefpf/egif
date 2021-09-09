#include <limits.h>
#include <stdlib.h>
#include <stdio.h>

#include "bitarray.h"

struct BitArray * create_bitarray(int bytes) {
    struct BitArray * bitarray = malloc(sizeof(struct BitArray));
    bitarray->size = 0;
    bitarray->max_size = bytes * CHAR_BIT;
    bitarray->data = malloc(bytes);
    return bitarray;
}

void insert_bit(struct BitArray * bitarray, bool cond) {
    if (bitarray->size >= bitarray->max_size) {
        printf("ERROR: Exeeded array size. \n");
        exit(-1);
    }

    if (cond) {
        BITSET(bitarray->data, bitarray->size);
    } else {
        BITCLEAR(bitarray->data, bitarray->size);
    }
    bitarray->size++;
}

void clear_bitarray(struct BitArray * bitarray) {
    for (int i = 0; i < BITTOBYTE(bitarray->max_size); i++) {
        bitarray->data[i] = 0;
    }
    bitarray->size = 0;
}

