#include <stdlib.h>
#include <string.h>

#include "image.h"
#include "colorspaces.h"
#include "utils.h"


struct EgifFileFormat * create_egif(int data[], int width, int height, int frames, int colorspace) {
    int size;
    struct EgifFileFormat * egif;
    
    size = width * height * frames * 4;
    if (colorspace != PB)
        size *= 3;

    egif = malloc(sizeof(struct EgifFileFormat) + size);
    strcpy(egif->magic_number, "EGIF!");
    strcpy(egif->version, "0.0.0");

    egif->width = width;
    egif->height = height;
    egif->frames = frames;
    egif->levels = 0;
    egif->colorspace = colorspace;

    egif->data_size = size;
    copy_array((char *) data, egif->data, size);
    
    return egif;
}

int delete_egif(struct EgifFileFormat * egif) {
    free(egif);
    return 0;
}