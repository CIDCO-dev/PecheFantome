SELECT * FROM crabnet.zones_20X20;

alter table zones_20X20 add type_de_zone varchar(20);

UPDATE zones_20X20 a SET type_de_zone='non_protege';
                  
UPDATE zones_20X20 a
set a.type_de_zone = 'autres_restrictions' where a.OGR_FID in 
(select r.OGR_FID
FROM zones_20X20 r, zones_exclusion z
where st_intersects(r.shape,(SELECT z.shape) ) >"0");

UPDATE zones_20X20 a
set a.type_de_zone = 'dfo_zones' where a.OGR_FID in 
(select r.OGR_FID
FROM zones_20X20 r, dfo_zones d
where st_intersects(r.shape,(SELECT d.shape) ) >"0");
            

  