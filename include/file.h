#ifndef __EGIF_FILE_H__
#define __EGIF_FILE_H__

#include <stdio.h>
#include "image.h"


int write_egif(struct EgifFileFormat * egif, int levels, int chroma_subsampling, FILE * file);

struct EgifFileFormat * read_egif(FILE * file);

#endif