#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

#include "rle.h"


int rle_encode(struct BitArray * array) {
    int repeated = 0;
    struct BitArray * encoded = create_bitarray(array->max_size);

    for (int i = 0; i < BITTOBYTE(array->size); i++) {      
        if ((array->data[i] == 0) && (repeated < (1 << CHAR_BIT))) {
            repeated++;
        } 
        else if (repeated > 0) {
            bitarray_append_byte(0, encoded);
            bitarray_append_byte(repeated, encoded);
            bitarray_append_byte(bitarray_get_byte(i, array), encoded);
            repeated = 0;
        }
        else {
            bitarray_append_byte(bitarray_get_byte(i, array), encoded);
        }
    }

    free(array->data);
    array->data = encoded->data;
    array->size = encoded->size;
    delete_bitarray(encoded);

    return 0;
}

int rle_decode(struct BitArray * array) {
    int last_is_zero = false;
    struct BitArray * decoded = create_bitarray(array->max_size);

    for (int i = 0; i < BITTOBYTE(array->size); i++) {
        if (array->data[i] == 0) {
            last_is_zero = true;
        }
        else if (last_is_zero) {
            last_is_zero = false;
            for (int j = 0; j < array->data[i]; j++) {
                bitarray_append_byte(0, decoded);
            }
        }
        else {
            bitarray_append_byte(bitarray_get_byte(i, array), decoded);
        }
    }

    free(array->data);
    array->data = decoded->data;
    array->size = decoded->size;
    delete_bitarray(decoded);

    return 0;
}