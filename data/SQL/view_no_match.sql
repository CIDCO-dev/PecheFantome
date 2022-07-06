CREATE VIEW `crabnet`.`no_match` AS
SELECT 
        `e`.`id`,
        `e`.`lost_date`,
        `e`.`gear` ,
        `e`.`quantity`,
        `e`.`rope_length`,
        `e`.`LONGITUDE` ,
        `e`.`LATITUDE`,
        `e`.`position`,
        `e`.`profondeur`
    FROM
        `dfo_engins` `e`
	WHERE
        `e`.`id` not IN (SELECT `m`.`id_lost` FROM `match_lost_retrieved` `m`);
        
