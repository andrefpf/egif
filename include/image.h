#ifndef __EGIF_H__
#define __EGIF_H__


struct Egif {
    int  width;
    int  height;
    int  frames;
    int  colorspace;
    char data[];
};


struct Egif * create_egif(char data[], int width, int height, int frames, int colorspace);

#endif