
#include <math.h>

void run(double* a, double* b, double* c, double* output) {
    for (int i = 0;  i < 10000000;  i++) {
        output[i] = (-b[i] + sqrt(b[i]*b[i] - 4*a[i]*c[i])) / (2*a[i]);
    }
}
