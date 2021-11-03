#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "encoding.h"
#include "transformer.h"
#include "rle.h"
#include "huffman.h"


int egif_compress(struct EgifFileFormat * egif, int levels, int chroma_subsampling) {
    egif_dwt(egif, levels);
    egif_run_length_encode(egif);
    egif_huffman_encode(egif);
    return 0;
}

int egif_decompress(struct EgifFileFormat * egif) {
    egif_huffman_decode(egif);
    egif_run_length_decode(egif);
    egif_idwt(egif);
    return 0;
}

int egif_dwt(struct EgifFileFormat * egif, int levels) {
    int * data = (int *) egif->data;
    egif->levels = levels;

    data[0] = 0;

    #pragma omp parallel for schedule(static)
    for (int i = 0; i < egif->frames; i++) {
        dwt_2d(
            &data[i * egif->width * egif->height], 
            egif->width, 
            egif->height, 
            egif->levels
        );
    }

    dtt(
        data, 
        egif->width, 
        egif->height, 
        egif->frames, 
        egif->levels
    );

    return 0;
}

int egif_idwt(struct EgifFileFormat * egif) {
    int * data = (int *) egif->data;

    idtt(
        data, 
        egif->width, 
        egif->height, 
        egif->frames, 
        egif->levels
    );
    
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < egif->frames; i++) {
        idwt_2d(
            &data[i * egif->width * egif->height], 
            egif->width, 
            egif->height, 
            egif->levels
        );
    }

    return 0;
}

int egif_run_length_encode(struct EgifFileFormat * egif) {
    int max_size;
    struct BitArray *encoded, *decoded;

    max_size = (egif->width * egif->height * egif->frames * 3 * sizeof(int));

    decoded = create_bitarray_init(egif->data, egif->data_size, max_size);
    encoded = run_length_encode(decoded);

    egif->data_size = bitarray_size_bytes(encoded);
    memcpy((void *) egif->data, (void *) encoded->data, egif->data_size);

    delete_bitarray(encoded);
    delete_bitarray(decoded);

    return 0;
}

int egif_run_length_decode(struct EgifFileFormat * egif) {
    int max_size;
    struct BitArray *encoded, *decoded;

    max_size = (egif->width * egif->height * egif->frames * 3 * sizeof(int));

    encoded = create_bitarray_init(egif->data, egif->data_size, max_size);
    decoded = run_length_decode(encoded);

    egif->data_size = bitarray_size_bytes(decoded);
    memcpy((void *) egif->data, (void *) decoded->data, egif->data_size);

    delete_bitarray(encoded);
    delete_bitarray(decoded);

    return 0;
}

int egif_huffman_encode(struct EgifFileFormat * egif) {
    int * table;
    int max_size;
    struct BitArray *encoded, *decoded;
    
    table = create_huffman_table(egif->data, egif->data_size);
    max_size = (egif->width * egif->height * egif->frames * 3 * sizeof(int));

    decoded = create_bitarray_init(egif->data, egif->data_size, max_size);
    encoded = huffman_encode(table, decoded);

    egif->data_size = bitarray_size_bytes(encoded);
    memcpy((void *) egif->data, (void *) encoded->data, egif->data_size);
    memcpy((void *) egif->huffman_table, (void *) table, (256 * sizeof(int)));

    delete_bitarray(encoded);
    delete_bitarray(decoded);
    free(table);

    return 0;
}

int egif_huffman_decode(struct EgifFileFormat * egif) {
    int max_size;
    struct BitArray *encoded, *decoded;

    max_size = (egif->width * egif->height * egif->frames * 3 * sizeof(int));

    encoded = create_bitarray_init(egif->data, egif->data_size, max_size);
    decoded = huffman_decode(egif->huffman_table, encoded);

    egif->data_size = bitarray_size_bytes(decoded);
    memcpy((void *) egif->data, (void *) decoded->data, egif->data_size);

    delete_bitarray(encoded);
    delete_bitarray(decoded);

    return 0;
}