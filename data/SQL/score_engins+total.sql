use crabnet;
#SELECT * FROM crabnet.dfo_engins;
#SELECT * FROM zones_de_recuperation ;

/*
retourne combien d'engin ont un cordage dans chaque zone de récuperation (ORG_FID) 
***INCLU DANS LA REQUETE SUIVANTE*** 

select r.*,e.id, e.rope_length, count(*) as nb_engin_avec_corde
FROM zones_de_recuperation r, dfo_engins e
where ST_WITHIN(e.position, r.SHAPE) >"0" and e.rope_length>0
group by OGR_FID;
*/

### Attribution de 2 point par engi avec corde pour score_engins ###
update zones_de_recuperation a
set a.score_engins = (select r1.nb_engin_avec_corde from (select r.*,e.id, e.rope_length, 
count(*)*2 as nb_engin_avec_corde
FROM zones_de_recuperation r, dfo_engins e
where ST_WITHIN(e.position, r.SHAPE) >"0" and e.rope_length>0
group by OGR_FID) as r1 where a.OGR_FID= r1.OGR_FID);

### Remplacement des null par zéro pour pouvoir additionner score_total ###
UPDATE zones_de_recuperation a SET score_frequentation=0 WHERE score_frequentation IS NULL;
UPDATE zones_de_recuperation a SET score_engins=0 WHERE score_engins IS NULL;
UPDATE zones_de_recuperation a SET score_total=0 WHERE score_total IS NULL;

### Score Total ###

update zones_de_recuperation a
set a.score_total = a.score_engins where a.score_frequentation =0;

update zones_de_recuperation a
set a.score_total = a.score_engins * a.score_frequentation where a.score_frequentation !=0;
