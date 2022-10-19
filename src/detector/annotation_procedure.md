# Annotation-for-dl-model-procedure

1. Connexion sur le serveur tsunami via le port 3389 avec remmina ou autre logiciel qui utilise le protocol rdp
1. Télécharger les fichiers xtf via l'interface web du nas à partir du serveur tsunami ou transférer les fichiers xtf sur le serveur tsunami avec une connexion sftp
1. Convertir les fichiers xtf en image jpg
```
find RÉPERTOIRE_XTF -name "*.xtf" -exec sidescan-dump {} \;
```

4. Dans le répertoire de la mission (répertoire des fichiers xtf téléchargés)
```
mkdir xtf "1920x1080" jpg 
```
5. Déplacer les images générés à l'étape 3 dans le répertoire *jpg* créer à l'étape précédente
```
mv *.jpg PATH/jpg/
```
6. Découper les images en format 1920 X 1080 :
```
cd PATH/jpg/
for file in *; do convert $file -crop 1920x1080 ../1920x1080/$file%04d.jpg; done
```
7. faire un backup du dernier entrainement
```
cp -r /data/dataset/Ghost_Gear /data/dataset/Ghost_Gear.bak
```

8. Via la connexion rdp ouvrir un navigateur et naviguer à l'addresse http://localhost:8080
8. Entrer le nom d'utilisateur et le mot de passe pour cvat
8. **Optionel** Dans la situation où un **projet** doit être créé : cliquer sur *projects* et puis sur *Create new Project* et créer les labels nécessaires
8. Cliquer sur le bouton *Create new task* et nommer la tâche avec le numéro de mission
8. Une fois l'annotation terminé, cliquer sur *menu* => *export task dataset* et ensuite choisir le format *YOLO 1.1*
8. Télécharger et dézipper le jeu de données
8. À partir du répertoire déziper du nouveau jeu de données, transférer les labels dans le jeu de données
```
mv -i obj_train_data/* /data/dataset/Ghost_Gear/data/labels/
```
15. Ajouter les nouvelles données au jeu précédent.
Dans le repertoire de la mission créer lors du téléchargements des fichiers xtf, il devrait y avoir les répertoires créés à l'étape 4
```
mv -i 1920x1080/* /data/dataset/Ghost_Gear/data/images/
```
16. Prêt pour lancer un nouvel entrainement
```
cd /data
sudo su dany
```
./train_new.sh (résolution max) (nb epoch) (yaml path) (dataset path) (résultat path) (nom du projet)
```
./train_new.sh 1920 500 /data/dataset/Ghost_Gear/Ghost_Gear.yaml /data/dataset/Ghost_Gear/ 20220824_500epoch
```
17. Vérifier que tout est bon : le output de ces commandes devraient être les même que ceux donné par le output de l'entrainement
```
cd /data/dataset/Ghost_Gear/data
find labels -size +0 -type f | xargs wc -l
ls images/ | wc -l
```

