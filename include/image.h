#ifndef __EGIF_IMAGE_H__
#define __EGIF_IMAGE_H__

#include "bitarray.h"


struct EgifFileFormat {
    char magic_number[256];
    char version[256];

    int  width;
    int  height;
    int  frames;
    int  colorspace;

    int  levels;
    int  chroma_subsampling;
    int  huffman_table[256];

    int  data_size;
    byte_t data[];
};

struct EgifFileFormat * create_egif(int data[], int width, int height, int frames, int colorspace);

int delete_egif(struct EgifFileFormat * egif);

#endif