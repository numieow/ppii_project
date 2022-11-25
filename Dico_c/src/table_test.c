#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <stdbool.h>
#include "dico.h"

int main() {

    printf("Test de table_create : \n");
    table_t* table = table_create(10);
    printf("%lu \n", sizeof(table));

    table_add(table, "moi", "moi");
    table_add(table, "lui", "lui");
    table_add(table, "else", "else");
    table_add(table, "dragon", "dragon");
    table_add(table, "dragno", "dragno");
    table_add(table, "quest", "quest");
    table_add(table, "ouille", "ouille");
    table_add(table, "fripouille", "fripouille");
    table_add(table, "chips", "chips");
    table_add(table, "clap", "clap");
    table_add(table, "table", "table");
    table_add(table, "table", "table");
    
    printf("Test du contains : \n");
    bool b = table_contains(table, "trempette");
    bool a = table_contains(table, "dragno");
    printf("%d\n", b);
    printf("%d\n", a);

    printf("On print la table en entier : \n");
    table_print(table);

    printf("On confirme l'indice de mots dans la table: \n");
    int index_d = table_indexof(table, "dragon");
    int index_q = table_indexof(table, "quest");
    int index_l = table_indexof(table, "lui");

    printf("dragon : %d\n", index_d);
    printf("quest : %d\n", index_q);
    printf("lui : %d\n", index_l);

    printf("Tests de table_get : \n");
    char* dragon = table_get(table, "dragon");
    char* ouille = table_get(table, "ouille");

    printf("Le mot associé à dragon : %s\n", dragon);
    printf("Le mot associé à ouille : %s\n", ouille);

    table_destroy(table);

}
