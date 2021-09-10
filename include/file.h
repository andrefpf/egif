#ifndef __EGIF_FILE_H__
#define __EGIF_FILE_H__


struct EgifFileFormat {
    char magic_number[];
    char version[];

    int  width;
    int  height;
    int  frames;
    int  colorspace;

    int  levels;
    int  downsample;

    int  data_size;
    char data[];
};


struct EgifFileFormat * compress_egif(struct Egif * egif, int levels, int downsample);

int write_egif(struct Egif * egif, FILE * file, int levels, int downsample);

struct Egif * read_egif(FILE * file);


#endif