#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "image.h"
#include "encoding.h"
#include "transformer.h"
#include "colorspaces.h"
#include "huffman.h"
#include "file.h"


int example[] = {
    1,   19,  37,  55,  73,  91,  109, 127,
    19,  37,  55,  73,  91,  109, 127, 145,
    37,  55,  73,  91,  109, 127, 145, 163,
    55,  73,  91,  109, 127, 145, 163, 181, 
    73,  91,  109, 127, 145, 163, 181, 199, 
    91,  109, 127, 145, 163, 181, 199, 217,
    109, 127, 145, 163, 181, 199, 217, 235,
    127, 145, 163, 181, 199, 217, 235, 253,
};


void print_matrix(int matrix[], int width, int height) {
    printf("[\n");
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            printf("%d \t", matrix[i*width + j]);
        }
        printf("\n");
    }
    printf("]\n");
}

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

int assert_matrices(int matrix_a[], int matrix_b[], int width, int height) {
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            if (matrix_a[i*width + j] != matrix_b[i*width + j]) {
                return 1;
            }
        }
    }
    return 0;
} 

int mse(int matrix_a[], int matrix_b[], int width, int height) {
    int tmp;
    int total = 0;

    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            tmp = (matrix_a[i*width + j] != matrix_b[i*width + j]);
            total += tmp * tmp;
        }
    }

    return total;

}

int test_compress_decompress() {
    int w = 8;
    int h = 4;
    int f = 1;

    int size = w * h * f;
    int * tst = malloc(size * sizeof(int));

    for (int i = 0; i < size; i++) {
        tst[i] = i % 256;
    }

    struct EgifFileFormat * img = create_egif(tst, w, h, f, 0);

    egif_compress(img, 4, 0);

    egif_decompress(img);

    print_matrix(tst, w, h);
    print_matrix((int *) img->data, w, h);

    return 0;
}

int test_write() {
    return 0;
}

// 4k  = 3840 x 2160
// FHD = 1920 x 1080
// HD  = 1080 x 720

int main() {
    test_compress_decompress();
    return 0;
}