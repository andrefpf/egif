#ifndef __BITARRAY_H__
#define __BITARRAY_H__

#define BYTESIZE 8
#define WORDSIZE 32

#define BITMASK(b) (1 << ((b) % BYTESIZE))
#define BITSLOT(b) ((b) / BYTESIZE)
#define BITSET(a, b) ((a)[BITSLOT(b)] |= BITMASK(b))
#define BITCLEAR(a, b) ((a)[BITSLOT(b)] &= ~BITMASK(b))
#define BITTEST(a, b) ((a)[BITSLOT(b)] & BITMASK(b))
#define BITNSLOTS(nb) ((nb + BYTESIZE - 1) / BYTESIZE)
#define BITTOBYTE(a) ((a % BYTESIZE) ? (a / BYTESIZE + 1) : (a / BYTESIZE))

typedef unsigned char byte_t;

struct BitArray {
    int size;
    int max_size;
    byte_t * data;
};


// 
struct BitArray * create_bitarray(int bits);

struct BitArray * create_bitarray_init(byte_t array[], int size, int max_size);

int delete_bitarray(struct BitArray * bitarray);

// 
int bitarray_size_bits(struct BitArray * bitarray);

int bitarray_size_bytes(struct BitArray * bitarray);

int bitarray_size_words(struct BitArray * bitarray);

// 
int bitarray_append_bit(int value, struct BitArray * bitarray);

int bitarray_append_byte(byte_t value, struct BitArray * bitarray);

int bitarray_append_word(int value, struct BitArray * bitarray);

//
int bitarray_pop_bit(struct BitArray * bitarray);

byte_t bitarray_pop_byte(struct BitArray * bitarray);

int bitarray_pop_word(struct BitArray * bitarray);

// 
int bitarray_set_bit(int index, int value, struct BitArray * bitarray);

int bitarray_set_byte(int index, byte_t value, struct BitArray * bitarray);

int bitarray_set_word(int index, int value, struct BitArray * bitarray);

// 
int bitarray_get_bit(int index, struct BitArray * bitarray);

byte_t bitarray_get_byte(int index, struct BitArray * bitarray);

int bitarray_get_word(int index, struct BitArray * bitarray);


#endif
