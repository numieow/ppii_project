#include <stdbool.h>
#include "table.h"

#ifndef DICO
#define DICO

table_t* dico_load(char* filename, int size);
list_t* rech_mot1(table_t* dico, char* mot);
bool is_perm(char* mot1, char* mot2);
char* sort_mot(char* mot);
unsigned int lev(char* s1, char* s2);
int calc_spec(char* mot);
unsigned int min3(unsigned int a, unsigned int b, unsigned int c);
int levenshtein(char *s1, char *s2);
list_t* rech_mot(table_t* dico, char* mot, int nbop);
list_t* rech_fin(table_t* dico, char* mot, int nbop);
int custom_strcmp(char* first, char* second);
list_t* tri3(list_t* list, char* mot);
int list_length(list_t* list);
bool has_ap(char* mot);
#endif
