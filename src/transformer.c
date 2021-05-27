#include <stdlib.h>
#include <immintrin.h>
#include "transformer.h"


void dwt(int array[], int size, int levels, int steps) {
    int half;
    int even, odd;
    int *temp = malloc(size * sizeof(int));

    for (int level = 0; level < levels; level++) {
        half = size >> (level + 1);

        // Puts even numbers in the start and odd numbers in the end 
        for (int i = 0; i < half; i++) {
            even = steps * (i*2);
            odd  = steps * (i*2 + 1);

            temp[i] = array[even];
            temp[i + half] = array[odd];
        }    

        // Puts everything in the array using SIMD (I hope)
        for (int i = 0; i < half; i++) {
            array[i] = temp[i];
            array[i + half] = temp[i + half] - temp[i];
        }
    }

    free(temp);
}

void idwt(int array[], int size, int levels, int steps) {
    int half;
    int even, odd;
    int *temp = malloc(size * sizeof(int));

    for (int level = levels; level > 0; level--) {
        half = size >> level;

        for (int i = 0; i < half; i++) {
            temp[i] = array[i];
            temp[i + half] = array[i] + array[i+half];
        }

        for (int i = 0; i < half; i++) {
            even = steps * (i*2);
            odd  = steps * (i*2 + 1);

            array[even] = temp[i];
            array[odd]  = temp[i + half];
        }
    }

    free(temp);
}