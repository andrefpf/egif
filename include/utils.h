#ifndef __UTILS_H__
#define __UTILS_H__

inline int constrain_i(int n, int low, int high) {
    if (n < low)
        return low;

    if (n > high)
        return high;

    return n;
}

inline float constrain_f(float n, float low, float high) {
    if (n < low)
        return low;

    if (n > high)
        return high;

    return n;
}

inline int log2int(unsigned int x )
{
  int ans = 0;
  while ( x >>= 1 ) ans++;
  return ans;
}

inline int min(int a, int b) {
    return (a < b)? a : b;
}

inline int max(int a, int b) {
    return (a > b)? a : b;
}

#endif