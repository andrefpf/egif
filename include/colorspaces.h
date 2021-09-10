#ifndef __COLORSPACES_H__
#define __COLORSPACES_H__


enum colorspace {
    PB    = 0,
    RGB   = 1,
    YCoCg = 2,
};


void rgb_to_ycocg(int image[], int size);

void ycocg_to_rgb(int image[], int size);

void rgb_to_ycbcr(int image[], int size);

void ycbcr_to_rgb(int image[], int size);

#endif