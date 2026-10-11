#include "ufbx.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Bake complete FBX object/geometric transforms. Retain source orientation,
// convert centimetres to millimetres, then apply the recorded [0,-1620,0]
// translation. Registration is a separate, measured operation.
int main(int argc,char **argv) {
    if(argc!=4){fprintf(stderr,"source.fbx labels.tsv output-directory\n");return 2;}
    ufbx_load_opts opts={0};opts.ignore_animation=true;opts.ignore_embedded=true;
    ufbx_error error;ufbx_scene *s=ufbx_load_file(argv[1],&opts,&error);
    if(!s){char msg[1024];ufbx_format_error(msg,sizeof(msg),&error);fprintf(stderr,"%s\n",msg);return 2;}
    fprintf(stderr,"Source units %.12g metres, %zu nodes\n",s->settings.unit_meters,s->nodes.count);
    if(s->settings.unit_meters!=0.01){fprintf(stderr,"Unexpected source units\n");return 2;}
    FILE *list=fopen(argv[2],"r");char line[1024],path[2048];size_t count=0;
    while(fgets(line,sizeof(line),list)) {
        char *tab=strchr(line,'\t');if(!tab)continue;*tab=0;
        char *id=tab+1;id[strcspn(id,"\r\n")]=0;
        ufbx_node *n=NULL;
        for(size_t k=0;k<s->nodes.count;k++)if(s->nodes.data[k]->mesh && strcmp(s->nodes.data[k]->name.data,line)==0){n=s->nodes.data[k];break;}
        if(!n){fprintf(stderr,"Missing label: %s\n",line);return 2;}
        ufbx_mesh *m=n->mesh;
        snprintf(path,sizeof(path),"%s/%s.positions.f64",argv[3],id);FILE *pv=fopen(path,"wb");if(!pv)return 2;
        for(size_t k=0;k<m->num_vertices;k++) {
            ufbx_vec3 p=ufbx_transform_position(&n->geometry_to_world,m->vertices.data[k]);
            double q[3]={p.x*10.0,p.y*10.0-1620.0,p.z*10.0};fwrite(q,sizeof(double),3,pv);
        }
        fclose(pv);
        snprintf(path,sizeof(path),"%s/%s.indices.bin",argv[3],id);FILE *pf=fopen(path,"wb");if(!pf)return 2;
        size_t triangles=0;uint32_t *ix=malloc(m->max_face_triangles*3*sizeof(uint32_t));
        // Mirror transforms reverse orientation; source negative determinants
        // are accounted for once, while the registration matrix is proper.
        double det=ufbx_matrix_determinant(&n->geometry_to_world);
        for(size_t k=0;k<m->num_faces;k++) {
            uint32_t nt=ufbx_triangulate_face(ix,m->max_face_triangles*3,m,m->faces.data[k]);
            for(uint32_t t=0;t<nt;t++) {
                uint32_t f[3]={m->vertex_indices.data[ix[t*3]],m->vertex_indices.data[ix[t*3+1]],m->vertex_indices.data[ix[t*3+2]]};
                if(det<0){uint32_t tmp=f[1];f[1]=f[2];f[2]=tmp;}fwrite(f,sizeof(uint32_t),3,pf);
            }
            triangles+=nt;
        }
        fclose(pf);free(ix);count++;
        printf("%s\t%zu\t%zu\n",id,m->num_vertices,triangles);
    }
    fclose(list);ufbx_free_scene(s);fprintf(stderr,"Extracted %zu meshes\n",count);return 0;
}
