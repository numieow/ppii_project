#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <stdbool.h>
#include <time.h>
#include "dico.h"

int main() {
    double time = 0.0;

    //Temps de chargement entre 100 et 120sec en moyenne.
    clock_t begin = clock();
    table_t* dico = dico_load("../data/dico_fr_gutenberg.txt", 10000);
    clock_t end = clock();

    time += (double) (end-begin)/CLOCKS_PER_SEC;
    printf("Le dictionnaire s'est chargé en %f secondes.\n", time);

    //La différence d'indice entre un mot et son pluriel est de 115 !
  /*int index1 = table_indexof(dico, "zithum");
    int index2 = table_indexof(dico, "zithums");
    int delta1 = index2 - index1;
    printf("La diff d'index est de %d.\n", delta1);

    int index3 = table_indexof(dico, "empressée");
    int index4 = table_indexof(dico, "empressées");
    int delta2 = index4 - index3;
    printf("La diff d'index est de %d.\n", delta2);

    int index5 = table_indexof(dico, "massicotée");
    int index6 = table_indexof(dico, "massicotées");
    int delta3 = index6 - index5;
    printf("La diff d'index est de %d.\n", delta3);

    printf("abc-abv : %d\n", custom_strcmp("abc", "abv"));
    printf("abc-abc : %d\n", custom_strcmp("abc", "abc")); */

    //list_t* fin1 = rech_fin(dico, "coridalement", 2);
    
    int compteur = 0 ;
    int nb_mots = 0 ;

    list_t* fin1 = rech_fin(dico, "etete", 2);
    nb_mots ++ ;
    if (list_contains(fin1, "étête")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");

    list_t* fin2 = rech_fin(dico, "bnjor", 2);
    nb_mots ++ ;
    if (list_contains(fin2, "bonjour")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin3 = rech_fin(dico, "feiulle", 2);
    nb_mots ++ ;
    if (list_contains(fin3, "feuille")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin4 = rech_fin(dico, "vielle", 2);
    nb_mots ++ ;
    if (list_contains(fin4, "vieille")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin5 = rech_fin(dico, "proopse", 2);
    nb_mots ++ ;
    if (list_contains(fin5, "propose")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin6 = rech_fin(dico, "trouse", 3);
    nb_mots ++ ;
    if (list_contains(fin6, "trousse")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin7 = rech_fin(dico, "informatik", 4);
    nb_mots ++ ;
    if (list_contains(fin7, "informatique")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin8 = rech_fin(dico, "jene", 2);
    nb_mots ++ ;
    if (list_contains(fin8, "jeune")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin9 = rech_fin(dico, "ortografe", 3);
    nb_mots ++ ;
    if (list_contains(fin9, "orthographe")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


    list_t* fin10 = rech_fin(dico, "gramère", 4);
    nb_mots ++ ;
    if (list_contains(fin10, "grammaire")) {
        compteur ++ ;
    }
    else {
        printf("Le mot n'est pas dans la liste \n") ;
    }
    printf("\n");


   printf("Nombre de mots proposés : %d \n", nb_mots);
   printf("Nombre de mots trouvés : %d \n", compteur);


    list_destroy(fin1);
    list_destroy(fin2);
    list_destroy(fin3);
    list_destroy(fin4);
    list_destroy(fin5);
    list_destroy(fin6);
    list_destroy(fin7);
    list_destroy(fin8);
    list_destroy(fin9);
    list_destroy(fin10);

    table_destroy(dico);
}
