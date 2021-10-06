#include <stdlib.h>

#include "file.h"
#include "bitarray.h"
#include "transformer.h"
#include "rle.h"
#include "huffman.h"
#include "utils.h"


int compress_egif(struct EgifFileFormat * egif, int levels, int chroma_subsampling) {
    struct BitArray * temp;

    /* set values */
    egif->levels = levels;
    egif->chroma_subsampling = chroma_subsampling;

    /* create table */
    int * table = create_huffman_table(egif->data, egif->data_size);
    copy_array((char *) table, (char *) egif->huffman_table, 256);
    free(table);

    /* encode */
    dwt_egif(egif);
    
    /* compress */
    temp = create_bitarray_init(egif->data, egif->data_size);  

    rle_encode(temp);
    huffman_encode(egif->huffman_table, temp);

    egif->data_size = bitarray_size_bytes(temp);
    copy_array((char *) temp->data, (char *) egif->data, egif->data_size);
    delete_bitarray(temp);

    return 0;
}

int decompress_egif(struct EgifFileFormat * egif) {
    struct BitArray * temp;

    /* decompress */
    temp = create_bitarray_init(egif->data, egif->data_size);  
    huffman_decode(egif->huffman_table, temp);
    rle_decode(temp);
    egif->data_size = bitarray_size_bytes(temp);
    copy_array((char *) temp->data, (char *) egif->data, egif->data_size);
    delete_bitarray(temp);

    /* decode */
    idwt_egif(egif);

    /* set values */
    egif->levels = 0;

    return 0;
}
