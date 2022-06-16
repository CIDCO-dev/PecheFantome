
DELIMITER //
CREATE TRIGGER Trig_UpdateScore_NewEngins
	AFTER insert ON dfo_engins 
    FOR EACH ROW
    
    BEGIN
		call crabnet.generer_score();
	END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER Trig_UpdateScore_Engins
	AFTER update ON dfo_engins 
    FOR EACH ROW
    
    BEGIN
		call crabnet.generer_score();
	END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER Trig_UpdateScore_poly_especes
	AFTER update ON polygone_par_espece 
    FOR EACH ROW
    
    BEGIN
		call crabnet.generer_score();
	END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER Trig_UpdateScore_NewPoly
	AFTER insert ON polygone_par_espece 
    FOR EACH ROW
    
    BEGIN
		call crabnet.generer_score();
	END //
DELIMITER ;