#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include "list.h"


list_t* list_create() {
    list_t* liste = calloc(1,sizeof(node *));
    return liste;
}

void node_free(node* node) {
    free(node->valeur->value);
    free(node->valeur->key);
    free(node->valeur);
    free(node);
}

void list_destroy(list_t* one_list) {

        if(list_is_empty(one_list)) {
            free(one_list);
        } else {
            node* check = one_list->premier;
            node* temp = NULL;

            while (check->suivant != NULL) {
                temp = check;
                check = check->suivant;
                node_free(temp);
            }
            node_free(check);
            free(one_list);
        }
    
}

bool list_is_empty(list_t* one_list) {
    return one_list->premier == NULL;
}

//Empties the list without destroying it.
list_t* empty_list(list_t* one_list) {
    if(list_is_empty(one_list)) {
            return one_list;
        } else {
            node* check = one_list->premier;
            node* temp = NULL;

            while (check->suivant != NULL) {
                temp = check;
                check = check->suivant;
                node_free(temp);
            }
            node_free(check);
            one_list->premier = NULL;
            return one_list;
        }
}

void list_append(list_t* one_list, char *one_key, char *one_value) {
    node* cell = calloc(1, sizeof(node));
    element_t* ele = calloc(1, sizeof(element_t));
    ele->key = strdup(one_key);
    ele->value = strdup(one_value);
    cell->valeur = ele;
    if(list_is_empty(one_list)) {
        one_list->premier = cell;
    } else {
        node* check = one_list->premier;
        while (check->suivant != NULL) {
            check = check->suivant;
        }
        check->suivant = cell;
    }
    
}

void element_print(element_t* one_element) {
    char* key = one_element->key;
    char* value = one_element->value;
    printf("%s: %s", key, value);
}

void list_print(list_t* one_list) {
    if(list_is_empty(one_list)) {
        printf("[ ] \n");
    } else {
        node* check = one_list->premier;
        printf("[");
        while (check->suivant != NULL) {
            printf(" %s: %s,", check->valeur->key, check->valeur->value);
            check = check->suivant;
        }
        printf(" %s: %s ] \n", check->valeur->key, check->valeur->value);
    }
}

bool list_contains(list_t *one_list, char *one_key) {
    if (list_is_empty(one_list)) {
        return false;
    } else {
        node* check = one_list->premier;
        while(check != NULL) {
            int diff = strcmp(check->valeur->key, one_key);
            if(diff == 0) {
                return true;
            }
            check = check->suivant;
        }
        return false;
    }
}

char* list_find(list_t *one_list, char *one_key) {
    if (list_is_empty(one_list)) {
        return NULL;
    } else {
        node* check = one_list->premier;
        while(check != NULL) {
            int diff = strcmp(check->valeur->key, one_key);
            if(diff == 0) {
                return check->valeur->value;
            }
            check = check->suivant;
        }
        return NULL;
    }
}

list_t* anti_dup(list_t* one_list) {
    list_t* anti_dup = list_create();
    if(!list_is_empty(one_list)) {
        node* check = one_list->premier;
        while(check != NULL) {
            if(!list_contains(anti_dup, check->valeur->value)) {
                list_append(anti_dup, check->valeur->key, check->valeur->value);
            }
            check =check->suivant;
        }
    }
    list_destroy(one_list);
    return anti_dup;
}

list_t* list_sup(list_t* list, char* mot) {
    if(!list_contains(list, mot) || list_is_empty(list)) {
        return list;
    } else {
        node* check = list->premier;
        if(strcmp(check->valeur->value, mot) == 0) {
            list->premier = check->suivant;
            node_free(check);
            return list;
        } else {
            while(check->suivant->suivant != NULL) {
                if(strcmp(check->suivant->valeur->value, mot) == 0) {
                    node* tmp = check->suivant;
                    check->suivant = check->suivant->suivant;
                    node_free(tmp);
                    return list;
                }
                check = check->suivant;
            }
            if(strcmp(check->suivant->valeur->value, mot) == 0) {
                node* tmp = check->suivant;
                check->suivant = check->suivant->suivant;
                node_free(tmp);
                return list;
            } else {
                return list;
            }
        }
    }
}