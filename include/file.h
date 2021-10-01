#ifndef __EGIF_FILE_H__
#define __EGIF_FILE_H__

#include <stdio.h>

struct EgifFileFormat * compress_egif(struct EgifFileFormat * egif, int levels, int downsample);

int write_egif(struct EgifFileFormat * egif, FILE * file, int levels, int downsample);

struct EgifFileFormat * read_egif(FILE * file);


#endif