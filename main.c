#include <stdio.h>
#include <stdlib.h>

#include "transformer.h"


void print_array(int array[], int size) {
    printf("[");
    for (int i = 0; i < size; i++) {
        printf("%d ", array[i]);
    }
    printf("]\n");
}

int * create_array(int size) {  
    int *array = malloc(sizeof(int) * size);
    for (int i = 0; i < size; i++) {
        array[i] = i;
    }
    return array;
}

int main() {
    int size = 1 << 27;

    int * array = create_array(size);
    // print_array(array, size);

    dwt(array, size, 8, 1);
    // print_array(array, size);

    idwt(array, size, 8, 1);
    // print_array(array, size);

    return 0;
}