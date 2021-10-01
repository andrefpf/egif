#ifndef __TRANSFORMER_H__
#define __TRANSFORMER_H__


struct EgifFileFormat {
    char magic_number[256];
    char version[256];

    int  width;
    int  height;
    int  frames;
    int  colorspace;

    int  levels;
    int  downsample;

    int  data_size;
    char data[];
};


void dwt(int array[], int size, int levels, int steps);

void idwt(int array[], int size, int levels, int steps);

void dwt_2d(int array[], int width, int height, int levels);

void idwt_2d(int array[], int width, int height, int levels);

void dwt_3d(int array[], int width, int height, int frames, int levels);

void idwt_3d(int array[], int width, int height, int frames, int levels);

void truncate(int array[], int width, int height, int details, int levels);

void dwt_animage(struct EgifFileFormat * egif);

void idwt_animage(struct EgifFileFormat * egif);

#endif 