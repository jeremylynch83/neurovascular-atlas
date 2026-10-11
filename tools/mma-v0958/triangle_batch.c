#include <stdint.h>
#include <dlfcn.h>
typedef int (*triangle_fn)(const double*,const double*,const double*,const double*,const double*,const double*);
int vtk_triangle_batch(const char *library, const double *tri, const int64_t *a, const int64_t *b, int64_t n, uint8_t *out) {
    static triangle_fn fn = 0;
    if (!fn) {
        void *handle = dlopen(library, RTLD_NOW | RTLD_LOCAL);
        if (!handle) return -1;
        fn = (triangle_fn)dlsym(handle, "_ZN11vtkTriangle18TrianglesIntersectEPKdS1_S1_S1_S1_S1_");
        if (!fn) return -2;
    }
    for (int64_t i=0;i<n;i++) {
        const double *p=tri+9*a[i], *q=tri+9*b[i];
        out[i]=(uint8_t)(fn(p,p+3,p+6,q,q+3,q+6)!=0);
    }
    return 0;
}
