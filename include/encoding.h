#ifndef __EGIF_ENCODING_H__
#define __EGIF_ENCODING_H__


int egif_compress(struct EgifFileFormat * egif, int levels, int chroma_subsampling);

int egif_decompress(struct EgifFileFormat * egif);

int egif_dwt(struct EgifFileFormat * egif, int levels);

int egif_idwt(struct EgifFileFormat * egif);

int egif_huffman_encode(struct EgifFileFormat * egif);

int egif_huffman_decode(struct EgifFileFormat * egif);

int egif_run_length_encode(struct EgifFileFormat * egif);

int egif_run_length_decode(struct EgifFileFormat * egif);

#endif