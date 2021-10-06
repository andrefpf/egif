#include <stdio.h>
#include <stdlib.h>

#include "image.h"
#include "transformer.h"
#include "colorspaces.h"
#include "huffman.h"
#include "file.h"


void print_array(int array[], int size) {
    printf("[");
    for (int i = 0; i < size; i++) {
        printf("%d ", array[i]);
    }
    printf("]\n\n");
}

int * create_array(int size) {  
    int *array = malloc(sizeof(int) * size);
    for (int i = 0; i < size; i++) {
        array[i] = i % 256;
    }
    return array;
}

// 4k  = 3840 x 2160
// FHD = 1920 x 1080
// HD  = 1080 x 720

int main() {
    int16_t array[10];
    int lista[10];

    for (int i = 0; i < 10; i++) {
        array[i] = i; 
        lista[i] = i;
    }
    
    printf("%ld \n", sizeof(array));
    printf("%ld \n", sizeof(lista));

    return 0;
}