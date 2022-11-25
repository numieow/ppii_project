#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include "dico.h"

int main() {
    double time = 0.0;
    clock_t begin = clock();
    table_t* dico = dico_load("../data/dico_fr_gutenberg.txt", 3000);
    FILE* input;
    FILE* output;
    char* mot;
    char truc;
    input = fopen("../../appweb/avant_correction.txt", "r");
    if(input != NULL) {
        output = fopen("../../appweb/apres_correction.txt", "w");
        if (output != NULL) {
            while (!feof(input)) {
                fscanf(input, "%s", mot);
                int lon = strlen(mot);
                char par = '(';
                char par2 = ')';
                char spec = ' ';
                char specd = ' ';
                char specf = ' ';

                if(mot[0] == par) {
                    specd = par;
                    mot = mot + 1;
                    lon = lon -1;
                } else if (mot[0] == '\"') {
                    specd = '\"';
                    mot = mot + 1;
                    lon = lon-1;
                }
                int test = 0;
                if ((mot[0] >='A' && mot[0] <='Z')) {
                    test = 1;
                }
                mot[0] |= 32;
                if(mot[lon-1] == ',' || mot[lon-1] == par2 || mot[lon-1] == ';' || mot[lon-1] == '.' || mot[lon-1] == ',' || mot[lon-1] == '?' || mot[lon-1] == '!' || mot[lon-1] == ':') {
                    spec = mot[lon -1];
                    mot[lon-1] = '\0';
                    lon = lon-1;
                }

                if(mot[lon-1] == '\"') {
                    specf = '\"';
                    mot[lon-1] = '\0';
                }

                if(strcmp(mot, "\n") != 0 || strcmp(mot, " ") != 0) {
                    bool connu = table_contains(dico, mot);
                    if(has_ap(mot)) {
                        fprintf(output, "%s", mot);
                    } else if(connu) {
                        if (test==1) {mot[0] = (mot[0] - 32);}
                        if(specd != ' ') {
                            fprintf(output, "%c", specd);
                        }
                        fprintf(output, "%s", mot);
                        if(specf != ' ') {
                            fprintf(output, "%c", specf);
                        }
                        if(spec != ' ') {
                            fprintf(output, "%c", spec);
                        }
                    } else {
                        list_t* fin1 = rech_fin(dico, mot, lon/3 + 1);
                        
                        if(specd != ' ') {
                                fprintf(output, "%c", specd);
                        }
                        if(list_length(fin1) == 1) {
                            fprintf(output, "%s", fin1->premier->valeur->value);
                            if(specf != ' ') {
                                fprintf(output, "%c", specf);
                            }
                        } else {
                            fprintf(output, "%c", par);
                            if(!list_is_empty(fin1)) {
                                node* check = fin1->premier;
                                while(check->suivant != NULL) {
                                    char* mot2 = check->valeur->value;
                                    fprintf(output, "%s, ",mot2);
                                    if(specf != ' ') {
                                        fprintf(output, "%c", specf);
                                    }
                                    check = check->suivant;
                                }
                                char* mot2 = check->valeur->value;
                                fprintf(output, "%s",mot2);
                            }
                            fprintf(output, "%c", par2);
                            if(specf != ' ') {
                                fprintf(output, "%c", specf);
                            }
                        }
                        if(spec != ' ') {
                            fprintf(output, "%c", spec);
                        }
                        list_destroy(fin1);
                    }
                }
                if(fscanf(input, "%c", &truc) != EOF) {
                fprintf(output, "%c", truc);
            }
            }
        } else {
            return 1;
        }
        fclose(output);
    } else {
        return 1;
    }
    fclose(input);
    clock_t end = clock();
    time += (double) (end-begin)/CLOCKS_PER_SEC;
    printf("Le temps de traitement est de %f secondes.\n", time);
    table_destroy(dico);
}
