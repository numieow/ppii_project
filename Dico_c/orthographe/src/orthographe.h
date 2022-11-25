#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#ifndef ORTHO
#define ORTHO

struct _element_t
{
    char* value;
    struct _element_t *next;
};
typedef struct _element_t element_t;

struct _table_t
{
    element_t *head;
};
typedef struct _table_t table_t;


table_t* dico(char* filename);
bool compare(table_t* dico, char* mot);
float minimum(float n, float m, float p);
float damerauL(char* mot1, char* mot2);
char* motproche(table_t* dico, char* mot);
bool list_is_empty(table_t* texte);
void list_append(table_t* texte, char* mot);
table_t* correction_t(table_t* dico, table_t* texte);

// Reste à gérer la correction d'un texte et la création d'un fichier avec le texte corriger (ou corriger directement le texte dans un fichier)

#endif