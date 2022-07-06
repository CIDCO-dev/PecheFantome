CREATE VIEW `crabnet`.`match_lost_retrieved` AS
SELECT DISTINCT
        `e`.`id` AS `id_lost`,
        `r`.`id` AS `id_retrieved`,
        (select MIN(
        ROUND(ST_DISTANCE_SPHERE(`e`.`position`, `r`.`position`),2))) AS `distance`,
        e.position
    FROM `crabnet`.`dfo_engins` `e`
        JOIN `crabnet`.`dfo_recuperes` `r` ON (ST_DISTANCE_SPHERE(`e`.`position`, `r`.`position`) < 500)
    GROUP BY `e`.`id`
    ORDER BY `e`.`id`;