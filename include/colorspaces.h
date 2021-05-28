#ifndef __COLORSPACES_H__
#define __COLORSPACES_H__

#include <stdint.h>

void rgb_to_ycocg(int image[], int size);

void ycocg_to_rgb(int image[], int size);

void rgb_to_ycbcr(int image[], int size);

void ycbcr_to_rgb(int image[], int size);

#endif