from cmath import inf
from re import M, T
from flask import Flask, render_template, request, redirect, session, flash, url_for ,jsonify,send_from_directory
from flask.helpers import make_response
from flask_session import Session
from flask_user import *
from Salad import get_response
import recherche as re
import traitement_hubs as re2
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt

import subprocess
import logging, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]="filesystem"
Session(app)


#Liste de mots-clés, empruntés à mon cerveau et au site "jeparticipe.meuse.fr"
MOTS_CLES = ["Sports et loisirs",
			 "Culture",
			 "Transition écologique",
			 "Tourisme",
			 "Mobilité",
			 "Sécurité",
			 "Education",
			 "Environnement"
			]


@app.route("/")
def index():
	'''La page index du projet. On y accède en lançant le site.
	Si l'id_session n'existe pas, on le crée à ce moment-là.
	Renvoie vers la page index.html'''
	if not session.get("id_sess"):
		session["id_sess"] = None
	return(render_template("index.html"))

@app.route("/projets-partages")
def projets_partages(tri=[None]):
	'''Affiche la page permettant de rechercher les projets créés par les utilisateurs
	avec un ou des mots-clés.
	Accédé via le topnav.'''
	if tri==[None]:
		tri = re.recherche(" ", re.lst_proj())											#Liste de tous les projets
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	liste_cur = [row for row in cur.execute('SELECT * FROM projets')]
	projets_tries = []
	proprios=[] 
	liste_hub = [row for row in cur.execute("SELECT * FROM hub")]	
	liste_membre =	[row for row in cur.execute("SELECT * FROM membre_hub")]															#Liste des str nom+prénom associé a chaque projet a la même place dans projets_trie
	for id in tri:																	#Création de la liste des projets avec leur propriétaire,
		for ele in liste_cur:
			if ele[0] == id:
				lst_comptes = [row for row in cur.execute('SELECT * FROM comptes')]
				for compte in lst_comptes:
					if compte[0]==ele[2]:
						projets_tries.append((ele,compte[1]+" "+compte[2]))				#Les éléments sont de la forme ((id_projet, nom, propriétaire, commentaire), (prénom_proprio nom_proprio))
	projets = []
	#Ajout de (id_hub, nom_hub) à chacun des projets s'ils font partie d'un hub, sinon on ajoute (False, False)
	for projet in projets_tries:
		nb_com = len(cur.execute("SELECT * FROM commentaires WHERE id_projet = ?", [projet[0][0]]).fetchall())


		id_hub_membre = cur.execute("SELECT id_hub FROM membre_hub WHERE id_membre=?", [projet[0][0]]).fetchall()
		ajout = (False, False)
		if id_hub_membre != []:
			ajout = cur.execute("SELECT id_hub, nom FROM hub WHERE id_hub=?", [id_hub_membre[0][0]]).fetchall()[0]
		(a, b) = projet
		projet = (a, b, ajout,nb_com)
		projets.append(projet)

	mots_et_nb = []
	for mot in MOTS_CLES:
		nb = len(cur.execute("SELECT * FROM motscles WHERE motcle = ?", [mot]).fetchall())
		mots_et_nb.append((mot, nb))
	#passe nombre de com en arguments:
	
	return render_template("projets-partages.html",projets=projets, liste_hub=liste_hub, liste_membre=liste_membre, mots_cles = mots_et_nb)

@app.route("/resultats-recherches", methods=["POST"])
def resultats_recherches():
	'''Route servant à l'affichage de tous les projets après un tri en fct de la recherche.
	Cette fonction effectue le tri et renvoie la liste triée vers la route projets-partages pour l'affichage'''
	mots = request.form.get("Mot")	
	cle = request.form.get("categorie")
	mot = mots.lower()													#Récupération des informations
	triés = re.recherche(mot, re.lst_proj(cle))											#Tri de tous les projets avec le/les mot(s) entré
	#con = sqlite3.connect('tables.db')
	#cur = con.cursor()
	#if cle != "":
	#	liste_cur = [row for row in cur.execute('SELECT * from projets p JOIN motscles m ON p.id_projet = m.projet WHERE motcle = ?', [cle])]
	#else:
	#	liste_cur = [row for row in cur.execute('SELECT * FROM projets')]
	
	tri = triés
	return projets_partages(tri)

@app.route("/projets-groupes")
def projets_groupes(hubs=[]):
	'''Affiche la page permettant de rechercher les hubs créés par les utilisateurs
	avec un ou des mots-clés.
	Accédé via le topnav.'''
	if hubs==[]:
		con = sqlite3.connect('tables.db')
		cur = con.cursor()
		liste_cur = [row for row in cur.execute('SELECT * FROM hub')]
		hubs=[]
		for ele in liste_cur:
			proprio=cur.execute('SELECT proprietaire FROM projets WHERE id_projet=?',(ele[2],)).fetchall()[0][0]
			info_proprio=cur.execute('SELECT * FROM comptes WHERE id_compte=?',(proprio,)).fetchall()[0]
			hubs.append([ele,info_proprio])	
			#elements de hubs de la forme [(id_hub,'nom_hub',id_proj_respo,'description'),(id_compte nom,prénom,contact)]
	return(render_template("projets-groupes.html",hubs=hubs, mots_cles = MOTS_CLES))

@app.route("/resultats-recherches_hub", methods=["POST"])
def resultats_recherches_hub():
	'''Route servant à l'affichage de tous les hubs existants selon les points donnés à chacun
	d'entre eux après notre tri (du module recherche).'''
	mots = request.form.get("Mot")														#Récupération des informations
	cle = request.form.get("categorie")
	if cle=="":
		triés = re2.recherche(mots, re2.lst_hubs())	
	else:
		triés = re2.recherche(mots, re2.filtrage_mot_cles([cle]))											#Tri de tous les hubs avec le/les mot(s) entré
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	liste_cur = [row for row in cur.execute('SELECT * FROM hub')]
	hubs_tries = []
	for id in triés:																	#Création de la liste des hubs avec leur propriétaire, toujours classés avec le tri appliqué précédemment
		for ele in liste_cur:
			if ele[0] == id:
				proprio=cur.execute('SELECT proprietaire FROM projets WHERE id_projet=?',(ele[2],)).fetchall()[0][0]
				info_proprio=cur.execute('SELECT * FROM comptes WHERE id_compte=?',(proprio,)).fetchall()[0]
				hubs_tries.append([ele,info_proprio])				#Les éléments sont de la forme [(id_hub,'nom_hub',id_proj_respo,'description'),(id_compte nom,prénom,contact)]
	return projets_groupes(hubs_tries)

@app.route("/a-propos")
def a_propos():
	'''Page à propos communes à tous ces sites, pour avoir quelques infos.
	Accédé via le topnav.'''
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	nb_projets = len(cur.execute("SELECT * FROM projets").fetchall())
	nb_hubs = len(cur.execute("SELECT * FROM hub").fetchall())
	nb_comptes = len(cur.execute("SELECT * FROM comptes").fetchall())
	return(render_template("a-propos.html", nb_projets=nb_projets, nb_hubs=nb_hubs, nb_comptes=nb_comptes))

@app.route("/mentions-legales")
def mentions_legales():
	return(render_template("mentions-legales.html"))

@app.route("/confidentialite")
def confidentialite():
	return(render_template("confidentialite.html"))

@app.route("/user_login",methods=["GET","POST"])
def login():
	'''Route amenant au login de l'utilisateur.
	Si le mot de passe ou l'identifiant est incorrect, il est redirigé vers cette même page avec un message d'erreur.
	Sinon, l'id_session est changé en l'id de l'utilisateur et la page index s'affiche.'''
	if request.method == "POST":
		mail = request.form["mail"]
		password_attendu = request.form["password"]
		con = sqlite3.connect('tables.db')
		cur = con.cursor()
		cur.execute("SELECT password FROM comptes WHERE contact = ?",(mail,))
		pswd = cur.fetchone()
		verif = sha256_crypt.verify(password_attendu,pswd[0])
		if verif :
			statement = f"SELECT * FROM comptes WHERE contact = '{mail}';"
			id = [row[0] for row in cur.execute(statement)]
			session["id_sess"]=id[0]
			return(redirect("/"))
		else :
			err = "Identfiant ou mot de passe incorrect"
			return(render_template("user-login.html",err=err))
	else :
		return(render_template("user-login.html"))

@app.route("/new_login",methods=["GET","POST"])
def new_login():
	return(render_template("new_login.html"))

@app.route("/ajout_compte",methods=["GET","POST"])
def ajout_compte():
	'''Page permettant de créer un nouveau compte, qui est rajouté dans la table compte.
	Pour le moment, on considère qu'on id_compte valide est un entier entre 1 et 999.
	Accédé via le topnav ou l'index si on n'est pas connecté.'''
	if request.method == "POST":
		nom_user = request.form.get("last_name")													#Récupération de toutes les données envoyées
		prenom_user = request.form.get("first_name")
		mail_user = request.form.get("user_mail")
		password = request.form.get("password")
		password_confirm = request.form.get("password_confirm")
		con = sqlite3.connect('tables.db')
		cur = con.cursor()
		liste_id_compte_oqp= [row [0]for row in cur.execute('SELECT id_compte FROM comptes')]	#Récupération de tous les id_compte existants
		id_nouv_compte=0
		for i in range(1,999):																	#L'id_compte qui sera attribué sera le premier nombre valide qui n'a pas déjà été attribué
			if not i in liste_id_compte_oqp and id_nouv_compte==0:
				id_nouv_compte=i
		statement = f"SELECT contact FROM comptes WHERE id_compte='{id_nouv_compte}';"
		cur.execute(statement)
		user = cur.fetchone()
		if user :
			err_mail = "Cet utilisateur existe déjà."
			return(render_template("user-login.html", err_mail=err_mail))
		if password != password_confirm :
			err_password = "Les mots de passe ne sont pas identiques."
			return(render_template("user-login.html", err_password = err_password))
		cur.execute('INSERT INTO comptes (id_compte,nom,prenom,contact,password) VALUES(?,?,?,?,?)',(id_nouv_compte,nom_user,prenom_user,mail_user,sha256_crypt.encrypt(password)))	#On insère ce nouvel utilisateur dans la table comptes																															
		con.commit()																														#Du coup le téléphone part dans le néant ??
		session["id_sess"] = id_nouv_compte														#L'utilisateur est directement connecté avec son nouveau compte
	return(redirect("/"))

@app.route("/ajout_compte_org", methods=["GET","POST"])
def ajout_compte_org():
	'''Route servant (dans le futur) à la connexion pour les organismes, tels les entreprises.'''
	if request.method == "POST":
		organisme = request.form.get("organisme")
		# whoami = request.form.get("whoami")
		mail_user = request.form.get("user_mail")
		tel_user = request.form.get("phone")
		con = sqlite3.connect('tables.db')
		cur = con.cursor()
		liste_id_org = [row[0] for row in cur.execute('SELECT id_org FROM comptes_org')]
		id_org = 0
		for i in range(3001,4000):
			if not i in liste_id_org and id_org == 0:
				id_org = i
		cur.execute('INSERT INTO comptes_org (id_org, nom_org, contact) VALUES (?,?,?)', (id_org, organisme, mail_user))
		con.commit()
		session["id_sess"] = id_org
	return(redirect("/"))

@app.route("/logout")
def logout():
	'''Route servant à la déconnexion de l'utilisateur. On repose l'id_session à None.
	Accédé via le bouton logout d'index.'''
	session["id_sess"] = None
	session.pop("id_sess",None)
	return redirect("/")

@app.route("/proposition-projet")
def proposition_projet():
	'''Route redirigeant vers la page permettant de créer un projet.
	Seul un utilisateur connecté peut créer un projet. S'il ne l'est pas, on le redirige vers
	la page de connexion/création de compte..
	Route accédée via le topnav'''
	if session['id_sess'] != None :
		return(render_template("proposition-projet.html", mots_cles = MOTS_CLES))
	else:
		err="Veuillez vous connecter avant de poursuivre"
		return(render_template("user-login.html",err=err))



def compare(fich1, fich2) :
	f = open(fich1, 'r')
	g = open(fich2, 'r')
	ch1 = f.read()
	ch2 = g.read()
	if len(ch1) != len(ch2):
		return 1
	for x in range(min(len(ch1),len(ch2))):
		if ch1[x]!=ch2[x]:
			return 1
	f.close()
	g.close()
	return 0

@app.route("/avant_correction",methods=["POST"])			
def avant_correction():
	nom_proj=request.form.get("nom_projet")
	code_proj=request.form.get("code_projet")
	description_proj=request.form.get("projet_desc")
	cat = request.form.get("categorie")
	
	with open('avant_correction.txt', 'w') as f:
		f.write(description_proj)
		f.close()
	# ON APPELLE LE CORRECTEUR EN C
	os.system("cd ../Dico_c/src ; make correction ; ./correction")
	with open('apres_correction.txt') as f:
		nouv_desc = f.read()
		f.close()

	test = "non corrige" 
	if compare('avant_correction.txt','apres_correction.txt') == 1: 
		test = "corrige" 
	return(render_template("confirmation_proposition.html",nom_projet=nom_proj,code_projet=code_proj,categorie=cat,description_sans_correction=description_proj,description_corrigée=nouv_desc,compare=test)) 




@app.route("/ajout",methods=["POST"])			
def ajout_projet():
	'''Route servant à l'ajout de projet dans la table projet, après récupération des informations
	du form de la page /proposition-projet.'''
	id_user=session['id_sess']																	#Récupération de toutes les informations
	nom_proj=request.form.get("nom_projet")
	code_proj=request.form.get("code_projet")
	description_proj=request.form.get("projet_desc")
	cat = request.form.get("categorie")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	liste_id_proj_oqp= [row [0]for row in cur.execute('SELECT id_projet FROM projets')]			#Liste des id_projets déjà pris
	id_proj=0
	for i in range(1000,2000):																	#Attribution du plus petit id_projet disponible et valide
		if not i in liste_id_proj_oqp and id_proj==0:
			id_proj=i
	cur.execute('INSERT INTO projets (id_projet,nom,proprietaire,commentaire) VALUES(?,?,?,?)',(id_proj,nom_proj,id_user,description_proj))
	cur.execute("INSERT INTO motscles (projet, motcle) VALUES(?, ?)", [id_proj, cat])			#Insertion du mot-clé dans la table
	con.commit()																				#Insertion du projet dans la table
	liste_proj_user= [row for row in cur.execute('SELECT * FROM projets WHERE proprietaire=?',(id_user,))]
	return(render_template("gestion-projet.html",Mes_projets=liste_proj_user))					#Redirection vers la page de gestion de projets avec la nouvelle liste de projets du l'utilisateur

@app.route("/suppression_projet",methods=["POST"])
def suppression_projet():
	'''Route servant à la suppression d'un projet de la table.
	On accède à cette route via le bouton "Supprimer" présent sur plusieurs pages.
	Redirige vers la page index du site.'''
	proj_a_suppr=request.form.get("proj_a_suppr")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	cur.execute('DELETE FROM membre_hub WHERE id_membre=?',(proj_a_suppr,))
	hub_dont_respo=[row for row in cur.execute('SELECT * FROM hub WHERE projet_respo=?', (proj_a_suppr,))]
	if hub_dont_respo!= []:
		hub_dont_respo=hub_dont_respo[0][0]
		nouv_respo=cur.execute('SELECT id_membre FROM membre_hub WHERE id_hub=?',(hub_dont_respo,)).fetchall()[0][0]
		cur.execute('UPDATE hub SET projet_respo = ? WHERE projet_respo=?',(nouv_respo,proj_a_suppr))
	cur.execute('DELETE FROM associations WHERE ProjetCible=? OR ProjetDemandeur=?',(proj_a_suppr,proj_a_suppr))
	cur.execute('DELETE FROM projets WHERE projets.id_projet=?',(proj_a_suppr,))
	con.commit()
	return(redirect("gestion-projet")) 

@app.route("/commentaire",methods=["POST"])
def commentaire():
	'''Route servant à l'ajout d'un commentaire sur un projet
	On accède à cette route via le bouton "commentaire" présent sur la page du projet.
	Redirige vers la page du projet d'ou on vient '''
	id_proj=request.form.get("id_proj")
	com=request.form.get("com")
	id_auteur=session["id_sess"]
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	liste_id_com_oqp= [row [0]for row in cur.execute('SELECT id_commentaire FROM commentaires')]			#Liste des id_commentaires déjà pris
	id_com=0
	for i in range(3000,4000):																	#Attribution du plus petit id_projet disponible et valide
		if not i in liste_id_com_oqp and id_com==0:
			id_com=i
	cur.execute('INSERT INTO commentaires (id_projet, id_auteur, id_commentaire, commentaire) VALUES (?,?,?,?)',(id_proj,id_auteur,id_com,com))
	con.commit()
	return(redirect('/projets/'+str(id_proj))) 

@app.route("/commentaire_hub",methods=["POST"])
def commentaire_hub():
	'''Route servant à l'ajout d'un commentaire sur un projet
	On accède à cette route via le bouton "commentaire" présent sur la page du projet.
	Redirige vers la page du projet d'ou on vient '''
	id_hub=request.form.get("id_hub")
	com=request.form.get("com")
	id_auteur=session["id_sess"]
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	liste_id_com_oqp= [row[0] for row in cur.execute('SELECT id_commentaire FROM commentaires_hub')]			#Liste des id_commentaires déjà pris
	id_com=0
	for i in range(4000,5000):																	#Attribution du plus petit id_projet disponible et valide
		if not i in liste_id_com_oqp and id_com==0:
			id_com=i
	cur.execute('INSERT INTO commentaires_hub (id_hub, id_auteur, id_commentaire, commentaire) VALUES (?,?,?,?)',(id_hub,id_auteur,id_com,com))
	con.commit()
	return(redirect('/hubs/'+str(id_hub)))

@app.route("/interaction", methods=["POST"])
def interaction():
	'''Route servant à liker ou disliker un projet.
	Si on like avec un like déjà mis de notre part, il est retiré, de même pour un dislike.
	Si on like en ayant déjà disliké, on enlève le dislike et un like est mis à la place, de même à l'inverse.
	Sinon, l'interaction est mise.'''
	id_proj = request.form.get("id_projet")
	interact = request.form.get("interact")
	auteur = session["id_sess"]
	con = sqlite3.connect("tables.db")
	cur = con.cursor()
	if interact == "pos":

		if len(cur.execute("SELECT * FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 1", [session["id_sess"], id_proj]).fetchall()) == 1:
			cur.execute("DELETE FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 1", [session["id_sess"], id_proj])
			con.commit()
			return redirect('/projets/'+str(id_proj))

		elif len(cur.execute("SELECT * FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 0", [session["id_sess"], id_proj]).fetchall()) == 1:
			cur.execute("UPDATE interactions SET type_interaction = 1 WHERE id_auteur = ? AND id_projet = ?", [session["id_sess"], id_proj])
			con.commit()
			return redirect('/projets/'+str(id_proj))
		
		else:
			cur.execute("INSERT INTO interactions VALUES(?, ?, ?)", [id_proj, auteur, 1])
			con.commit()
			return redirect('/projets/'+str(id_proj))

	if interact == "neg":

		if len(cur.execute("SELECT * FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 0", [session["id_sess"], id_proj]).fetchall()) == 1:
			cur.execute("DELETE FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 0", [session["id_sess"], id_proj])
			con.commit()
			return redirect('/projets/'+str(id_proj))

		elif len(cur.execute("SELECT * FROM interactions WHERE id_auteur = ? AND id_projet = ? AND type_interaction = 1", [session["id_sess"], id_proj]).fetchall()) == 1:
			cur.execute("UPDATE interactions SET type_interaction = 0 WHERE id_auteur = ? AND id_projet = ?", [session["id_sess"], id_proj])
			con.commit()
			return redirect('/projets/'+str(id_proj))
		
		else:
			cur.execute("INSERT INTO interactions VALUES(?, ?, ?)", [id_proj, auteur, 0])
			con.commit()
			return redirect('/projets/'+str(id_proj))

@app.route("/interaction_hub", methods=["POST"])
def interaction_hub():
	'''Route servant à liker ou disliker un hub.
	Si on like avec un like déjà mis de notre part, il est retiré, de même pour un dislike.
	Si on like en ayant déjà disliké, on enlève le dislike et un like est mis à la place, de même à l'inverse.
	Sinon, l'interaction est mise.'''
	id_hub = request.form.get("id_hub")
	interact = request.form.get("interact")
	auteur = session["id_sess"]
	con = sqlite3.connect("tables.db")
	cur = con.cursor()
	if interact == "pos":

		if len(cur.execute("SELECT * FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 1", [session["id_sess"], id_hub]).fetchall()) == 1:
			cur.execute("DELETE FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 1", [session["id_sess"], id_hub])
			con.commit()
			return redirect('/hubs/'+str(id_hub))

		elif len(cur.execute("SELECT * FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 0", [session["id_sess"], id_hub]).fetchall()) == 1:
			cur.execute("UPDATE interactions_hub SET type_interaction = 1 WHERE id_auteur = ? AND id_hub = ?", [session["id_sess"], id_hub])
			con.commit()
			return redirect('/hubs/'+str(id_hub))
		
		else:
			cur.execute("INSERT INTO interactions_hub VALUES(?, ?, ?)", [id_hub, auteur, 1])
			con.commit()
			return redirect('/hubs/'+str(id_hub))

	if interact == "neg":

		if len(cur.execute("SELECT * FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 0", [session["id_sess"], id_hub]).fetchall()) == 1:
			cur.execute("DELETE FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 0", [session["id_sess"], id_hub])
			con.commit()
			return redirect('/hubs/'+str(id_hub))

		elif len(cur.execute("SELECT * FROM interactions_hub WHERE id_auteur = ? AND id_hub = ? AND type_interaction = 1", [session["id_sess"], id_hub]).fetchall()) == 1:
			cur.execute("UPDATE interactions_hub SET type_interaction = 0 WHERE id_auteur = ? AND id_hub = ?", [session["id_sess"], id_hub])
			con.commit()
			return redirect('/hubs/'+str(id_hub))
		
		else:
			cur.execute("INSERT INTO interactions_hub VALUES(?, ?, ?)", [id_hub, auteur, 0])
			con.commit()
			return redirect('/hubs/'+str(id_hub))

@app.route('/projets/form_participation',methods=['GET','POST'])
def form_participation():
	'''Route servant à la demande d'association d'un projet et sa mise en place dans la table.
	Les informations sont récupérées via le form rempli après avoir appuyé sur le bouton "Je veux m'asocier"
	d'un projet.'''
	id_demande=request.form.get("id_demande")													#					Récupération des informations
	projet_desc=request.form.get("projet_desc")
	id_cible = request.form.get("id_cible")
	nom_cible = request.form.get("nom_cible")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	projets_valables = [row[0] for row in cur.execute("SELECT id_projet FROM projets WHERE proprietaire = ?", [session['id_sess']]).fetchall()]
	mes_projets = cur.execute("SELECT id_projet, nom FROM projets WHERE proprietaire=?", [session["id_sess"]])
	if int(id_demande) not in projets_valables:																		#Gestion de l'erreur si l'utilisateur rentre un id_projet non valide (projet inexistant, id_projet impossible ou projet qui ne lui appartient pas)
		err = "Erreur : Veuillez effectuer une demande avec un projet qui vous appartient ou qui existe."
		return render_template("form_participation.html", err = err, id_cible = id_cible, nom_cible = nom_cible, mes_projets = mes_projets)	#Redirection vers cette page avec le message d'erreur
	else: 
		cur.execute('INSERT INTO associations (ProjetCible, ProjetDemandeur, message, statut) VALUES (?,?,?,0)', (id_cible, id_demande, projet_desc))
		con.commit()
		con.close()																								#Insertion de la demande dans la table
		return(redirect("/"))


@app.route("/gestion-projet")
def gestion_projet():
	'''Route servant à l'affichage des projets de l'utilisateur connecté.
	Il peut supprimer des projets depuis cette page.
	Il peut aussi y voir les demandes d'associations à ses projets.'''
	if session['id_sess'] != None :																										#Gestion de la redirection si l'utilisateur n'est pas connecté
		con = sqlite3.connect('tables.db')
		cur = con.cursor()
#		a=cur.execute('SELECT * FROM projets WHERE proprietaire=?',session["id_sess"])
		liste_proj_user= [row for row in cur.execute('SELECT * FROM projets WHERE proprietaire=?',(session["id_sess"],))]
		liste_demande_asso = [row for row in cur.execute('SELECT ProjetDemandeur, message, ProjetCible FROM associations a JOIN projets p ON a.ProjetCible=p.id_projet AND p.proprietaire=? AND a.statut=0',(session["id_sess"],))] #la liste contient des tuples contenant uniquement les id_projets voulant s'associer. on va créer une liste plus détaillée
		liste_proj_a_asso=[]
		for demande in liste_demande_asso: 																								#Affichage de toutes les demandes
			projet=[row for row in cur.execute('SELECT * FROM projets WHERE id_projet=?',(demande[0],)).fetchall()[0]]+[demande[1]]
			nom_prenom_demandeur=cur.execute('SELECT nom,prenom FROM comptes WHERE id_compte=?',(projet[2],)).fetchall()[0]
			projet.append(nom_prenom_demandeur)
			id_nom_proj_cible=cur.execute('SELECT id_projet, nom FROM projets WHERE id_projet = ?', [demande[2]]).fetchall()[0]
			projet.append(id_nom_proj_cible)
			liste_proj_a_asso.append(projet) 																							#Les projets ont la forme [id_projet_demandeur,nom_projet_demandeur,id_proprio_demandeur,description_proj_demandeur,message_demande,(nom_demandeur,prenom_demandeur), (id_cible, nom_cible)]
		return(render_template("gestion-projet.html",Mes_projets=liste_proj_user,liste_proj_a_asso=liste_proj_a_asso))					#Redirection vers la page avec la liste des projets de l'utilisateur et de toutes les demandes d'associations
	else:
		err="Veuillez vous connecter avant de poursuivre"
		return(render_template("user-login.html",err=err))

@app.route('/projets/<string:id_proj>')
def projets_route(id_proj):
	'''Route servant à afficher la page d'un projet.
	Si l'utilisateur est le propriétaire du projet, il peut le supprimer depuis cette page également.
	Si le projet est le projet respo d'un hub qui n'est pas encore fini, la complétion du hub se fait depuis cette page.
	Sinon, l'utilisateur rpourrait laisser des commentaires/likes/dislikes, mais aussi demander de s'associer à ce projet avec l'un des siens.
	Route accédée via les liens hypertextes présents sur les noms de projets.'''
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	id = int(id_proj)
	projet = [row for row in cur.execute("SELECT * FROM projets WHERE id_projet = ?", [id])]				#Récupération des informations du projet que l'on veut voir
	id_prop = int(projet[0][2])
	prop = [row for row in cur.execute("SELECT * FROM comptes WHERE id_compte = ?", [id_prop])]				#Récupération des informations du propriétaire
	liste_demande_asso = [row for row in cur.execute('SELECT ProjetDemandeur, message, ProjetCible FROM associations a WHERE a.ProjetCible=? AND a.statut=0',(id_proj,))]	#Liste des demandes d'associations faites à ce projet
	liste_proj_a_asso=[]

	# Liste des hub ayant besoin de nom et commentaire: 
	hubs_incomplets = [row for row in cur.execute('SELECT * FROM hub WHERE projet_respo = ? AND commentaire = "NULL" AND nom = "NULL"', [id_proj]).fetchall()]
	
	for demande in liste_demande_asso: 																		#Pour chaque projet on cherche plusieurs informations :
		projetasso=[row for row in cur.execute('SELECT * FROM projets WHERE id_projet=?',(demande[0],)).fetchall()[0]]+[demande[1]]
		nom_prenom_demandeur=cur.execute('SELECT nom,prenom FROM comptes WHERE id_compte=?',(projetasso[2],)).fetchall()[0]
		projetasso.append(nom_prenom_demandeur)
		id_nom_proj_cible=cur.execute('SELECT id_projet, nom FROM projets WHERE id_projet = ?', [demande[2]]).fetchall()[0]
		projetasso.append(id_nom_proj_cible)
		liste_proj_a_asso.append(projetasso) 																# Les éléments de cette liste ont la forme[id_projet_demandeur,nom_projet_demandeur,id_proprio_demandeur,description_proj_demandeur,message_demande,(nom_demandeur,prenom_demandeur), (id_cible, nom_cible)]

	#Check pour savoir si le projet fait partie d'un hub (ou si il en est le chef)
	membre = cur.execute("SELECT * FROM membre_hub WHERE id_membre=?", [id]).fetchall()
	hub = "lol rien"
	chef = cur.execute("SELECT * FROM hub WHERE projet_respo = ?", [id]).fetchall()
	appartenance = "rien"
	if membre != []:
		hub = cur.execute("SELECT nom FROM hub WHERE id_hub = ?", [membre[0][0]]).fetchall()
		appartenance = "membre"
		if chef != []:
			appartenance = "chef"
	
	#Like et dislikes du projet :
	nb_like = len(cur.execute("SELECT * FROM interactions WHERE type_interaction = 1 AND id_projet = ?", [id]).fetchall())
	nb_dis = len(cur.execute("SELECT * FROM interactions WHERE type_interaction = 0 AND id_projet = ?", [id]).fetchall())

	#Commentaires sur ce projet :
	lst_com = cur.execute("SELECT * FROM commentaires WHERE id_projet=?", [id]).fetchall()
	lst_commentaires=[]
	for i in lst_com:
		auteur = cur.execute("SELECT * FROM comptes WHERE id_compte=?", [i[1]]).fetchall()[0]
		lst_commentaires.append([i[2], i[1], str(auteur[1])+' '+str(auteur[2]), i[3],]) 
	lst_mots = cur.execute("SELECT * from motscles WHERE projet = ?", [id]).fetchall()
	lst_mots_juste = [mot[1] for mot in lst_mots]
	print(lst_mots_juste)
	mots_manquants = []
	print(MOTS_CLES)
	for mot in MOTS_CLES:
		print(mot in lst_mots_juste)
		if not (mot in lst_mots_juste):
			mots_manquants.append(mot)								#Chaque élémment est de la forme [id_com,id_auteur,"Nom Prénom auteur","contenu_comm"]
	return render_template("page-projet.html", projet = projet, prop = prop, id_prop=id_prop,liste_proj_a_asso=liste_proj_a_asso, hubs_incomplets=hubs_incomplets, appartenance = appartenance, membre = membre, chef = chef, hub = hub,lst_commentaires=lst_commentaires, nb_like = nb_like, nb_dis = nb_dis, lst_mots = lst_mots, mots_manquants = mots_manquants)


@app.route('/hubs/<string:id_hub>')
def hubs_route(id_hub):
	'''Route redirigeant l'utilisateur vers la page d'un hub.'''
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	id = int(id_hub)
	hub = [row for row in cur.execute("SELECT * FROM hub WHERE id_hub = ?", [id])]		
	proprio=[row for row in cur.execute("SELECT * FROM comptes JOIN projets ON projets.proprietaire=comptes.id_compte WHERE id_projet = ?", [hub[0][2]])][0][:3]
	liste_id_proj_du_hub = [row for row in cur.execute('SELECT id_membre FROM membre_hub WHERE id_hub=?',(id_hub,))]	#Liste des id des projets membres
	liste_proj_du_hub=[]
	for id_proj in liste_id_proj_du_hub:
		projet=[row for row in cur.execute("SELECT * FROM projets WHERE id_projet = ?", [id_proj[0]])][0]
		liste_proj_du_hub.append(projet)
	
	nb_like = len(cur.execute("SELECT * FROM interactions_hub WHERE type_interaction = 1 AND id_hub = ?", [id]).fetchall())
	nb_dis = len(cur.execute("SELECT * FROM interactions_hub WHERE type_interaction = 0 AND id_hub = ?", [id]).fetchall())

	#Commentaires sur ce hub :
	lst_com = cur.execute("SELECT * FROM commentaires_hub WHERE id_hub=?", [id]).fetchall()
	lst_commentaires=[]
	for i in lst_com:
		auteur = cur.execute("SELECT * FROM comptes WHERE id_compte=?", [i[1]]).fetchall()[0]
		lst_commentaires.append([i[2], i[1], str(auteur[1])+' '+str(auteur[2]), i[3],]) 									#Chaque élémment est de la forme [id_com,id_auteur,"Nom Prénom auteur","contenu_comm"]
	
	return render_template("page-hub.html", hub = hub[0], proprio=proprio,liste_proj_du_hub=liste_proj_du_hub, nb_like = nb_like, nb_dis = nb_dis, lst_commentaires=lst_commentaires)


@app.route('/form_asso', methods=["POST"])
def form_asso():
	'''Route servant à l'affichage du form permettant de faire la demande d'association à un projet'''
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	id_cible =int(request.form.get("id_cible")) 													#Récupération de l'id du projet a qui est faite la demande
	#Si la demande est faite a un membre d'un hub, celle-ci doit être transférée au projet respo du hub. 
	#On va donc modifier si besoin l'id cible pour que ce soit le projet respo du hub.
	liste_id_membres_hub=[row[0] for row in cur.execute('SELECT id_membre FROM membre_hub')]
	if id_cible in liste_id_membres_hub : 															#La cible fait partie d'un hub, on transmet la demande au respo du hub
		id_cible=cur.execute('SELECT projet_respo FROM hub JOIN membre_hub ON hub.id_hub=membre_hub.id_hub WHERE membre_hub.id_membre = ?', (id_cible,)).fetchall()[0][0]
	#Si on demande de s'associer a un hub la demande est redirigée vers le projet respo
	if id_cible >= 2000 : 
		id_cible=cur.execute('SELECT projet_respo FROM hub WHERE id_hub=?',(id_cible,)).fetchall()[0][0]
	cible = [row for row in cur.execute("SELECT * FROM projets WHERE id_projet=?", [id_cible])]		#Sinon, la demande se fait naturellement vers le projet qu'on regardait auparavant.
	nom_cible = cible[0][1]
	mes_projets = cur.execute("SELECT id_projet, nom FROM projets WHERE proprietaire=?", [session["id_sess"]]).fetchall()
	projets_libres = []
	for projet in mes_projets:
		if projet[0] not in liste_id_membres_hub:
			projets_libres.append(projet)
	print(projets_libres)

	return render_template("form_participation.html", nom_cible = nom_cible, id_cible = id_cible, mes_projets = projets_libres)




@app.route("/association_refuse",methods=["POST"])
def association_refuse():
	'''Route servant à la suppression des demandes refusées de la table.
	Route accédée via le bouton de refus de la demande.
	On est redirigé vers la page d'index du site.'''
	cible=request.form.get("id_projet_cible")						#Récupération des informations
	demandeur=request.form.get("id_projet_demandeur")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	cur.execute('DELETE FROM associations WHERE associations.ProjetCible=? AND associations.ProjetDemandeur=?',(cible,demandeur))
	con.commit()													#Délétion de la demande de la table
	return(render_template("index.html"))



@app.route("/association_accepte",methods=["POST"])
def association_acceptee():
	'''Route servant à gérer l'acceptation de la demande d'association d'un projet vers un autre.
	Il faut donc créer un hub si le projet cible ne fait pas partie d'un hub, et donc insérer dans la table
	membre_hub et hub les tuples correspondants.
	Sinon, uniquement rajouter le tuplpe correspondant dans la table membre.
	Aussi, on met à jour le statut de la demande d'association dans la table associations.'''
	cible=int(request.form.get("id_projet_cible"))													#Récupération des informations
	demandeur=request.form.get("id_projet_demandeur")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	lst_projets1_des_hubs= [row[0] for row in cur.execute('SELECT projet_respo FROM hub')]

	#On cherche si le projet cible est un projet ou le projet respo d'un hub :
	if not cible in lst_projets1_des_hubs:															#On a une association entre projets simples, on va créer un hub contenant le projet cible												
		id_hub=0
		liste_id_hub_oqp=[row[0] for row in cur.execute('SELECT id_hub FROM hub')]
		for i in range(2000,3000):																	#Choix de l'id_hub le plus petit valide
			if not i in liste_id_hub_oqp and id_hub==0:
				id_hub=i
		nom_hub="NULL"
		commentaire="NULL"
		cur.execute('INSERT INTO hub (id_hub, nom, projet_respo, commentaire) VALUES (?,?,?,?)', (id_hub, nom_hub, cible,commentaire))
		con.commit()																				#Création du nouveau hub dans la table
		cur.execute('INSERT INTO membre_hub (id_hub, id_membre) VALUES (?,?)', (id_hub,cible))
		con.commit()																				#Création du tuple dans membre_hub correspondant au projet cible

	id_hub=cur.execute('SELECT id_hub FROM hub WHERE projet_respo=?',(cible,)).fetchall()[0][0] 	#On redéfinit id_hub pour qu'il ne passe pas dans le if précédent
	cur.execute('INSERT INTO membre_hub (id_hub, id_membre) VALUES (?,?)', (id_hub,demandeur))
	con.commit()																					#On met le projet demandeur dans le hub
	cur.execute('UPDATE associations SET statut=1 WHERE ProjetCible=? AND ProjetDemandeur=?', (cible,demandeur))
	con.commit()																					#On marque l'association terminée
	return(render_template("index.html")) 

@app.route("/ajout_desc_hub", methods=["POST"])
def ajout_desc_hub():
	'''Route servant à la complétion des hubs juste après création par le possesseur du projet respo.
	L'utilisateur doit alors remplir le nom du hub ainsi que sa description.
	On met à jour le hub avec ces nouvelles informations. '''
	id_hub = request.form.get("id_hub")																#Récupération des informations
	nom = request.form.get("nom_hub")
	projet_respo = request.form.get("respo")
	commentaire = request.form.get("commentaire")
	con = sqlite3.connect('tables.db')
	cur = con.cursor()
	#Changement du tuple concerné avec le vrai nom et vrai commentaire !
	cur.execute("UPDATE hub SET nom=?, commentaire=? WHERE id_hub=?", [nom, commentaire, id_hub])
	con.commit()																					#Mise à jour du hub dans la table
	return render_template("index.html")

@app.route("/user/<string:id_compte>")
def users_route(id_compte):
	'''Route reidirigeant l'utilisateur vers la page du compte d'un utilisateur.'''
	id = int(id_compte)
	con = sqlite3.connect("tables.db")
	cur = con.cursor()
	infos = cur.execute("SELECT * FROM comptes WHERE id_compte=?", [id]).fetchall()[0][:4]
	projets = cur.execute("SELECT * FROM projets WHERE proprietaire=?", [id]).fetchall()
	return render_template("page-user.html", infos = infos, projets = projets)

@app.route("/page-user")
def page_user():
	'''Redirige vers la route /user/id ou amenant l'utilisateur à se login.
	Sert dans la navbar à l'onglet "Mon compte".'''
	#Gestion de la redirection si l'utilisateur n'est pas connecté
	if session['id_sess'] != None :	
		return(redirect("/user/" + str(session["id_sess"])))																								
	else:
		err="Veuillez vous connecter avant de poursuivre"
		return(render_template("user-login.html",err=err))

@app.route("/predict",methods=["POST"])
def predict():
	text=request.get_json().get("message") #recupère a partir du  dictionnaire la valeur ayant la clé "message" donc le texte envoyé par l'user
	response = get_response(text)	#A partir de text on va créer la réponse avec le traitement dans SALAD.get_response
	message = {"answer":response}	#création de la réponse en forme json mais c'est pas encore un json
	return jsonify(message)			#transfère du message au format json

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/static/images/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 #Taille maximum des images : 16 Mo
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.context_processor		#pour pouvoir utiliser os dans les pages templates (ici pour aller chercher les images d'un certain projet)
def handle_context():
    return dict(os=os)


@app.route('/ajout_image', methods = ['POST'])
def api_root():
	'''Route ajoutant une image pour un projet quand on l'envoie.'''
	app.logger.info(PROJECT_HOME)
	if request.method == 'POST' and request.files['image']:
		app.logger.info(app.config['UPLOAD_FOLDER'])
		img=request.files['image']
		id_projet=request.form.get("id_proj")
		img_name = secure_filename(id_projet+".png")
		create_new_folder(app.config['UPLOAD_FOLDER'])
		saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
		app.logger.info("saving {}".format(saved_path))
		img.save(saved_path)
		return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
	else:
		return redirect("/")

@app.route("/supp_mot", methods = ['POST'])
def supp_mot():
	'''Route qui sert à la suppression d'un mot-clé associé à un projet.'''
	id = int(request.form.get("id_projet"))
	mot = request.form.get("mot")
	con = sqlite3.connect("tables.db")
	cur = con.cursor()
	cur.execute("DELETE FROM motscles WHERE projet = ? AND motcle = ?", [id, mot])
	con.commit()
	return(redirect('/projets/'+str(id)))

@app.route("/ajout_mot", methods = ['POST'])
def ajout_mot():
	id = int(request.form.get("id_projet"))
	mot = request.form.get("mot")
	con = sqlite3.connect("tables.db")
	cur = con.cursor()
	cur.execute("INSERT INTO motscles VALUES(?, ?)", [id, mot])
	con.commit()
	return(redirect('/projets/'+str(id)))

if __name__=="__main__":
    app.run(debug=True)