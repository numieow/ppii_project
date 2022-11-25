#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include "list.h"

int main() {

    printf("Test de création de liste :\n");
    list_t* liste = list_create();
    printf("La taille de la liste doit être non nulle : \n");
    printf("%lu \n", sizeof(liste));

    printf("Test pour list_is_empty : \n");
    printf("%d \n", list_is_empty(liste));

    printf("Test de list_append : \n");
    list_append(liste, "c", "ac");
    printf("Son seul élément est de clé c :  ");
    element_print(liste->premier->valeur);
    printf("\n");
    list_print(liste);
    printf("\nOn append a nouveau un élément, de clé a : \n");
    list_append(liste, "a", "aaaa");
    list_print(liste);

    printf("On print la liste créée précédemment : \n");
    list_print(liste);

    printf("On checke si la clé c est bien dans la liste : ");
    printf("%d\n", list_contains(liste, "c"));
    printf("On checke si la clé bonobo est bien pas dans la liste : ");
    printf("%d\n", list_contains(liste, "bonobo"));

    printf("On print la valeur associée à la clé a : %s \n", list_find(liste, "a"));

    list_print(liste);
    empty_list(liste);
    list_print(liste);

    list_destroy(liste);

}
