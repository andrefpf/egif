#include <limits.h>
#include <stdlib.h>
#include <stdio.h>

#include "bitarray.h"


// 
struct BitArray * bitarray_create(int bits) {
    struct BitArray * bitarray = malloc(sizeof(struct BitArray));
    bitarray->size = 0;
    bitarray->max_size = bits;
    bitarray->data = malloc((bits / BYTESIZE) + 1);
    return bitarray;
}

int bitarray_clear(struct BitArray * bitarray) {
    free(bitarray->data);
    free(bitarray);
    return 0;
}

// 
int bitarray_size_bits(struct BitArray * bitarray) {
    return bitarray->size;
}

int bitarray_size_bytes(struct BitArray * bitarray) {
    return BITTOBYTE(bitarray->size);
}

//
int bitarray_append_bit(int val, struct BitArray * bitarray) {
    BITSET(bitarray->data, bitarray->size);
    bitarray->size++;
    return 0;
}

int bitarray_append_byte(int val, struct BitArray * bitarray) {
    bitarray->data[bitarray_size_bytes(bitarray)] = (char) val;
    bitarray->size += BYTESIZE;
    return 0;
}

// 
int bitarray_pop_bit(struct BitArray * bitarray) {
    bitarray->size--;
    return BITTEST(bitarray->data, bitarray->size);
}

int bitarray_pop_byte(struct BitArray * bitarray) {
    int dif = (bitarray->size % BYTESIZE);
    bitarray->size -= (dif) ? dif : BYTESIZE;
    return bitarray->data[bitarray_size_bytes(bitarray)];
}

// 
int bitarray_set_bit(int index, int value, struct BitArray * bitarray) {
    if (value) {
        BITSET(bitarray->data, index);
    } else {
        BITCLEAR(bitarray->data, index);
    }
    return 0;
}

int bitarray_set_byte(int index, int value, struct BitArray * bitarray) {
    bitarray->data[index] = value;
    return 0;
}


// 
int bitarray_get_bit(int index, struct BitArray * bitarray) {
    return BITTEST(bitarray->data, index);
}

int bitarray_get_byte(int index, struct BitArray * bitarray) {
    return bitarray->data[index];
}


