create view possible_retrieve as SELECT distinct e.id, e.LATITUDE, e.LONGITUDE,
r.id as id_r, r.LATITUDE as LATITUDE_r, r.LONGITUDE as LONGITUDE_r,
ST_Distance_Sphere(e.position,r.position) as distance,
e.position
FROM dfo_engins e
inner join dfo_engins_recuperes r on ST_Distance_Sphere(e.position,r.position) <2000
group by e.id
order by e.id
;