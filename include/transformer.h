#ifndef __TRANSFORMER_H__
#define __TRANSFORMER_H__


int dwt(int array[], int size, int levels, int steps);

int idwt(int array[], int size, int levels, int steps);

int dwt_2d(int array[], int width, int height, int levels);

int idwt_2d(int array[], int width, int height, int levels);

int dtt(int array[], int width, int height, int frames, int levels);

int idtt(int array[], int width, int height, int frames, int levels);

int truncate(int array[], int width, int height, int details, int levels);

#endif 