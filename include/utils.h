#ifndef __EGIF_UTILS_H__
#define __EGIF_UTILS_H__


int constrain_i(int n, int low, int high);

float constrain_f(float n, float low, float high);

int log2int(unsigned int x);

int min(int a, int b);

int max(int a, int b);

int copy_array(char from[], char to[], int size);

#endif