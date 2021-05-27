#include <stdlib.h>
#include <immintrin.h>
#include "transformer.h"


void dwt(int array[], int size, int levels, int steps) {
    int half;
    int even, odd; // even and odd indexes of the array 
    int start, end; // first and second part of the array 
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
            start = steps * i;
            end   = steps * (i + half);

            array[start] = temp[i];
            array[end] = temp[i + half] - temp[i];
        }
    }

    free(temp);
}

void idwt(int array[], int size, int levels, int steps) {
    int half;
    int even, odd, start, end;
    int *temp = malloc(size * sizeof(int));

    for (int level = levels; level > 0; level--) {
        half = size >> level;

        for (int i = 0; i < half; i++) {
            start = steps * i;
            end   = steps * (i + half);

            temp[i] = array[start];
            temp[i + half] = array[start] + array[end];
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

void dwt_2d(int array[], int width, int height, int levels) {
    for (int i = 0; i < height; i++) {
        dwt(&array[i*width], width, levels, 1);
    }

    for (int i = 0; i < width; i++) {
        dwt(&array[i], height, levels, width);
    }
}

void idwt_2d(int array[], int width, int height, int levels) {
    for (int i = 0; i < height; i++) {
        idwt(&array[i*width], width, levels, 1);
    }

    for (int i = 0; i < width; i++) {
        idwt(&array[i], height, levels, width);
    }
}