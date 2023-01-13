# Annotation-for-dl-model-procedure

1. Connexion sur le serveur tsunami via le port 3389 avec remmina ou autre logiciel qui utilise le protocol rdp
1. Télécharger les fichiers xtf via l'interface web du nas à partir du serveur tsunami ou transférer les fichiers xtf sur le serveur tsunami avec une connexion sftp
1. Convertir les fichiers xtf en image jpg
```
find PATH/RÉPERTOIRE_XTF -name "*.xtf" -exec sidescan-dump {} \;
```

4. Dans le répertoire de la mission (répertoire des fichiers xtf téléchargés)
```
mkdir xtf "1920x1080" jpg 
```
5. Déplacer les images générés à l'étape 3 dans le répertoire *jpg* créer à l'étape précédente
```
mv *.jpg jpg/
```
6. Découper les images en format 1920 X 1080 :
```
cd jpg/
for file in *; do convert $file -crop 1920x1080 ../1920x1080/$file%04d.jpg; done
```
7. Supprimmer les fragments d'images trop petits avec ce scripts : PecheFantome/src/detectordelete_bad_images.py
```
python3 delete_bad_images.py PATH
```

8. faire un backup du dernier entrainement
```
sudo cp -r /data/dataset/Ghost_Gear /data/dataset/Ghost_Gear.bak
```

9. Via la connexion rdp ouvrir un navigateur et naviguer à l'addresse http://localhost:8080
9. Entrer le nom d'utilisateur et le mot de passe pour cvat
9. Cliquer sur le bouton *Create new task* et nommer la tâche avec le numéro de mission
9. Ouvrir la tache puis cliquer sur le job ID et commencer à annotater en appuyant sur la touche *n*
9. Une fois l'annotation terminé, enregistrer puis ensuite cliquer sur *menu* => *export task dataset* et ensuite choisir le format *YOLO 1.1*
9. Télécharger et dézipper le jeu de données
9. À partir du répertoire déziper du nouveau jeu de données, transférer les labels dans le jeu de données
```
sudo mv -i obj_train_data/* /data/dataset/Ghost_Gear/data/labels/
```
16. Ajouter les nouvelles données au jeu précédent.
Dans le repertoire de la mission créer lors du téléchargements des fichiers xtf, il devrait y avoir les répertoires créés à l'étape 4
Déplacer entre 10% et 20% d'images dans le répertoire val
```
sudo mv `ls 1920x1080/ | head -NbImages` /data/dataset/Ghost_Gear/data/val/
```
Déplacer le reste des images
```
sudo mv -i 1920x1080/* /data/dataset/Ghost_Gear/data/images/
```
17. Prêt pour lancer un nouvel entrainement
```
cd /data
sudo su dany
```
./train_new.sh (résolution max) (nb epoch) (yaml path) (dataset path) (résultat path) (nom du projet)
```
./train_new.sh 1920 500 /data/dataset/Ghost_Gear/Ghost_Gear.yaml /data/train_result date_nbEpoch
```

18. Tester le model une fois l'entrainement terminé avec les images https://github.com/CIDCO-dev/OpenSidescan/tree/master/test/data/ghostfishinggear

