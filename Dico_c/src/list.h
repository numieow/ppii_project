#include <stdbool.h>

#ifndef __LIST_H__
#define __LIST_H__

struct _element_t
{
    char* key;
    char* value;
};

typedef struct _element_t element_t;

typedef struct node {
    element_t* valeur;
    struct node* suivant;
} node;

struct _list_t
{
    node* premier; 
};

typedef struct _list_t list_t;

list_t *list_create();
void list_destroy(list_t *one_list);
bool list_is_empty(list_t *one_list);
list_t* empty_list(list_t* one_list);
void list_append(list_t *one_list, char *one_key, char *one_value);
void element_print(element_t *one_element);
void list_print(list_t *one_list);
bool list_contains(list_t *one_list, char *one_key);
char *list_find(list_t *one_list, char *one_key);
list_t* anti_dup(list_t* one_list);
list_t* list_sup(list_t* list, char* mot);

#endif /* __LIST_H__ */
