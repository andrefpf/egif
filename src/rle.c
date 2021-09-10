#include <limits.h>
#include <stdio.h>

#include "rle.h"
#include "bitarray.h"


struct BitArray * rle_encode(struct BitArray * array) {
    int repeated = 0;
    struct BitArray * encoded = create_bitarray(BITTOBYTE(array->max_size));

    for (int i = 0; i < BITTOBYTE(array->size); i++) {      
        if ((array->data[i] == 0) && (repeated < (1 << CHAR_BIT))) {
            repeated++;
        } 
        else if (repeated > 0) {
            encoded->data[BITTOBYTE(encoded->size)] = 0;
            encoded->size += CHAR_BIT;

            encoded->data[BITTOBYTE(encoded->size)] = repeated;
            encoded->size += CHAR_BIT;

            encoded->data[BITTOBYTE(encoded->size)] = array->data[i];
            encoded->size += CHAR_BIT;

            repeated = 0;
        }
        else {
            encoded->data[BITTOBYTE(encoded->size)] = array->data[i];
            encoded->size += CHAR_BIT;
        }
    }
    return encoded;
}

struct BitArray * rle_decode(struct BitArray * array) {
    int last_is_zero = false;
    struct BitArray * decoded = create_bitarray(BITTOBYTE(array->max_size));

    for (int i = 0; i < BITTOBYTE(array->size); i++) {
        if (array->data[i] == 0) {
            last_is_zero = true;
        }
        else if (last_is_zero) {
            last_is_zero = false;
            for (int j = 0; j < array->data[i]; j++) {
                decoded->data[BITTOBYTE(decoded->size)] = 0;
                decoded->size += CHAR_BIT;
            }
        }
        else {
            decoded->data[BITTOBYTE(decoded->size)] = array->data[i];
            decoded->size += CHAR_BIT;
        }
    }

    return decoded;
}