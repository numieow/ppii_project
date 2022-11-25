CREATE TABLE comptes (
	id_compte INTEGER PRIMARY KEY,
	nom VARCHAR NOT NULL,
	prenom VARCHAR NOT NULL,
	contact VARCHAR NOT NULL,
	password VARCHAR NOT NULL
);

CREATE TABLE projets (
	id_projet INTEGER PRIMARY KEY,
	nom VARCHAR NOT NULL,
	proprietaire INTEGER REFERENCES comptes (id_compte),
	commentaire TEXT
);

CREATE TABLE hub (
	id_hub INTEGER PRIMARY KEY,
	nom VARCHAR NOT NULL,
	projet_respo INTEGER REFERENCES projets (id_projet),
	commentaire TEXT
);

CREATE TABLE motscles_hub (
	hub INTEGER REFERENCES hub (id_hub),
	motcle VARCHAR NOT NULL,
	PRIMARY KEY (hub, motcle)
);

CREATE TABLE motscles (
	projet INTEGER REFERENCES projets (id_projet),
	motcle VARCHAR,
	PRIMARY KEY (projet, motcle)
);

CREATE TABLE IF NOT EXISTS "associations" (
	"ProjetCible"	INTEGER REFERENCES projets (id_projet),
	"ProjetDemandeur"	INTEGER REFERENCES projets (id_projet),
	"message"	TEXT,
	"statut"	INTEGER,
	PRIMARY KEY ("ProjetCible", "ProjetDemandeur")
);

CREATE TABLE membre_hub (
	id_hub INTEGER REFERENCES hub (id_hub),
	id_membre INTEGER REFERENCES projets (id_projet),
	PRIMARY KEY (id_hub, id_membre)
);


CREATE TABLE commentaires(
	id_projet INTEGER REFERENCES projets (id_projet),
	id_auteur INTEGER REFERENCES comptes (id_compte),
	id_commentaire INTEGER PRIMARY KEY,
	commentaire TEXT
);


CREATE TABLE interactions(
	id_projet INTEGER REFERENCES projets (id_projet),
	id_auteur INTEGER REFERENCES comptes (id_compte),
	type_interaction INTEGER,
	PRIMARY KEY (id_projet, id_auteur)
);

CREATE TABLE interactions_hub(
	id_hub INTEGER REFERENCES hub (id_hub),
	id_auteur INTEGER REFERENCES comptes (id_compte),
	type_interaction INTEGER,
	PRIMARY KEY (id_hub, id_auteur)
);

CREATE TABLE commentaires_hub(
	id_hub INTEGER REFERENCES hub (id_hub),
	id_auteur INTEGER REFERENCES comptes (id_compte),
	id_commentaire INTEGER PRIMARY KEY,
	commentaire TEXT
);


INSERT INTO comptes VALUES(1, 'User1', 'Test', 'exemple1@gmail.com','tncy1');
INSERT INTO comptes VALUES(2, 'User2', 'Test', 'exemple2@gmail.com','tncy2');

INSERT INTO projets VALUES(1000, "Nouveau jardin dans Nancy", 1, "Je voudrais que l'on crée un jardin participatif pour les nancéens.");
INSERT INTO projets VALUES(1001, "Plus de poubelles à Nancy", 2, "Il faudrait recycler plus, créons plus de poubelles pour le recyclage.");
INSERT INTO projets VALUES(1002, 'Panneaux informatifs pour Nancy', 1, "Pour en apprendre plus sur la ville et son histoire.");
INSERT INTO projets VALUES(1003, 'Plantations dans mon immeuble', 2, "Je voudrais que l'on crée un endroit où l'on pourrait planter des légumes avec les gens de mon immeuble");
INSERT INTO projets VALUES(1004, 'Instaurons un meilleur recyclage', 1, "Pour la planète, apprenons à plus recycler et mettons dans la ville plus de poubelles adaptées !");

INSERT INTO motscles VALUES(1002, "Culture");
INSERT INTO motscles VALUES(1000, "Environnement");
INSERT INTO motscles VALUES(1004, "Environnement");

INSERT INTO associations VALUES(1003, 1000, "Nos 2 projets se ressemblent, faisons un projet commun", 1);
INSERT INTO associations VALUES(1004,1001,"Nos intérêts se rejoignent, collaborons !", 1);

INSERT INTO hub VALUES(2000, "Plus de verdure", 1003, "Rajoutons des jardins participatifs à plusieurs endroits de la ville.");
INSERT INTO hub VALUES(2001, "Meilleur recyclage", 1004, "Installons des poubelles adaptées au recyclage de tous nos déchets partout en ville.");

INSERT INTO membre_hub VALUES(2000, 1003);
INSERT INTO membre_hub VALUES(2000, 1000);
INSERT INTO membre_hub VALUES(2001, 1004);
INSERT INTO membre_hub VALUES(2001, 1001);

INSERT INTO commentaires VALUES(1000, 2,3000,"J'aime bien ce projet !");

INSERT INTO interactions VALUES(1000, 2,1);

INSERT INTO interactions_hub VALUES(2001, 1, 1);

INSERT INTO commentaires_hub VALUES(2000, 1,4000,"J'aime bien ce hub !");