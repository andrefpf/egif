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


inline int min(int a, int b){
    return (a < b)? a : b;
}

inline int max(int a, int b){
    return (a > b)? a : b;
}