#ifndef __RUN_LENGTH_ENCODE_H__
#define __RUN_LENGTH_ENCODE_H__


#include "bitarray.h"

int rle_encode(struct BitArray * array);

int rle_decode(struct BitArray * array);

#endif