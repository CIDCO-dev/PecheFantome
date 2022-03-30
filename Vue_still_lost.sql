create view still_lost as
select e.* from dfo_engins e where e.id not in
( 
SELECT id FROM possible_retrieve)
;