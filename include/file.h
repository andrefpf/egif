#ifndef __EGIF_FILE_H__
#define __EGIF_FILE_H__

#include "image.h"


int write_egif(struct EgifFileFormat * egif, int levels, int chroma_subsampling, char * filename);

struct EgifFileFormat * read_egif(char * filename);

#endif