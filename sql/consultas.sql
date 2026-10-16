--script 1: creacion base de datos

CREATE DATABASE IF NOT EXISTS gestion_escolar
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

--script 2: creacion de usuario local y remoto

CREATE USER IF NOT EXISTS 'gestion_l'@'localhost' IDENTIFIED BY 'casaca2026'; --importante que es gestion_ L minuscula    ------- usuario local
CREATE USER IF NOT EXISTS 'gestion_r'@'%' IDENTIFIED BY 'casaca2026';		--------usuario remoto


-- script 3: asignacion permisos

GRANT ALL PRIVILEGES ON gestion_escolar.* TO 'gestion_l'@'localhost';
GRANT ALL PRIVILEGES ON gestion_escolar.* TO 'gestion_r'@'%';

--aplicar cambios
FLUSH PRIVILEGES;


--estas son las credenciales de superusuario para acceder a la aplicacion igualmente estaran en un txt

--superuser
--nombre:vicente
--correo:vicente@admin.cl
--password:casaca

