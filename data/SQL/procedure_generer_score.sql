CREATE DEFINER=`crabnet`@`%` PROCEDURE `generer_score`()
BEGIN 
			
			UPDATE zones_de_recuperation a SET score_total=0 WHERE score_total IS NULL;
            
            UPDATE zones_de_recuperation a
			set a.score_frequentation = (select r3.total from (select  r2.OGR_FID, sum(score) as total from
			(select r.*,p.score,
			st_intersects(r.shape,(SELECT p.poly)) as t 
			FROM zones_de_recuperation r, polygone_par_espece p
			where st_intersects(r.shape,(SELECT p.poly)) >"0") as r2
			group by r2.OGR_FID
			) as r3 where a.OGR_FID= r3.OGR_FID)  ;
            
            UPDATE zones_de_recuperation a SET score_frequentation=0 WHERE score_frequentation IS NULL;
			
            update zones_de_recuperation a
			set a.score_engins = (select r1.nb_engin from (select r.*,e.id, e.rope_length, 
			count(*) as nb_engin
			FROM zones_de_recuperation r, dfo_engins e
			where ST_WITHIN(e.position, r.SHAPE) >"0"
			group by OGR_FID) as r1 where a.OGR_FID= r1.OGR_FID);

			UPDATE zones_de_recuperation a SET score_engins=0 WHERE score_engins IS NULL;
            
			UPDATE zones_de_recuperation a
			SET a.score_total = a.score_engins WHERE a.score_frequentation =0;
			UPDATE zones_de_recuperation a
			SET a.score_total = a.score_frequentation WHERE a.score_engins =0;
			UPDATE zones_de_recuperation a
			SET a.score_total = a.score_engins * a.score_frequentation WHERE a.score_frequentation !=0 and a.score_engins!=0;

        END