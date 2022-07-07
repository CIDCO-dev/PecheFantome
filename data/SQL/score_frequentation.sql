USE crabnet;
#SELECT * FROM crabnet.polygone_par_espece;
#SELECT * FROM crabnet.zones_de_recuperation;

### PREPARATION DE LA TABLE ###
/*
alter table zones_de_recuperation
ADD score_engins int; 
alter table zones_de_recuperation
ADD score_total int;
alter table zones_de_recuperation
change field1 score_frequentation int; 
*/

###  Requete complete + inscrit le total  au score_frequentation ###

update zones_de_recuperation a
set a.score_frequentation = (select r3.total from (select  r2.OGR_FID, sum(score) as total from
(select r.*,p.score,
st_intersects(r.shape,(SELECT p.poly)) as t 
FROM zones_de_recuperation r, polygone_par_espece p
where st_intersects(r.shape,(SELECT p.poly)) >"0") as r2
group by r2.OGR_FID
) as r3 where a.OGR_FID= r3.OGR_FID)  ;


 ##### décomposition en chacune des sous-requete #####

/* Retourne toute les zones de récupération qui sont fréquenté avec le score du mammifere marin
Une ligne est retourneé pour chacun des espèce qui la fréquente
***INCLU DANS LA SÉQUENCE SUIVANTE***

select r.*,p.score,
st_intersects(r.shape,(SELECT p.poly)) as t 
FROM zones_de_recuperation r, polygone_par_espece p
where st_intersects(r.shape,(SELECT p.poly)) >"0";
*/

/* Retoune toute les zones de récupération qui sont fréquenté avec le score total des mammifere marin
Une ligne est retourneé par zones fréquentée 

select r2.OGR_FID, sum(score) as total from
(select r.*,p.score,
st_intersects(r.shape,(SELECT p.poly)) as t 
FROM zones_de_recuperation r, polygone_par_espece p
where st_intersects(r.shape,(SELECT p.poly)) >"0") as r2
group by r2.OGR_FID;
*/




