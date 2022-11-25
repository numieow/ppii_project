#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>
#include "dico.h"
#define min(a,b) (a<=b?a:b)

char* speciaux[] = {"°","é","è","ç","à","ê","Ê","£","ù","î","µ","§","Ô","ô"};
char clavier[8][11] = {{'1','2','3','4','5','6','7','8','9','0','+'},
                        {'&','.','"','{','(','-','.','_','.',')','='},
                        {'a','z','e','r','t','y','u','i','o','p','$'},
                        {'A','Z','E','R','T','Y','U','I','O','P','.'},
                        {'q','s','d','f','g','h','j','k','l','m','*'},
                        {'Q','S','D','F','G','H','J','K','L','M','.'},
                        {'<','w','x','c','v','b','n',',',';',':','!'},
                        {'>','W','X','C','V','B','N','?','.','/','{'}
                        };


int custom_strcmp(char* first, char* second){  
    int compte =0;
    if (calc_spec(first)!=calc_spec(second)){
        //spec_modifie(first,second);
        return 7;
    }
    int min1 = min(strlen(first),strlen(second));
    int diff = strlen(first)-strlen(second);
    compte+=2*abs(diff);
    for (int k=0;k<min1;k++){
        char cara1=first[k];
        char cara2=second[k];
        int ab1;
        int or1;
        int ab2;
        int or2;
        for(int i=0;i<8;i++){
            for(int j=0;j<11;j++){
                if (clavier[i][j]==cara1){
                    ab1=j;
                    or1= i ;
                }
                if (clavier[i][j]==cara2){
                    ab2=j;
                    or2= i ;
                }
            }
        }
        compte += 2*abs(ab1-ab2)+abs(or1-or2);
    }
    return compte;
}


table_t* dico_load(char* filename, int size) {
    table_t* dico = table_create(size);
    FILE* input = fopen(filename, "r");
    if (input != NULL) {
        char mot[100];
            while(!feof(input)) {
                fscanf(input, "%s", mot);
                //printf("%s\n", mot);
                table_add(dico, mot, mot);
            }
    }
    fclose(input);
    return dico;
}

//Sorts a string by alphabetical order
char* sort_mot(char* word) {
    char* mot = strdup(word);
    strcpy(mot, word);
    int len = strlen(mot);
    char tmp;
    for(int i = 1; i<len; i++) {
        for (int j = 0; j<(len-i); j++) {
            if(mot[j] > mot[j+1]) {
                tmp = mot[j];
                mot[j] = mot[j+1];
                mot[j+1] = tmp;
            }
        }
    }
    return mot;
}

//Checks if two words are permutations of one another
bool is_perm(char* mot1, char* mot2) {
    int len1 = strlen(mot1);
    int len2 = strlen(mot2);
    if(len1 != len2) {
        return false;
    } else {
        mot1 = sort_mot(mot1);
        mot2 = sort_mot(mot2);
        int res = strcmp(mot1, mot2);
        free(mot1);
        free(mot2);
        return res == 0;
        
    }
}

//Searches for a word different by only a permutation, ie in the same list
list_t* rech_mot1(table_t* dico, char* mot) {
    int index = table_indexof(dico, mot);
    node* check = dico->tab[index]->premier;
    list_t* mots_proches = list_create();
    bool perm;
    while(check->suivant != NULL) {
        if(strcmp(mot, check->valeur->value) == 0) {
            empty_list(mots_proches);
            list_append(mots_proches, check->valeur->value, check->valeur->value);
            return mots_proches;
        } else {
            perm = is_perm(mot, check->valeur->value);
            if(perm) {
                list_append(mots_proches, check->valeur->value, check->valeur->value);
            }
            check = check->suivant;
        }
        
    }
    return mots_proches;
}

//L'indice de la lettre A majuscule accent est 183. Si on enlève ou rajoute cette lettre à un mot, 
//il est déplacé dans la table de 183 place vers le bas ou le haut respectivement.
//Pour checker 1 erreur, on checke donc uniquement les 266 listes en-dessous ou au-dessus de celle sur laquelle
//on se trouve !

unsigned int min3(unsigned int a, unsigned int b, unsigned int c) {
    if (a < b) {
        return (a < c) ? a : c;
    } else {
        return (b < c) ? b : c;
    }
}

//Optimized version of the calculation of the Levenshtein distance
unsigned int lev(char* mot1, char* mot2) {
    unsigned int len1 = strlen(mot1);
    unsigned int len2 = strlen(mot2);
    unsigned int vieu, dernier, i, j;
    unsigned int mat[len1 + 1];
    for (j = 1; j < len1; j++) {
        mat[j] = j;
    }
    for (i = 1; i < len2; i++) {
        mat[0] = i;
        for (j = 1, dernier = i - 1; j <= len1; j++) {
            vieu = mat[j];
            mat[j] = min3(mat[j] + 1, mat[j-1] + 1, dernier + (mot1[j-1] == mot2[i-1] ? 0 : 1));
            dernier = vieu;
        }
    }
    return mat[len1];
}

int calc_spec(char* mot) {
    char* word = strdup(mot);
    int spec = 0;
    int len = strlen(word);
    int i = 0;
    while(i < len) {
        if (word[i] > 122 || word[i] < 0) {
            spec = spec + 1;
            if(i<len) {
                if(word[i+1] > 122 || word[i+1] < 0) {
                    i = i+1;
                }
            }
        }
        i = i + 1;
    }
    /*
    if(word[strlen(word) - 1] > 122 || word[strlen(word) - 1] < 0) {
        spec = spec + 1;
    }*/
    free(word);
    return (spec< 0) ? 0 : spec;
}

//Programme repris de https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
int levenshtein(char *s1, char *s2) {
    unsigned int s1len, s2len, x, y, lastdiag, olddiag;
    s1len = strlen(s1);
    s2len = strlen(s2);
    unsigned int column[s1len + 1];
    for (y = 1; y <= s1len; y++)
        column[y] = y;
    for (x = 1; x <= s2len; x++) {
        column[0] = x;
        for (y = 1, lastdiag = x - 1; y <= s1len; y++) {
            olddiag = column[y];
            column[y] = min3(column[y] + 1, column[y - 1] + 1, lastdiag + (s1[y-1] == s2[x - 1] ? 0 : 1));
            lastdiag = olddiag;
        }
    }
    int spec = calc_spec(s2);
    return column[s1len] - spec;
}

//Searches for the most similar words, with a maximum of nbop operations (permutations, deletions and additions of characters)
list_t* rech_mot(table_t* dico, char* mot, int nbop) {
    int lenmax = 184;
    int reach = nbop*lenmax;
    int index = table_indexof(dico, mot);
    list_t* mots_proches = list_create();
    int dist_min = nbop;
    int debut = (index - reach >= 0) ? index - reach : index - reach + dico->taille;
    int fin = (index + reach <= dico->taille) ? index + reach : index + reach - dico->taille;
    for(int i = debut; i < dico->taille && i < fin; i++) {
        if(!list_is_empty(dico->tab[i])) {
            node* check = dico->tab[i]->premier;
            while(check->suivant != NULL) {
                int lev1 = levenshtein(mot, check->valeur->value);
                if(lev1 <= dist_min) {
                    if(lev1 == dist_min) {
                        list_append(mots_proches, check->valeur->value, check->valeur->value);
                    } else {
                        dist_min = lev1;
                        empty_list(mots_proches);
                        list_append(mots_proches, check->valeur->value, check->valeur->value);
                    }
                }
                check = check->suivant;
            }
        }
    }
    for (int i = 0; i < fin && i < dico->taille; i++) {
        if(!list_is_empty(dico->tab[i])) {
            node* check = dico->tab[i]->premier;
            while(check->suivant != NULL) {
                int lev1 = levenshtein(mot, check->valeur->value);
                if(lev1 <= dist_min) {
                    if(lev1 == dist_min) {
                        list_append(mots_proches, check->valeur->value, check->valeur->value);
                    } else {
                        dist_min = lev1;
                        empty_list(mots_proches);
                        list_append(mots_proches, check->valeur->value, check->valeur->value);
                    }
                }
                check = check->suivant;
            }
        }
    }
    list_t* dup = anti_dup(mots_proches);
    return dup;
}

int list_length(list_t* list) {
    int res = 0;
    if(list_is_empty(list)) {
        return res;
    } else {
        node* check = list->premier;
        while(check != NULL) {
            res += 1;
            check = check->suivant;
        }
        return res;
    }
}

list_t* tri3(list_t* list, char* mot) {
    if(list_is_empty(list)) {
        return list;
    } else {
        list_t* tri = list_create();
        while(!list_is_empty(list) && list_length(tri) < 3) {
            node* check = list->premier;
            int min = custom_strcmp(check->valeur->value, mot);
            char* mot1 = calloc(1, 100);
            while(check != NULL) {
                int diff = custom_strcmp(check->valeur->value, mot);
                strcpy(mot1, check->valeur->value);
                if(diff <= min) {
                    if(diff < min) {
                        strcpy(mot1, check->valeur->value);
                        if(!list_contains(tri, mot1)) {
                            min = diff;
                        } 
                    }
                }
                check = check->suivant;
            }
            list_append(tri, mot1, mot1);
            list_sup(list, mot1);
            free(mot1);
        }
        list_destroy(list);
        return tri;
    }
}

//Filters the list previously obtained with the custom strcmp function
/*
list_t* rech_fin(table_t* dico, char* mot, int nbop) {
    printf("Tout d'abord la liste des mots proches de %s suivant Levenshtein, puis avec custom_strcmp : \n", mot);
    list_t* mots1 = rech_mot(dico, mot, nbop);
    list_print(mots1);
    list_t* fin = list_create();
    if (list_is_empty(mots1)) {
        return mots1;
    } else {
        node* check = mots1->premier;
        int min = custom_strcmp(check->valeur->value, mot);
        while (check != NULL) {
            int diff = custom_strcmp(check->valeur->value, mot);
            if(diff <= min) {
                if (diff == min) {
                    list_append(fin, check->valeur->key, check->valeur->value);
                    check = check->suivant;
                } else {
                    min = diff;
                    empty_list(fin);
                    list_append(fin, check->valeur->key, check->valeur->value);
                    check = check->suivant;
                }
            } else {
                check = check->suivant;
            }
        }
        list_destroy(mots1);
        list_print(fin);
        fin = tri3(fin);
        return fin;
    }
}
*/
list_t* rech_fin(table_t* dico, char* mot, int nbop) {
    printf("Tout d'abord la liste des mots proches de %s suivant Levenshtein, puis avec custom_strcmp : \n", mot);
    list_t* mots1 = rech_mot(dico, mot, nbop);
    list_print(mots1);
    list_t* fin = tri3(mots1, mot);
    list_print(fin);
    return fin;
}

bool has_ap(char* mot) {
    int lon = strlen(mot);
    char ap = '\'';
    for(int i = 0; i < lon; i++) {
        if(mot[i] == ap) {
            return true;
        }
    }
    return false;
}