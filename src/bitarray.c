#include <limits.h>
#include <stdlib.h>
#include <stdio.h>

#include "bitarray.h"


// 
struct BitArray * create_bitarray(int bits) {
    struct BitArray * bitarray = malloc(sizeof(struct BitArray));
    bitarray->size = 0;
    bitarray->max_size = bits;
    bitarray->data = calloc((bits / BYTESIZE) + 1, 1);
    return bitarray;
}

struct BitArray * create_bitarray_init(byte_t array[], int size, int max_size) {
    struct BitArray * bitarray = create_bitarray(max_size * BYTESIZE);
    for (int i = 0; i < size; i++) {
        bitarray_append_byte((int) array[i], bitarray);
    }
    return bitarray;
}

int delete_bitarray(struct BitArray * bitarray) {
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
    if (val) {
        BITSET(bitarray->data, bitarray->size);
    }
    else {
        BITCLEAR(bitarray->data, bitarray->size);
    }
    bitarray->size++;
    return 0;
}

int bitarray_append_byte(byte_t val, struct BitArray * bitarray) {
    bitarray->data[bitarray_size_bytes(bitarray)] = (char) val;
    bitarray->size += BYTESIZE;
    return 0;
}

// 
int bitarray_pop_bit(struct BitArray * bitarray) {
    bitarray->size--;
    return BITTEST(bitarray->data, bitarray->size);
}

byte_t bitarray_pop_byte(struct BitArray * bitarray) {
    int dif = (bitarray->size % BYTESIZE);
    bitarray->size -= (dif) ? dif : BYTESIZE;
    return bitarray->data[bitarray_size_bytes(bitarray)];
}

// 
int bitarray_set_bit(int index, int value, struct BitArray * bitarray) {
    if (value) {
        BITSET(bitarray->data, index);
    } 
    else {
        BITCLEAR(bitarray->data, index);
    }
    return 0;
}

int bitarray_set_byte(int index, byte_t value, struct BitArray * bitarray) {
    bitarray->data[index] = value;
    return 0;
}


// 
int bitarray_get_bit(int index, struct BitArray * bitarray) {
    return BITTEST(bitarray->data, index);
}

byte_t bitarray_get_byte(int index, struct BitArray * bitarray) {
    return bitarray->data[index];
}


