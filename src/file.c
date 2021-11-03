#include <stdio.h>
#include <stdlib.h>

#include "file.h"
#include "encoding.h"

int write_egif(struct EgifFileFormat * egif, int levels, int chroma_subsampling, char * filename) {
    egif_compress(egif, levels, chroma_subsampling);

    FILE * file = fopen(filename, "wb");
    fwrite(egif, sizeof(struct EgifFileFormat) + egif->data_size, 1, file);
    fclose(file);

    return 0;
}

struct EgifFileFormat * read_egif(char * filename) {
    return 0;
}
