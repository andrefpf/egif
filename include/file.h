#ifndef __EGIF_FILE_H__
#define __EGIF_FILE_H__

#include <stdio.h>
#include "image.h"


int compress_egif(struct EgifFileFormat * egif, int levels, int chroma_subsampling);

int decompress_egif(struct EgifFileFormat * egif);

int write_egif(struct EgifFileFormat * egif, FILE * file, int levels, int chroma_subsampling);

struct EgifFileFormat * read_egif(FILE * file);

#endif