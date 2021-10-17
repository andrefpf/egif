#ifndef __TRANSFORMER_H__
#define __TRANSFORMER_H__


void dwt(int array[], int size, int levels, int steps);

void idwt(int array[], int size, int levels, int steps);

void dwt_2d(int array[], int width, int height, int levels);

void idwt_2d(int array[], int width, int height, int levels);

void dtt(int array[], int width, int height, int frames, int levels);

void idtt(int array[], int width, int height, int frames, int levels);

void truncate(int array[], int width, int height, int details, int levels);

#endif 