#include <stdlib.h>

#include "encoding.h"
#include "transformer.h"
#include "rle.h"
#include "huffman.h"
#include "utils.h"


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

int egif_huffman_encode(struct EgifFileFormat * egif) {
    int * table;
    struct BitArray * bitarray;
    
    table = create_huffman_table(egif->data, egif->data_size);
    copy_array((char *) egif->huffman_table, (char *) table, 256*4);
    free(table);

    bitarray = create_bitarray_init(egif->data, egif->data_size);
    huffman_encode(egif->huffman_table, bitarray);
    egif->data_size = bitarray_size_bytes(bitarray);
    copy_array(egif->data, bitarray->data, egif->data_size);
    delete_bitarray(bitarray);

    return 0;
}

int egif_huffman_decode(struct EgifFileFormat * egif) {
    struct BitArray * bitarray;

    bitarray = create_bitarray_init(egif->data, egif->data_size);
    huffman_decode(egif->huffman_table, bitarray);
    egif->data_size = bitarray_size_bytes(bitarray);
    copy_array(egif->data, bitarray->data, egif->data_size);
    delete_bitarray(bitarray);

    return 0;
}

int egif_run_length_encode(struct EgifFileFormat * egif) {
    struct BitArray * bitarray;

    bitarray = create_bitarray_init(egif->data, egif->data_size);
    run_length_encode(bitarray);
    egif->data_size = bitarray_size_bytes(bitarray);
    copy_array(egif->data, bitarray->data, egif->data_size);
    delete_bitarray(bitarray);
    
    return 0;
}

int egif_run_length_decode(struct EgifFileFormat * egif) {
    struct BitArray * bitarray;

    bitarray = create_bitarray_init(egif->data, egif->data_size);
    run_length_decode(bitarray);
    egif->data_size = bitarray_size_bytes(bitarray);
    copy_array(egif->data, bitarray->data, egif->data_size);
    delete_bitarray(bitarray);

    return 0;
}