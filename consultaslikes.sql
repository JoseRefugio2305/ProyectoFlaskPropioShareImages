
SELECT p.*, COUNT(*), if (p.id IN (SELECT idPub FROM reluserreaction WHERE idUser=1 AND idReaction=1),'red','black')
FROM publicacion AS p inner JOIN reluserreaction as rur ON p.id=rur.idPub
WHERE p.id_status=1 AND rur.idReaction=1 GROUP BY p.id 
UNION 
SELECT p.*,0,'black'
FROM publicacion AS p 
WHERE p.id_status=1 AND p.id NOT  IN (SELECT idPub 
						FROM reluserreaction)
UNION 					
SELECT p.*, 0,'black'
FROM publicacion AS p
WHERE p.id_status=1 AND p.id NOT IN (SELECT pp.id
							FROM publicacion AS pp inner JOIN reluserreaction as rurr ON pp.id=rurr.idPub
							WHERE pp.id_status=1 AND rurr.idReaction=1)

ORDER BY pub_date DESC;


SELECT p.*, COUNT(*) FROM publicacion AS p INNER JOIN reluserreaction AS rur ON p.id=rur.idPub WHERE rur.idReaction=1 AND p.id_status = 1 AND p.id_usuario = (SELECT id FROM usuario WHERE email='refugioriveramendoza@hotmail.com') GROUP BY p.id
UNION 
SELECT p.*,0
FROM publicacion AS p 
WHERE  p.id_usuario=1 AND p.id_status=1 AND p.id NOT  IN (SELECT idPub 
						FROM reluserreaction)
UNION 					
SELECT p.*, 0
FROM publicacion AS p
WHERE  p.id_usuario=1 AND p.id_status=1 AND p.id NOT IN (SELECT pp.id
							FROM publicacion AS pp inner JOIN reluserreaction as rurr ON pp.id=rurr.idPub
							WHERE pp.id_status=1 AND rurr.idReaction=1);
							
SELECT rcu.*, u.* FROM relusercomment AS rcu INNER JOIN usuario AS u ON rcu.iduser=u.id WHERE rcu.idpub=1;
SELECT p.*, u.* FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id WHERE p.id=1;
SELECT p.*, u.* FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id WHERE (id_status=1 OR id_status=3) AND p.id=13;


SELECT *, (SELECT COUNT(*) FROM publicacion WHERE (pub_date BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) AND  NOW()) AND id_status=1) AS conteo FROM publicacion WHERE (pub_date BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) AND  NOW()) AND id_status=1;

SELECT *, (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserseguido=1 AND isactive='1') AS Cuantoslosiguen, (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserquesigue=1 AND isactive='1') AS Acuantossigue FROM usuario WHERE id=1;

SELECT *, (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserseguido=2 AND isactive='1') AS Cuantoslosiguen, (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserquesigue=2 AND isactive='1') AS Acuantossigue, if(exists(SELECT iduserseguido FROM reluserfollowuser WHERE iduserquesigue=1 AND iduserseguido=2 AND isactive='1'),1,0) FROM usuario WHERE id=2;


SELECT * FROM reluserfollowuser WHERE iduserseguido=8 AND iduserquesigue=1;
SELECT if (1 in (select idconversacion from relmensajes), 0,1);
select iduserremitente from conversacion where iduserdestino=1;
select iduserdestino from conversacion where iduserremitente=1;
SELECT u.* FROM usuario AS u INNER JOIN reluserfollowuser AS rufu ON u.id=rufu.iduserseguido WHERE rufu.iduserquesigue=1;


SELECT u.*, s.* FROM usuario AS u INNER JOIN userplaybuscaminas AS s ON u.id=s.idplayer
ORDER BY s.dificultad,s.tiempo ASC;

SELECT u.gender,COUNT(*) FROM usuario AS u WHERE u.is_active='1'
GROUP BY u.gender;

SELECT COUNT(*) FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id WHERE u.gender LIKE 'H'
UNION ALL
SELECT COUNT(*) FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id WHERE u.gender LIKE 'M'
UNION ALL 
SELECT COUNT(*) FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id WHERE u.gender LIKE 'O'