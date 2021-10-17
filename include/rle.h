#ifndef __RUN_LENGTH_ENCODE_H__
#define __RUN_LENGTH_ENCODE_H__

#include "bitarray.h"


int run_length_encode(struct BitArray * array);

int run_length_decode(struct BitArray * array);

#endif