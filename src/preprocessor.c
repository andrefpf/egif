#include <stdlib.h>
#include <stdint.h>
#include "preprocessor.h"


uint8_t * int_to_uint8(int input[], int size) {
    uint8_t * output = malloc(size * sizeof(uint8_t));

    for (int i = 0; i < size; i++) {
        output[i] = (uint8_t) input[i];
    }

    return output;
}

int * uint8_to_int(uint8_t input[], int size) {
    int * output = malloc(size * sizeof(int));

    for (int i = 0; i < size; i++) {
        output[i] = (int) input[i];
    }

    return output;
}