-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.7.24 - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para bddpinterestchafon
CREATE DATABASE IF NOT EXISTS `bddpinterestchafon` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `bddpinterestchafon`;

-- Volcando estructura para tabla bddpinterestchafon.conversacion
CREATE TABLE IF NOT EXISTS `conversacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iduserremitente` int(11) NOT NULL,
  `iduserdestino` int(11) NOT NULL,
  `fechainicio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `reluserremitente` (`iduserremitente`),
  KEY `reluserdestino` (`iduserdestino`),
  CONSTRAINT `reluserdestino` FOREIGN KEY (`iduserdestino`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reluserremitente` FOREIGN KEY (`iduserremitente`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.publicacion
CREATE TABLE IF NOT EXISTS `publicacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_title` varchar(150) NOT NULL DEFAULT 'Sin determinar',
  `pub_des` varchar(250) NOT NULL DEFAULT 'Sin descripcion',
  `url_archive` varchar(250) NOT NULL DEFAULT 'static/img/imagenotfound.png',
  `id_status` int(11) NOT NULL DEFAULT '1',
  `id_usuario` int(11) NOT NULL,
  `pub_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `StatusPublicacion` (`id_status`),
  KEY `RelUsuarioPublica` (`id_usuario`),
  CONSTRAINT `RelUsuarioPublica` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `StatusPublicacion` FOREIGN KEY (`id_status`) REFERENCES `pubstatus` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.pubstatus
CREATE TABLE IF NOT EXISTS `pubstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `statusdesc` varchar(50) NOT NULL DEFAULT 'Es un estatus',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.reactions
CREATE TABLE IF NOT EXISTS `reactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `reactiondesc` varchar(150) NOT NULL DEFAULT 'Es una reaccion',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.relmensajes
CREATE TABLE IF NOT EXISTS `relmensajes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenido` varchar(250) NOT NULL DEFAULT '',
  `idconversacion` int(11) NOT NULL,
  `idremitente` int(11) NOT NULL,
  `fechaenvio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `relmensajeconversacion` (`idconversacion`),
  KEY `relidremitente` (`idremitente`),
  CONSTRAINT `relidremitente` FOREIGN KEY (`idremitente`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relmensajeconversacion` FOREIGN KEY (`idconversacion`) REFERENCES `conversacion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.relusercomment
CREATE TABLE IF NOT EXISTS `relusercomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(250) NOT NULL,
  `idpub` int(11) NOT NULL,
  `iduser` int(11) NOT NULL,
  `isactive` varchar(2) NOT NULL DEFAULT '1',
  `comment_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `publicacion` (`idpub`),
  KEY `usuario` (`iduser`),
  CONSTRAINT `publicacion` FOREIGN KEY (`idpub`) REFERENCES `publicacion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `usuario` FOREIGN KEY (`iduser`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.reluserfollowuser
CREATE TABLE IF NOT EXISTS `reluserfollowuser` (
  `iduserseguido` int(11) NOT NULL,
  `iduserquesigue` int(11) NOT NULL,
  `isactive` varchar(2) NOT NULL DEFAULT '1',
  `datefollow` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `FK_usurarioseguido` (`iduserseguido`),
  KEY `FK_usuarioquesigue` (`iduserquesigue`),
  CONSTRAINT `FK_usuarioquesigue` FOREIGN KEY (`iduserquesigue`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_usurarioseguido` FOREIGN KEY (`iduserseguido`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.reluserreaction
CREATE TABLE IF NOT EXISTS `reluserreaction` (
  `idUser` int(11) NOT NULL,
  `idReaction` int(11) NOT NULL,
  `idPub` int(11) NOT NULL,
  KEY `usario` (`idUser`),
  KEY `reaccion` (`idReaction`),
  KEY `publicacionreaccionada` (`idPub`),
  CONSTRAINT `publicacionreaccionada` FOREIGN KEY (`idPub`) REFERENCES `publicacion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reaccion` FOREIGN KEY (`idReaction`) REFERENCES `reactions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `usario` FOREIGN KEY (`idUser`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.userroles
CREATE TABLE IF NOT EXISTS `userroles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL DEFAULT '',
  `isActive` varchar(2) NOT NULL DEFAULT '1',
  `description` varchar(50) NOT NULL DEFAULT 'Es un tipo de rol',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bddpinterestchafon.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(150) NOT NULL DEFAULT 'No especificado',
  `last_name` varchar(150) NOT NULL DEFAULT 'No especificado',
  `email` varchar(200) NOT NULL,
  `password` varchar(16) NOT NULL,
  `url_img` varchar(250) NOT NULL DEFAULT 'static/img/usernotfound.png',
  `is_active` char(2) NOT NULL DEFAULT '1',
  `id_rol` int(11) NOT NULL DEFAULT '1',
  `gender` varchar(3) NOT NULL,
  `fechanac` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `UserRol` (`id_rol`),
  CONSTRAINT `UserRol` FOREIGN KEY (`id_rol`) REFERENCES `userroles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarConversaciones
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarConversaciones`(
	IN `idusuariocon` INT











)
    COMMENT 'con este procedimeinto se obtienen todos lo mensajes del usuario'
BEGIN
	select c.*, u.*, if(c.id in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id),relmensajes.contenido,'') as contenido,
		if(c.id in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id),relmensajes.fechaenvio,'') as fechaenviomen
	from relmensajes, conversacion as c inner join usuario as u on c.iduserdestino=u.id

	where c.iduserremitente=idusuariocon and (relmensajes.id=(select max(id) from relmensajes where idconversacion=c.id) or c.id not in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id))
	
	union 
	
	select c.*, u.*, if(c.id in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id),relmensajes.contenido,'') as contenido,
	if(c.id in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id),relmensajes.fechaenvio,'') as fechaenviomen
	from relmensajes, conversacion as c inner join usuario as u on c.iduserremitente=u.id

	where c.iduserdestino=idusuariocon and (relmensajes.id=(select max(id) from relmensajes where idconversacion=c.id) or c.id not in (select idconversacion from relmensajes as rms inner join conversacion as cn on rms.idconversacion=cn.id))
	 
	order by fechaenviomen desc;
	
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarDatosUsuario
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarDatosUsuario`(
	IN `idusuarioperfil` INT


)
BEGIN
	SELECT *, 
			(SELECT COUNT(*) FROM reluserfollowuser WHERE iduserseguido=idusuarioperfil AND isactive='1') AS Cuantoslosiguen, 
			(SELECT COUNT(*) FROM reluserfollowuser WHERE iduserquesigue=idusuarioperfil AND isactive='1') AS Acuantossigue 
			FROM usuario WHERE id=idusuarioperfil and is_active='1';
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarLikesDelUsuario
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarLikesDelUsuario`(
	IN `iduserlikes` INT

)
BEGIN
SELECT p.*, u.* FROM publicacion AS p INNER JOIN reluserreaction AS rup ON rup.idPub=p.id
                            INNER JOIN usuario AS u ON p.id_usuario=u.id
                        WHERE rup.idUser=iduserlikes AND p.id_status=1 AND rup.idReaction=1 and u.is_active='1';
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarMensajesConversacion
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarMensajesConversacion`(
	IN `idconvercon` INT


)
    COMMENT 'Consulta los mensajes de una conversacion'
BEGIN
if idconvercon in (select idconversacion from relmensajes)
then 
select c.*,rms.*
from relmensajes as rms inner join conversacion as c on rms.idconversacion=c.id 
where c.id=idconvercon;
else 
select c.* from conversacion as c where c.id=idconvercon;
end if;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarOtroPerfilLogged
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarOtroPerfilLogged`(
	IN `idperfilconsultado` INT,
	IN `idusuarioueconsulta` INT

)
    COMMENT 'Este se usa cuando se esta logeado y se consulta otro perfil'
BEGIN
	SELECT *, 
                                    (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserseguido=idperfilconsultado AND isactive='1') AS Cuantoslosiguen, 
                                    (SELECT COUNT(*) FROM reluserfollowuser WHERE iduserquesigue=idperfilconsultado AND isactive='1') AS Acuantossigue, 
                                    if(exists(SELECT iduserseguido FROM reluserfollowuser WHERE iduserquesigue=idusuarioueconsulta AND iduserseguido=idperfilconsultado AND isactive='1'),1,0) 
                            FROM usuario WHERE id=idperfilconsultado and is_active='1';
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarPublicacionesDelPerfil
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarPublicacionesDelPerfil`(
	IN `idperfiluser` INT

)
BEGIN
									 SELECT p.*, COUNT(*) 
									 FROM publicacion AS p INNER JOIN reluserreaction AS rur ON p.id=rur.idPub 
									 WHERE rur.idReaction=1 AND p.id_status = 1 AND p.id_usuario = idperfiluser GROUP BY p.id
									 
                            UNION 
                            
                            SELECT p.*,0
                            FROM publicacion AS p 
                            WHERE  p.id_usuario=idperfiluser AND p.id_status=1 AND p.id NOT  IN (SELECT idPub 
                                                    FROM reluserreaction)
                            UNION 	
									 				
                            SELECT p.*, 0
                            FROM publicacion AS p
                            WHERE  p.id_usuario=idperfiluser AND p.id_status=1 AND p.id NOT IN (SELECT pp.id
                            FROM publicacion AS pp inner JOIN reluserreaction as rurr ON pp.id=rurr.idPub
                            WHERE pp.id_status=1 AND rurr.idReaction=1);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarPublicacionesInicioLog
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarPublicacionesInicioLog`(
	IN `idusuario_proc` INT


)
    COMMENT 'Funciona para mostrar las publicaciones que se muestran al inicio cuando se ha inciado sesion'
BEGIN

		  SELECT p.*, COUNT(*), if (p.id IN (SELECT idPub FROM reluserreaction WHERE idUser=idusuario_proc AND idReaction=1),1,0)
        FROM publicacion AS p inner JOIN reluserreaction as rur ON p.id=rur.idPub
        INNER JOIN usuario as u on u.id=p.id_usuario
        WHERE p.id_status=1 AND rur.idReaction=1 and u.is_active='1' GROUP BY p.id
        
        UNION 
        
		  SELECT p.*,0,0
        FROM publicacion AS p INNER JOIN usuario as u on u.id=p.id_usuario
        WHERE p.id_status=1 AND p.id NOT  IN (SELECT idPub 
                                FROM reluserreaction) and u.is_active='1'
        UNION 
		  					
        SELECT p.*, 0,0
        FROM publicacion AS p INNER JOIN usuario as u on u.id=p.id_usuario
        WHERE p.id_status=1 AND p.id NOT IN (SELECT pp.id
                                    FROM publicacion AS pp inner JOIN reluserreaction as rurr ON pp.id=rurr.idPub
                                    WHERE pp.id_status=1 AND rurr.idReaction=1)  and u.is_active='1'
        ORDER BY pub_date DESC;

END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarPublicacionesInicioNoLog
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarPublicacionesInicioNoLog`()
BEGIN
					 SELECT p.*, COUNT(*)
                FROM publicacion AS p inner JOIN reluserreaction as rur ON p.id=rur.idPub
                INNER JOIN usuario as u on u.id=p.id_usuario
                WHERE p.id_status=1 AND rur.idReaction=1 and u.is_active='1' GROUP BY p.id
                
                UNION 
                
                SELECT p.*,0
                FROM publicacion AS p INNER JOIN usuario as u on u.id=p.id_usuario
                WHERE p.id_status=1 AND p.id NOT  IN (SELECT idPub 
                                        FROM reluserreaction) and u.is_active='1'
                                        
                UNION 					
                
                SELECT p.*, 0
                FROM publicacion AS p INNER JOIN usuario as u on u.id=p.id_usuario
                WHERE p.id_status=1 AND p.id NOT IN (SELECT pp.id
                                            FROM publicacion AS pp inner JOIN reluserreaction as rurr ON pp.id=rurr.idPub
                                            WHERE pp.id_status=1 AND rurr.idReaction=1) and u.is_active='1'      
                ORDER BY pub_date DESC;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.ConsultarSeguidores
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarSeguidores`(
	IN `idusercon` INT

,
	IN `optionconsul` INT








)
BEGIN
if (optionconsul=1)
then
SELECT u.* from usuario as u inner join reluserfollowuser as ufu on u.id=ufu.iduserquesigue where ufu.iduserseguido=idusercon  and 
u.id not in (select iduserdestino from conversacion where iduserremitente=idusercon) 
and u.id not in (select iduserremitente from conversacion where iduserdestino=idusercon);
else
SELECT u.* from usuario as u inner join reluserfollowuser as ufu on u.id=ufu.iduserseguido where ufu.iduserquesigue=idusercon and 
u.id not in (select iduserdestino from conversacion where iduserremitente=idusercon) 
and u.id not in (select iduserremitente from conversacion where iduserdestino=idusercon);
end if;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.CREATEconversacion
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `CREATEconversacion`(
	IN `idremiten` INT,
	IN `iddest` INT


)
BEGIN
	if idremiten not in (select iduserremitente from conversacion where iduserremitente=idremiten and iduserdestino=iddest) and idremiten not in (select iduserdestino from conversacion where iduserremitente=iddest and iduserdestino=idremiten)
	then
	INSERT INTO conversacion (iduserremitente, iduserdestino) values(idremiten,iddest);
	end if;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTcomment
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTcomment`(
	IN `comentario` VARCHAR(250),
	IN `idpublic` INT,
	IN `idusercomment` INT
)
BEGIN
INSERT INTO relusercomment (comment, idpub, iduser) VALUES(comentario, idpublic,idusercomment);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTfollow
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTfollow`(
	IN `is_active` VARCHAR(2),
	IN `idseguido` INT,
	IN `idquesigue` INT
)
BEGIN
INSERT INTO reluserfollowuser (iduserseguido, iduserquesigue, isactive) VALUES (idseguido, idquesigue, is_active);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTmessage
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTmessage`(
	IN `contmessage` VARCHAR(250),
	IN `idconvcon` INT,
	IN `idurem` INT


)
    COMMENT 'insertar un mensaje e una conversacion '
BEGIN
	INSERT INTO relmensajes (contenido, idconversacion, idremitente)
	VALUES (contmessage, idconvcon, idurem);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTnuevousuario
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTnuevousuario`(
	IN `firstname` VARCHAR(150),
	IN `lastname` VARCHAR(150),
	IN `newemail` VARCHAR(200),
	IN `pass` VARCHAR(16),
	IN `newgender` VARCHAR(3),
	IN `newfechanac` DATE


)
BEGIN
	INSERT INTO usuario (first_name, last_name, email, password, gender, fechanac) VALUES (firstname, lastname, newemail, pass, newgender, newfechanac);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTpublication
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTpublication`(
	IN `pubtitle` VARCHAR(150),
	IN `pubdesc` VARCHAR(250),
	IN `urlarchive` VARCHAR(250),
	IN `idstatus` INT,
	IN `iduser` INT


)
BEGIN
		  INSERT INTO publicacion (pub_title, pub_des, url_archive, id_status, id_usuario) 
        VALUES(pubtitle, pubdesc, urlarchive, idstatus,iduser);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.INSERTreaccion
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERTreaccion`(
	IN `idusertor` INT,
	IN `reaccion` INT,
	IN `idpublic` INT
)
BEGIN
	INSERT INTO reluserreaction (idUser, idReaction, idPub) VALUES (idusertor, reaccion, idpublic);
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.PrivatePubs
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `PrivatePubs`(
	IN `idusuario` INT
)
    COMMENT 'Obtener las publicaciones privadas de un usuario'
BEGIN
	SELECT * FROM publicacion WHERE id_status=3 AND id_usuario=idusuario;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.PublicacionesRelevantes
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `PublicacionesRelevantes`()
BEGIN
	SELECT * FROM publicacion inner join usuario as u on publicacion.id_usuario=u.id
	WHERE (pub_date BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) AND  NOW()) AND id_status=1 and u.is_active='1';
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.PublicationComments
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `PublicationComments`(
	IN `idpublic` INT
)
BEGIN
	SELECT rcu.*, u.* FROM relusercomment AS rcu INNER JOIN usuario AS u ON rcu.iduser=u.id WHERE rcu.idpub=idpublic;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.seePublication
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `seePublication`(
	IN `idpublic` INT

)
BEGIN
SELECT p.*, u.*
    FROM publicacion AS p INNER JOIN usuario AS u ON p.id_usuario=u.id 
    WHERE (id_status=1 OR id_status=3) AND p.id=idpublic;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.UPDATEfollow
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UPDATEfollow`(
	IN `is_active` VARCHAR(2),
	IN `idseguido` INT,
	IN `idquesigue` INT
)
BEGIN
	UPDATE reluserfollowuser 
	SET isactive=is_active
	WHERE iduserseguido=idseguido AND iduserquesigue=idquesigue;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.UPDATEpublication
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UPDATEpublication`(
	IN `pubtitle` VARCHAR(150),
	IN `pubdesc` VARCHAR(250),
	IN `urlarchive` VARCHAR(250),
	IN `idpublic` INT
)
BEGIN
	UPDATE publicacion
                        SET
                            pub_title=pubtitle,
                            pub_des=pubdesc,
                            url_archive=urlarchive
                        WHERE id=idpublic;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.UPDATEreaccion
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UPDATEreaccion`(
	IN `reaccion` INT
,
	IN `idpublic` INT,
	IN `idusertor` INT

)
BEGIN
					 UPDATE reluserreaction
                SET
                    idReaction=reaccion
                WHERE idPub =idpublic AND idUser=idusertor;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.UPDATEstatusPublication
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UPDATEstatusPublication`(
	IN `idstatus` INT,
	IN `idpublic` INT
)
BEGIN
UPDATE publicacion SET id_status=idstatus WHERE id=idpublic;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bddpinterestchafon.UPDATEuser
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UPDATEuser`(
	IN `firstname` VARCHAR(150),
	IN `lastname` VARCHAR(150),
	IN `newemail` VARCHAR(200)
,
	IN `pass` VARCHAR(16),
	IN `urlim` VARCHAR(250),
	IN `newgender` VARCHAR(3),
	IN `newfechanac` DATE,
	IN `iduseredit` INT

)
BEGIN
	UPDATE usuario SET
    first_name=firstname,
    last_name=lastname,
    email=newemail,
    password=pass,
    url_img=urlim,
    gender=newgender,
    fechanac=newfechanac
    WHERE id=iduseredit;
END//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
