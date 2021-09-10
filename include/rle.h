#ifndef __RUN_LENGTH_ENCODE_H__
#define __RUN_LENGTH_ENCODE_H__

struct BitArray * rle_encode(struct BitArray * array);

struct BitArray * rle_decode(struct BitArray * array);

#endif