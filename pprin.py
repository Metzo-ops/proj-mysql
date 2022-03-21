import csv 
import mysql.connector
conn = mysql.connector.connect(host="localhost",user="root",password="P@ssword10", database="NOTE_EXAM")
if conn.is_connected():
    print("connexion ok")
mycursor = conn.cursor()
with open ("eleve.csv","r") as file:
    myreader = csv.DictReader(file)
    maindata = dict()
    cpt = 0
    for element in myreader:
        #print(element)
        maindata.setdefault(cpt, element)
        cpt +=1
#    print(maindata)
    for line in maindata:
#      print(line)
      dico_mat = dict()
      numero = maindata.get(line).get('Numero')
      if len(numero) != 7 or not numero.isalpha(): 
          inser_numero = "INSERT INTO ETUDIANT (numero_etudiant) VALUES (%s)" 
          val_numero = (numero,)   
          mycursor.execute(inser_numero,val_numero)             
#      print(numero)                                                   # 
      date_de_naissance = maindata.get(line).get('Date de naissance')
      date_de_naissance = date_de_naissance.replace("/","-").replace(".","-").replace("août","08").replace("34","24").replace("13","12").replace("18","08")
      inser_ddn = "INSERT INTO ETUDIANT (date_de_naissance_etudiant) VALUES (%s)"
      val_ddn = (date_de_naissance,)
      mycursor.execute(inser_ddn,val_ddn)
#      print(date_de_naissance)                                        # 
      prenom = maindata.get(line).get('Prénom')
      inser_prenom = "INSERT INTO ETUDIANT (prenom_etudiant) VALUES (%s)"
      val_prenom = (prenom,)
      mycursor.execute(inser_prenom,val_prenom)
#      print(prenom)                                                   #
      nom = maindata.get(line).get('Nom')
      inser_nom = "INSERT INTO ETUDIANT (nom_etudiant) VALUES (%s)"
      val_nom = (nom,)
      mycursor.execute(inser_nom,val_nom)
#      print(nom)                                                       #
      classe = maindata.get(line).get('Classe')
      classe = classe.replace("5eme","5iemeC").replace("6emA","")
      if classe == "6emeA" or classe =="6emeB" or classe =="6emeC" or classe == "6emeD" or classe == "5emeA" or \
          classe == "5emeB" or classe == "5emeC" or classe == "5emeD" or classe == "4emeA" or classe == "4emeB" or \
              classe == "4emeC" or classe == "4emeD" or classe == "3emeA" or classe == "3emeB" or classe =="3emeC" or classe =="3emeD":
        inser_classe = "INSERT INTO CLASSE (nom_class) VALUES (%s)"
        val_class = (classe,)
      #   mycursor.execute(inser_classe,val_class)
      mycursor.execute("SELECT id_class FROM CLASSE") 
      id_cl = [] 
      for o in mycursor.fetchall():
            ol =
     # print(id)        
      inser_id_class = "INSERT INTO ETUDIANT (id_class) VALUES (%s)"
      val_id_class = (id_cl[0],)     
      mycursor.execute(inser_id_class,val_id_class)          
#      print(classe)                                             
      note = maindata.get(line).get('Note')
#      print(note)
      note = note.split("#")
#      print(note)

      for mat in note:
        dico_note = dict()
        mat = mat.replace(']', '')
        mat = mat.split('[')
#        print(mat)
        if len(mat) == 2:
            matiere = mat[0]
#        print(matiere)
      inser_matiere = "INSERT INTO MATIERE (nom_matiere) VALUES (%s)"
      val_matiere = (matiere,)
      mycursor.execute(inser_matiere,val_matiere) 
      notes_matiere = mat[1]
      notes_matiere = notes_matiere.split(':')
#      print(notes_matiere)
      devoirs = notes_matiere[0]
#      print(devoirs)
      if len(notes_matiere) >= 2:
        compo = notes_matiere[1]
#        print(compo)                                           #
      devoirs = devoirs.split(';')
#      print(devoirs)
      dico_note.setdefault('devoirs', devoirs)
      dev = dico_note.get('devoirs')
      moyennedev = (float(dev[0])+float(dev[1]))/2
      #I WANT TO INSERT MY "MOYENNE_DEVOIR" IN MY DATABASE
      inser_dev = "INSERT INTO DEVOIR (moy_dev) VALUES (%s)"
      val_dev = (moyennedev,)
      mycursor.execute(inser_dev,val_dev)

      #I WANT TO INSERT MY "id_matiere" IN MY TABLE  "DEVOIR"
      mycursor.execute("SELECT id_matiere FROM MATIERE")
      for h in mycursor.fetchall():
            id_mat_dev = [h]
      inser_id_mat_dev = "INSERT INTO DEVOIR (id_matiere) VALUES (%s)"
      val_id_mat_dev = (id_mat_dev[0],)
      inser_obt = "INSERT INTO OBTENIR (id_matiere) VALUES (%s)"
      val_obt = (id_mat_dev[0])
      mycursor.execute(inser_id_mat_dev, val_id_mat_dev) 
      mycursor.execute(inser_obt, val_obt)

      dico_note.setdefault('compo', compo)
      note_compo = dico_note.get('compo')
      MOy = (moyennedev + 2*float(note_compo))/3
      MOy = round(MOy)
      inser_compo = "INSERT INTO OBTENIR (note_examen) VALUES (%s)"
      val_compo = (note_compo,) 
      mycursor.execute(inser_compo,val_compo)

      inser_moy_gen = "INSERT INTO OBTENIR (moyenne_generale) VALUES (%s)"
      val_moy_gen = (MOy,) 
      mycursor.execute(inser_moy_gen,val_moy_gen)

      mycursor.execute("SELECT id_etudiant FROM ETUDIANT")
      for e in mycursor.fetchall():
            id_et_obt = [e]  
      inser_id_etu_obt = "INSERT INTO OBTENIR (id_etudiant) VALUES (%s)"
      val_id_etu_obt = (id_et_obt[0],) 
      inser_id_et_pos = "INSERT INTO POSSEDER (id_etudiant) VALUES (%s)"
      val_id_etu_pos = (id_et_obt[0],)
      mycursor.execute(inser_id_et_pos, val_id_etu_pos)
      mycursor.execute(inser_id_etu_obt, val_id_etu_obt)

      mycursor.execute("SELECT id_dev FROM DEVOIR")
      for g in mycursor.fetchall():
            id_dev_pos = [g]
      inser_id_dev_pos = "INSERT INTO POSSEDER (id_dev) VALUES (%s)"
      val_id_dev_pos = (id_dev_pos[0],)
      mycursor.execute(inser_id_dev_pos, val_id_dev_pos)                
#      print(MOy)
conn.commit()
conn.close()
        