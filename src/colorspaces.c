#include <stdlib.h>
#include "colorspaces.h"
#include "utils.h"


void rgb_to_ycocg(int image[], int size) {
    int tmp;
    int y, co, cg;
    int r, g, b;

    for (int i = 0; i < size; i += 3) {
        r = image[i + 0*size];
        g = image[i + 1*size];
        b = image[i + 2*size];

        co  = r - b;
        tmp = b + co/2;
        cg  = g - tmp;
        y   = tmp + cg/2;

        image[i + 0*size] = y;
        image[i + 1*size] = co;
        image[i + 2*size] = cg;
    }
}

void ycocg_to_rgb(int image[], int size) {
    int tmp;
    int y, co, cg;
    int r, g, b;

    for (int i = 0; i < size; i += 3) {
        y  = image[i + 0*size];
        co = image[i + 1*size];
        cg = image[i + 2*size];
        
        tmp = y - cg/2;
        g   = cg + tmp;
        b   = tmp - co/2;
        r   = b + co;

        image[i + 0*size] = r;
        image[i + 1*size] = g;
        image[i + 2*size] = b;
    }
}

void rgb_to_ycbcr(int image[], int size) {
    int r,g,b;
    float y,cb,cr;

    for (int i = 0; i < size; i += 3) {
        r = image[i+0];
        g = image[i+1];
        b = image[i+2];

        y  =   0 + (0.299    * r) + (0.587    * g) + (0.114    * b);
        cb = 128 - (0.168736 * r) - (0.331264 * g) + (0.5      * b);
        cr = 128 + (0.5      * r) - (0.418688 * g) - (0.081312 * b);

        y  = constrain_f(y,  0, 255);
        cb = constrain_f(cb, 0, 255);
        cr = constrain_f(cr, 0, 255);
         
        image[i+0] = (int) y;
        image[i+1] = (int) cb;
        image[i+2] = (int) cr;
    }
}

void ycbcr_to_rgb(int image[], int size) {
    int y,cb,cr;
    float r,g,b;

    for (int i = 0; i < size; i += 3) {
        y  = image[i+0];
        cb = image[i+1];
        cr = image[i+2];

        r = y + 1.402    * (cr - 128) + 2;
        g = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128);
        b = y + 1.772    * (cb - 128) + 2;

        r = constrain_f(r,  0, 255);
        g = constrain_f(g, 0, 255);
        b = constrain_f(b, 0, 255);
         
        image[i+0] = (int) r;
        image[i+1] = (int) g;
        image[i+2] = (int) b;
    }    
}
