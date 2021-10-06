#ifndef __EGIF_H__
#define __EGIF_H__


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
    char data[];
};

struct EgifFileFormat * create_egif(char data[], int width, int height, int frames, int colorspace);

int delete_egif(struct EgifFileFormat * egif);

#endif