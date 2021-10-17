#include "utils.h"


int constrain(int n, int low, int high) {
    if (n < low)
        return low;

    if (n > high)
        return high;

    return n;
}

float constrain_f(float n, float low, float high) {
    if (n < low)
        return low;

    if (n > high)
        return high;

    return n;
}

int log2int(unsigned int x )
{
  int ans = 0;
  while ( x >>= 1 ) ans++;
  return ans;
}

int min(int a, int b) {
    return (a < b)? a : b;
}

int max(int a, int b) {
    return (a > b)? a : b;
}

int copy_array(char to[], char from[], int size) {
    for (int i = 0; i < size; i++) {
        to[i] = from[i];
    }
    return 0;
}
