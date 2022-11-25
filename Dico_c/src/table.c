#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include "table.h"

int hash(char *some_value)
{
    int res = 0;
    int i = 0;

    for (i = 0; some_value[i] != '\0'; i++)
    {
        //printf("%d\n", some_value[i]);
        res = res + some_value[i];
    }
    //printf("Résultat : %d", res);
    return res;
}

table_t *table_create(int size) {
    table_t* table = calloc(1, sizeof(table_t));
    table->taille = size;
    table->tab = calloc(1, sizeof(list_t[size]));
    for (int i = 0; i < table->taille; i++) {
        table->tab[i] = list_create();
    }
    return table;
}

void table_destroy(table_t* one_table) {
    for (int i = 0; i < one_table->taille; i++) {
        list_destroy(one_table->tab[i]);
    }
    free(one_table->tab);
    free(one_table);
}

int table_indexof(table_t *one_table, char *one_key) {
    int hashage = hash(one_key);
    int modulo = one_table->taille;
    //printf("Hashage = %d\n", hashage);
    while(hashage <= 0) {
        hashage = hashage + modulo;
    }
    return hashage % modulo;
}

bool table_add(table_t* one_table, char* one_key, char* one_value) {
    int index = table_indexof(one_table, one_key);
    if(list_contains(one_table->tab[index], one_key)){
        return false;
    } else {
        list_append(one_table->tab[index], one_key, one_value);
        return true;
    }

}

void table_print(table_t* one_table) {
    printf("[");
    for(int i = 0; i<one_table->taille; i++) {
        list_print(one_table->tab[i]);
    }
    printf("]");
}

bool table_contains(table_t *one_table, char *one_key) {
    int index = table_indexof(one_table, one_key);
    return list_contains(one_table->tab[index], one_key);
}

char *table_get(table_t *one_table, char *one_key) {
    int index = table_indexof(one_table, one_key);
    return list_find(one_table->tab[index], one_key);
}
