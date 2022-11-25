#include "orthographe.h"


/* Charger un dictionnaire à partir d'un fichier */ 
table_t* dico(char* filename) {
    FILE* f;
    f = fopen(filename, "r");

    int n = compte(f);
    table_t* table = table_create(n);

    char buf[100];
    int i = 0;
    while (fscanf(f,"%*s",buf)==1) {
        table_add(table, i, buf);
        i++;
    }
    return table;
}


/* Comparer un mot avec les mots du dictionnaire */
bool compare(table_t* dico, char* mot) {
    element_t* d = dico-> head;
    while(d->next != NULL) {
        if (strcmp(d->value, mot) == 0) {
            return true;
        }
        d = d -> next;
    }
    return false;
}



/* Calcul du minimum entre trois float */
float minimum(float n, float m, float p) {
    float d = n;
    if (d>m) {d = m;}
    if (d>p) {d = p;}
    return d;
}

/* Distance entre 2 chaînes de caractères Damerau-Levenshtein */
float damerauL(char* mot1, char* mot2) {
    float n1 = length(mot1);
    float n2 = length(mot2);
    int coutsub;
    int d[(int) n1 +1][(int) n2 +1];
    for (int n = 0; n < n1; n++ ) {
        for (int m = 0; m < n2; m++ ) {
            d[n][m] = 0;
        }
    }

    for (int i = 1; i < n1; i++ ) {
        for (int j = 1; i < n2; j++ ) {
            if (mot1[i]==mot2[j]) {
                coutsub = 0;
            }
            else {
                coutsub = 1;
            }
            d[i][j] = minimum(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+coutsub);
            if (i>1 && j>1 && mot1[i]==mot2[j-1] && mot1[i-1]==mot2[j]) {
                d[i][j] = minimum(d[i][j], d[i-2][j-2]+coutsub, 0);
            }
        }
        return d[(int) n1][(int) n2];
    }
}


/* Retrouver le mot le plus proche dans le dico */
char* motproche(table_t* dico, char* mot) {
    char* motp;
    int distance;
    element_t* d = dico -> head;
    distance = damerauL(d -> value, mot);
    motp = d -> value;
    d = d -> next;
    
    while(d->next != NULL) {
        if ( strcmp(d->value, mot) == 0) {
            return d -> value;
        }
        int val = damerauL(d -> value, mot);
        if (val < distance) {
            distance = val;
            motp = d -> value;
        }
        d = d -> next;
    }
    return motp;
}


/* Vérifier si une table est vide */
bool list_is_empty(table_t* texte) {
    return texte->head == NULL;
}


/* Ajouter un élément en fin de table */ 
void list_append(table_t* texte, char* mot) {
    element_t* c = calloc(1, sizeof(element_t));
    c->value = mot;
    if(list_is_empty(texte)) {
        texte->head = c;
    } else {
        element_t* check = texte->head;
        while (check->next != NULL) {
            check = check->next;
        }
        check->next = c;
    } 
}

/* Correction d'une phrase, ne gère pas les ",;.:" et les majuscules */
table_t* correction_t(table_t* dico, table_t* texte) {
    table_t* newtexte = calloc(1,sizeof(element_t*));
    element_t* t = texte -> head;
        while(t->next != NULL) {
            char* val = motproche(dico, t->value);
            list_append(newtexte, val);
            t = t -> next;
    }
}
