-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: cuidatiacogdb
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actividad_usuario`
--

DROP TABLE IF EXISTS `actividad_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividad_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `tipo_evento` enum('Registrarse','Iniciar sesión','Jugar','Desbloquear nivel','Completar un nivel','Poner una reseña','Eliminar reseña','Añadir a favorito','Editar el perfil','Subir de nivel','Creo una incidencia') NOT NULL,
  `descripcion` text,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `actividad_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividad_usuario`
--

LOCK TABLES `actividad_usuario` WRITE;
/*!40000 ALTER TABLE `actividad_usuario` DISABLE KEYS */;
INSERT INTO `actividad_usuario` VALUES (1,1,'Registrarse','El usuario se ha registrado en la plataforma.','2025-07-24 09:15:00'),(2,26,'Iniciar sesión','Inicio de sesión exitoso.','2025-07-25 08:00:00'),(3,27,'Jugar','El usuario jugó al juego \"Sopa de Letras - Nivel 1\".','2025-07-25 10:30:00'),(4,28,'Desbloquear nivel','El usuario desbloqueó el nivel 2 del juego de memoria.','2025-07-25 11:00:00'),(5,28,'Completar un nivel','El usuario completó el nivel 3 de \"Sopa de Letras\" y ganó 50 puntos de experiencia.','2025-07-25 11:15:00'),(6,1,'Poner una reseña','El usuario dejó una reseña positiva en \"Juego de Conexiones\".','2025-07-25 11:45:00'),(7,1,'Añadir a favorito','El usuario marcó \"Sopa de Letras\" como uno de sus juegos favoritos.','2025-07-25 12:00:00'),(8,27,'Editar el perfil','El usuario actualizó su nombre de usuario y su avatar.','2025-07-25 12:30:00'),(9,26,'Subir de nivel','El usuario subió al nivel 5 de experiencia.','2025-07-25 12:45:00'),(10,1,'Jugar','El usuario jugó al juego \"Memoria Visual - Nivel 4\".','2025-07-25 13:00:00'),(11,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-25 14:04:17'),(12,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-25 14:05:26'),(13,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-25 14:05:49'),(15,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-29 09:58:00'),(16,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-29 10:08:40'),(17,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-29 12:27:38'),(18,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-29 12:33:59'),(19,62,'Editar el perfil','Usuario modificó su perfíl correctamente','2025-07-29 12:37:29'),(20,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-29 12:37:45'),(21,69,'Registrarse','Usuario registrado correctamente','2025-07-29 13:04:05'),(22,1,'Añadir a favorito','Usuario quito[object Object] a favoritos','2025-07-29 13:19:03'),(23,1,'Añadir a favorito','Usuario quito[object Object] a favoritos','2025-07-29 13:20:27'),(24,1,'Añadir a favorito','Usuario quito[object Object] a favoritos','2025-07-29 13:21:42'),(25,1,'Añadir a favorito','Usuario quito[object Object] a favoritos','2025-07-29 13:22:08'),(26,1,'Añadir a favorito','Usuario quito[object Object] a favoritos','2025-07-29 13:22:35'),(27,1,'Añadir a favorito','Usuario quitó Memoria Visual a favoritos','2025-07-29 13:23:58'),(28,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:24:20'),(29,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:24:26'),(30,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:30:09'),(31,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:31:00'),(32,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:32:07'),(33,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:32:09'),(34,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:34:00'),(35,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:34:09'),(36,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:35:23'),(37,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:35:27'),(38,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:36:05'),(39,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:36:07'),(40,1,'Añadir a favorito','Usuario quitó Memoria Visual de favoritos','2025-07-29 13:36:47'),(41,1,'Añadir a favorito','Usuario añadió Memoria Visual a favoritos','2025-07-29 13:36:48'),(42,1,'Poner una reseña','Usuario puso una reseña correctamente en undefined','2025-07-30 09:42:28'),(43,1,'Poner una reseña','Usuario puso una reseña correctamente en undefined','2025-07-30 09:47:12'),(44,1,'Poner una reseña','Usuario puso una reseña correctamente en undefined','2025-07-30 09:53:42'),(45,1,'Poner una reseña','Usuario puso una reseña correctamente en juego desconocido','2025-07-30 09:54:30'),(46,1,'Poner una reseña','Usuario puso una reseña correctamente en juego desconocido','2025-07-30 09:57:08'),(47,1,'Poner una reseña','Usuario puso una reseña correctamente en Secuencia de Luces','2025-07-30 09:58:18'),(48,1,'Eliminar reseña','Usuario eliminó su reseña en Sopa de Letras','2025-07-30 10:11:49'),(49,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego undefined','2025-07-30 10:18:21'),(50,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego undefined','2025-07-30 10:20:29'),(51,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Memoria Visual','2025-07-30 10:22:59'),(52,1,'Jugar','Usuario comenzó a jugar el nivel 2 del juego Memoria Visual','2025-07-30 10:23:33'),(53,1,'Jugar','Usuario comenzó a jugar el nivel 2 del juego Memoria Visual','2025-07-30 10:25:16'),(54,1,'Completar un nivel','Usuario completó el nivel 2 del juego Memoria Visual','2025-07-30 10:25:42'),(55,1,'Jugar','Usuario comenzó a jugar el nivel 3 del juego Memoria Visual','2025-07-30 10:29:20'),(56,1,'Completar un nivel','Usuario completó el nivel 3 del juego Memoria Visual','2025-07-30 10:30:48'),(57,1,'Desbloquear nivel','Usuario desbloqueó el nivel 4 del juego Memoria Visual','2025-07-30 10:30:48'),(58,1,'Jugar','Usuario comenzó a jugar el nivel 4 del juego Memoria Visual','2025-07-30 10:31:44'),(59,1,'Completar un nivel','Usuario completó el nivel 4 del juego Memoria Visual','2025-07-30 10:33:43'),(60,1,'Desbloquear nivel','Usuario desbloqueó el nivel 5 del juego Memoria Visual','2025-07-30 10:33:43'),(61,1,'Jugar','Usuario comenzó a jugar el nivel 5 del juego Memoria Visual','2025-07-30 10:33:53'),(62,1,'Completar un nivel','Usuario completó el nivel 5 del juego Memoria Visual','2025-07-30 10:37:30'),(63,1,'Desbloquear nivel','Usuario desbloqueó el nivel 6 del juego Memoria Visual','2025-07-30 10:37:30'),(64,1,'Jugar','Usuario comenzó a jugar el nivel 5 del juego Memoria Visual','2025-07-30 10:40:44'),(65,1,'Desbloquear nivel','Usuario desbloqueó el nivel 6 del juego Memoria Visual','2025-07-30 10:43:23'),(66,1,'Eliminar reseña','Usuario eliminó su reseña en Sudoku','2025-07-30 12:40:20'),(67,1,'Creo una incidencia','Usuario creó una incidencia del tipo problema-tecnico','2025-07-30 13:01:25'),(68,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sopa de Letras','2025-07-31 10:11:22'),(69,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Sopa de Letras','2025-07-31 10:12:12'),(70,1,'Completar un nivel','Usuario completó el nivel 1 del juego Sopa de Letras','2025-07-31 10:12:12'),(71,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Memoria Visual','2025-07-31 10:12:36'),(72,1,'Completar un nivel','Usuario completó el nivel 1 del juego Memoria Visual','2025-07-31 10:13:01'),(73,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Memoria Visual','2025-07-31 10:13:01'),(74,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sudoku','2025-07-31 10:15:00'),(75,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sudoku','2025-07-31 10:16:48'),(76,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Secuencias Numéricas','2025-07-31 10:19:01'),(77,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Secuencias Numéricas','2025-07-31 10:19:20'),(78,1,'Completar un nivel','Usuario completó el nivel 1 del juego Secuencias Numéricas','2025-07-31 10:19:20'),(79,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Unir Cartas','2025-07-31 10:21:32'),(80,1,'Completar un nivel','Usuario completó el nivel 1 del juego Unir Cartas','2025-07-31 10:21:43'),(81,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Unir Cartas','2025-07-31 10:21:43'),(82,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Tres en Raya','2025-07-31 10:25:16'),(83,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Tres en Raya','2025-07-31 10:25:31'),(84,1,'Completar un nivel','Usuario completó el nivel 1 del juego Tres en Raya','2025-07-31 10:25:31'),(85,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Matemáticas Básicas','2025-07-31 10:27:01'),(86,1,'Completar un nivel','Usuario completó el nivel 1 del juego Matemáticas Básicas','2025-07-31 10:27:24'),(87,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Matemáticas Básicas','2025-07-31 10:27:24'),(88,1,'Jugar','Usuario comenzó a jugar el nivel 3 del juego Adivina la Palabra','2025-07-31 10:28:47'),(89,1,'Desbloquear nivel','Usuario desbloqueó el nivel 4 del juego Adivina la Palabra','2025-07-31 10:29:33'),(90,1,'Completar un nivel','Usuario completó el nivel 3 del juego Adivina la Palabra','2025-07-31 10:29:33'),(91,1,'Jugar','Usuario comenzó a jugar el nivel 4 del juego Cálculo Rápido','2025-07-31 10:31:00'),(92,1,'Desbloquear nivel','Usuario desbloqueó el nivel 5 del juego Cálculo Rápido','2025-07-31 10:31:35'),(93,1,'Completar un nivel','Usuario completó el nivel 4 del juego Cálculo Rápido','2025-07-31 10:31:35'),(94,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Secuencia de Luces','2025-07-31 10:32:57'),(95,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Secuencia de Luces','2025-07-31 10:33:09'),(96,1,'Completar un nivel','Usuario completó el nivel 1 del juego Secuencia de Luces','2025-07-31 10:33:09'),(97,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sopa de Letras','2025-07-31 11:39:54'),(98,1,'Jugar','Usuario comenzó a jugar el nivel 5 del juego Sopa de Letras','2025-07-31 11:41:05'),(99,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sudoku','2025-07-31 11:42:32'),(100,1,'Jugar','Usuario comenzó a jugar el nivel 2 del juego Sudoku','2025-07-31 11:42:36'),(101,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-31 11:44:41'),(102,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-31 11:45:08'),(103,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Memoria Visual','2025-07-31 11:54:13'),(104,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-07-31 11:54:38'),(105,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-01 10:22:43'),(106,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-01 10:23:37'),(107,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-01 10:24:02'),(108,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-01 11:00:00'),(109,62,'Editar el perfil','Usuario modificó su perfíl correctamente','2025-08-01 11:39:07'),(110,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-01 11:40:56'),(111,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 11:50:34'),(112,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 11:50:34'),(113,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sudoku','2025-08-01 11:50:37'),(114,1,'Completar un nivel','Usuario completó el nivel 1 del juego Sudoku','2025-08-01 11:51:06'),(115,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Sudoku','2025-08-01 11:51:06'),(116,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:09:44'),(117,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:09:44'),(118,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:11:11'),(119,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:11:11'),(120,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:15:40'),(121,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:15:40'),(122,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:16:41'),(123,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:16:41'),(124,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:17:28'),(125,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:17:28'),(126,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:18:29'),(127,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:18:29'),(128,1,'Desbloquear nivel','Usuario desbloqueó el nivel 1 del juego Sudoku','2025-08-01 13:20:17'),(129,1,'Completar un nivel','Usuario completó el nivel null del juego Sudoku','2025-08-01 13:20:17'),(130,1,'Jugar','Usuario comenzó a jugar el nivel 1 del juego Sudoku','2025-08-01 13:28:19'),(131,1,'Desbloquear nivel','Usuario desbloqueó el nivel 2 del juego Sudoku','2025-08-01 13:28:40'),(132,1,'Completar un nivel','Usuario completó el nivel 1 del juego Sudoku','2025-08-01 13:28:40'),(133,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-04 09:57:11'),(134,1,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-04 10:11:58'),(135,62,'Iniciar sesión','Usuario inició sesión correctamente','2025-08-07 12:03:27');
/*!40000 ALTER TABLE `actividad_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `plazas_ocupadas` int DEFAULT '0',
  `plazas_totales` int NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `localidad` varchar(100) NOT NULL,
  `fecha_evento` date NOT NULL,
  `activo` tinyint(1) DEFAULT '0',
  `momento_insercion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos_usuario`
--

DROP TABLE IF EXISTS `eventos_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `evento_id` int NOT NULL,
  `participacion` tinyint(1) DEFAULT '0',
  `fecha_inscripcion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `evento_id` (`evento_id`),
  CONSTRAINT `eventos_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `eventos_usuario_ibfk_2` FOREIGN KEY (`evento_id`) REFERENCES `eventos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_usuario`
--

LOCK TABLES `eventos_usuario` WRITE;
/*!40000 ALTER TABLE `eventos_usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incidencias`
--

DROP TABLE IF EXISTS `incidencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incidencias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `resuelta` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incidencias`
--

LOCK TABLES `incidencias` WRITE;
/*!40000 ALTER TABLE `incidencias` DISABLE KEYS */;
INSERT INTO `incidencias` VALUES (1,'Pedro Metidieri Gomez','pedrometidierigomez@gmail.com','consulta-general','rgegdfdsgbdsgsdgds','2025-07-25 08:43:24',0),(2,'Jose','info@xenior.org','otro','rgeykyjdghdfj','2025-07-25 10:14:34',0),(3,'Borja','metidieriazazels@gmail.com','sugerencia','yteyeye','2025-07-29 08:05:36',0),(4,'Usuario de prueba','metidieriazazels@gmail.com','error-en-juego','Error en la sopa de letras','2025-07-30 10:33:33',0),(5,'Jose','info@xenior.org','cuentas','aregreqfadsf','2025-07-30 10:35:19',0),(6,'Jose','info@xenior.org','cuentas','aregreqfadsf','2025-07-30 10:35:49',0),(7,'Jose','info@xenior.org','error-en-juego','aregreqfadsf','2025-07-30 10:36:13',0),(8,'Jose','info@xenior.org','error-en-juego','aregreqfadsf','2025-07-30 10:36:17',0),(9,'Ignacio','ignacio@gmail.com','cuentas','adagrhrehrertwe','2025-07-30 10:37:14',0),(10,'Ignacio','ignacio@gmail.com','cuentas','adagrhrehrertwe','2025-07-30 10:38:36',0),(11,'Ignacio','ignacio@gmail.com','cuentas','adagrhrehrertwe','2025-07-30 10:38:50',0),(12,'Pedro Metidieri Rayo','demo@demo.com','error-en-juego','67856uufghkfit','2025-07-30 10:43:24',0),(13,'Pedro Metidieri Rayo','demo@demo.com','error-en-juego','67856uufghkfit','2025-07-30 10:43:48',0),(14,'Pedro Metidieri Rayo','demo@demo.com','error-en-juego','67856uufghkfit','2025-07-30 10:45:02',0),(15,'Pedro Metidieri Rayo','demo@demo.com','error-en-juego','67856uufghkfit','2025-07-30 10:46:26',0),(16,'Pedro Metidieri Rayo','demo@demo.com','error-en-juego','67856uufghkfit','2025-07-30 10:47:38',0),(17,'Pedro Metidieri Rayo','daa@gmail.com','otro','dasfgdghrehrtwgds','2025-07-30 10:48:37',0),(18,'Pedro Metidieri Gomez','admin@cuidatiacog.com','error-en-juego','fdsggehrehre','2025-07-30 10:49:07',0),(19,'njwerwet','rwrwrew@gmail.com','problema-tecnico','noiewtrehe','2025-07-30 10:51:04',0),(20,'Borja','demo@demo.com','otro','dwefgewhgrew','2025-07-30 10:53:15',0),(21,'Jose','pedro.metidieri@adiper.es','sugerencia','fewgagdsgs','2025-07-30 10:54:25',0),(22,'Pedro Metidieri Rayo','pedro.metidieri@adiper.es','problema-tecnico','dasafas','2025-07-30 10:58:45',0),(23,'Pedro Metidieri Gomez','demo@demo.com','error-en-juego','dswfsawefewgfwe','2025-07-30 10:59:08',0),(24,'Jose','admin@cuidatiacog.com','error-en-juego','afsfsfasfa','2025-07-30 11:00:53',0),(25,'Pedro Metidieri Rayo','demo@demo.com','problema-tecnico','dasfweewgew','2025-07-30 11:01:25',0),(26,'Borja','demo@demo.com','problema-tecnico','adweafewgew','2025-07-30 11:01:47',0),(27,'Pedro Metidieri Gomez','pedrometidierigomez@gmail.com','error-en-juego','32safsagfadgdsg','2025-07-30 11:03:12',0),(28,'Pedro Metidieri Rayo','metidieriazazels@gmail.com','sugerencia','hgfjgrjhedhdfgjkfk','2025-07-30 11:04:21',0),(29,'Usuario de prueba','demo@demo.com','sugerencia','dadafdafa','2025-07-30 11:06:27',0);
/*!40000 ALTER TABLE `incidencias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `juegos`
--

DROP TABLE IF EXISTS `juegos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juegos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `imagen` varchar(255) DEFAULT NULL,
  `icono` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `numero_jugadas` int DEFAULT '0',
  `es_destacado` tinyint(1) DEFAULT '0',
  `bloqueado` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juegos`
--

LOCK TABLES `juegos` WRITE;
/*!40000 ALTER TABLE `juegos` DISABLE KEYS */;
INSERT INTO `juegos` VALUES (1,'Memoria Visual','Recuerda la posición de objetos en pantalla.','/Memoria-Visual.png','Brain','Memoria',12,0,0),(2,'Sopa de Letras','Encuentra palabras escondidas rápidamente.','/SopaLetras.png','Puzzle','Letras',14,0,0),(3,'Sudoku','Rellena los números sin repetir filas o columnas.','/Sudoku.png','Gamepad2','Números',23,0,0),(4,'Secuencias Numéricas','Completa la serie lógica que falta.','/SecuenciasNumericas.png','Gamepad2','Numeros',7,0,0),(5,'Unir Cartas','Haz coincidir las palabras con las imagenes arrastrandolas','/Parejas.png','Puzzle','Memoria',4,0,0),(6,'Tres en Raya','El juego clásico de 3 en raya','/tres-en-raya.png','Puzzle','Logica',4,0,0),(7,'Matemáticas Básicas','Ejercicios simples de suma y resta.','/MatematicasBasicas.png','Gamepad2','Numeros',2,0,0),(8,'Adivina la Palabra','Completa palabras con letras faltantes.','/AdivinaPalabra.png','Puzzle','Letras',5,0,0),(9,'Cálculo Rápido','Resuelve operaciones lo más rápido posible.','/CalculoRapido.png','Brain','Numeros',5,0,0),(10,'Secuencia de Luces','Reproduce el patrón mostrado por luces.','/SecuenciaLuces.png','Gamepad2','Atencion',3,0,0);
/*!40000 ALTER TABLE `juegos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles_juego`
--

DROP TABLE IF EXISTS `niveles_juego`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles_juego` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dificultad_textual` enum('Principiante','Fácil','Intermedio','Difícil','Experto') DEFAULT NULL,
  `experiencia_otorgada` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_juego`
--

LOCK TABLES `niveles_juego` WRITE;
/*!40000 ALTER TABLE `niveles_juego` DISABLE KEYS */;
INSERT INTO `niveles_juego` VALUES (1,'Principiante',10),(2,'Fácil',20),(3,'Intermedio',30),(4,'Difícil',40),(5,'Experto',50);
/*!40000 ALTER TABLE `niveles_juego` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles_juego_usuario`
--

DROP TABLE IF EXISTS `niveles_juego_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles_juego_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `nivel_id` int DEFAULT NULL,
  `juego_id` int DEFAULT NULL,
  `es_favorito` tinyint(1) DEFAULT '0',
  `tiempo_jugado` timestamp NULL DEFAULT NULL,
  `ultima_conexion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`,`nivel_id`,`juego_id`),
  KEY `nivel_id` (`nivel_id`),
  KEY `juego_id` (`juego_id`),
  CONSTRAINT `niveles_juego_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `niveles_juego_usuario_ibfk_2` FOREIGN KEY (`nivel_id`) REFERENCES `niveles_juego` (`id`),
  CONSTRAINT `niveles_juego_usuario_ibfk_3` FOREIGN KEY (`juego_id`) REFERENCES `juegos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_juego_usuario`
--

LOCK TABLES `niveles_juego_usuario` WRITE;
/*!40000 ALTER TABLE `niveles_juego_usuario` DISABLE KEYS */;
INSERT INTO `niveles_juego_usuario` VALUES (1,1,5,9,0,NULL,'2025-07-24 07:22:18'),(2,1,2,3,0,NULL,'2025-07-24 07:24:01'),(3,1,5,2,1,NULL,'2025-07-24 08:07:46'),(4,1,4,8,0,NULL,'2025-07-24 08:16:28'),(5,1,1,6,1,NULL,'2025-07-24 11:50:20'),(6,36,2,8,0,NULL,'2025-07-24 11:52:44'),(7,36,2,2,0,NULL,'2025-07-24 11:55:37'),(8,36,3,1,0,NULL,'2025-07-24 11:56:53'),(9,36,2,3,1,NULL,'2025-07-24 12:02:25'),(10,36,2,5,0,NULL,'2025-07-24 12:19:52'),(11,62,2,1,1,NULL,'2025-07-29 08:19:14'),(12,62,2,10,0,NULL,'2025-07-29 08:19:51'),(13,1,5,1,1,NULL,'2025-07-29 11:18:21'),(14,1,2,4,0,NULL,'2025-07-31 08:19:20'),(15,1,2,5,0,NULL,'2025-07-31 08:21:43'),(16,1,2,7,0,NULL,'2025-07-31 08:27:24'),(17,1,2,10,0,NULL,'2025-07-31 08:33:09');
/*!40000 ALTER TABLE `niveles_juego_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (2,'administrador'),(1,'usuario');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `contrasena_hash` varchar(255) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id_rol` int DEFAULT '1',
  `avatar_url` varchar(255) DEFAULT '/avatars/default-avatar.png',
  `biografia` text,
  `ultima_conexion` timestamp NULL DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `experiencia` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Pedro Metidieri Gomez','pedrometidierigomez@gmail.com','2003-06-25','$2b$12$7QDIEMM9uCsYPacv1fibBurQ.JzJlfW0pwiovBf.KknWot5z16K4y','2025-07-22 10:45:22',2,'/avatars/1_thumbnail_image001.jpg','Esto es un perfil de administrador',NULL,1,480),(26,'Ana Martínez','ana@example.com','1990-04-15','$2b$12$abcdhashedpwd123','2025-07-23 08:26:50',1,'/avatars/default-avatar.png','Apasionada por los juegos de memoria.','2025-07-23 08:26:50',1,1200),(27,'Luis Gómez','luis@example.com','1985-10-02','$2b$12$abcdhashedpwd456','2025-07-21 08:26:50',1,'/avatars/default-avatar.png','Me encantan los retos visuales.','2025-07-23 08:26:50',1,850),(28,'Carla Pérez','carla@example.com','1993-08-21','$2b$12$abcdhashedpwd789','2025-07-20 08:26:50',1,'/avatars/default-avatar.png',NULL,'2025-07-23 08:26:50',1,300),(29,'Jorge Ramírez','jorge@example.com','1988-06-11','$2b$12$hashpassword101','2025-07-14 08:26:50',2,'/avatars/default-avatar.png','Administrador del sistema.','2025-07-23 08:26:50',1,2500),(30,'Lucía Torres','lucia@example.com','1995-12-03','$2b$12$hashpassword202','2025-06-23 08:26:50',1,'/avatars/default-avatar.png','Estudiante de psicología.','2025-07-23 08:26:50',1,430),(31,'Pedro Díaz','pedro@example.com','1991-02-17','$2b$12$hashpassword303','2025-07-23 08:26:50',1,'/avatars/default-avatar.png',NULL,'2025-07-23 08:26:50',0,900),(32,'María López','maria@example.com','1989-09-27','$2b$12$hashpassword404','2025-05-23 08:26:50',1,'/avatars/default-avatar.png','Jugadora frecuente de sopa de letras.','2025-07-23 08:26:50',1,1500),(33,'David Navarro','david@example.com','1992-01-09','$2b$12$hashpassword505','2025-07-23 08:26:50',1,'/avatars/default-avatar.png',NULL,'2025-07-23 08:26:50',1,720),(34,'Elena Ruiz','elena@example.com','1994-05-06','$2b$12$hashpassword606','2025-07-23 08:26:50',1,'/avatars/default-avatar.png','Me encantan los desafíos mentales.','2025-07-23 08:26:50',1,1050),(35,'Sergio Castro','sergio@example.com','1986-07-22','$2b$12$hashpassword707','2025-07-23 08:26:50',1,'/avatars/default-avatar.png','Usuario beta tester.','2025-07-23 08:26:50',1,600),(36,'Borja','demo@demo.com','1995-05-05','$2b$12$Cdq23MXPEud181ext9vAZeTnRwGTWPCHxFdMx01CFzJG9sXFqYvha','2025-07-24 11:51:13',1,'/avatars/36_Elena_Nevado_eurodiputada.jpg','Me gustasn los juegos de memoria',NULL,1,70),(37,'Elena Sánchez','user1@example.com','1966-01-16','6e7209c992075d429664eb2d539983eb2136917f62508835e42934b82696cea7','2025-07-01 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 1','2025-07-01 22:00:00',1,446),(38,'David Martínez','user2@example.com','2005-01-06','511224d5d3e45c214e897f3951f42c9cf2c5862b5280ad4b2eae4ca074d65f74','2025-06-22 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 2','2025-06-24 22:00:00',1,902),(39,'Manuel Díaz','user3@example.com','1984-01-02','6b527fca34dcd3e03a55fe9f43e18ceff8a100f7078f03c726bdabe77ae7382c','2025-07-07 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 3','2025-07-11 22:00:00',1,824),(40,'Marta Romero','user4@example.com','1995-01-03','25942e6bfbda12d9791d42d99765c9923c1b5a134a2c176eafaa93c98e4767b2','2025-06-26 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 4','2025-07-01 22:00:00',1,871),(41,'Raúl Alonso','user5@example.com','1987-01-01','57d8997e5b313e0e74248f820ea6504d3ef96e32d5091a6d74bc33152072d024','2025-07-15 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 5','2025-07-16 22:00:00',1,768),(42,'Diego Alonso','user101@example.com','1973-01-01','770cb9de8c2c4b4e7dacb666db809f249528428db2668135b6ae501d8b573597','2025-07-15 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 101','2025-07-22 22:00:00',1,431),(43,'Ana Pérez','user102@example.com','1977-01-18','65600b06f96fb5861792342635180fed099f49367df9538196a0a415f7891835','2025-07-16 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 102','2025-07-21 22:00:00',1,782),(44,'Raquel Díaz','user103@example.com','1973-01-01','4a7f282c7bab00b116383081fcb8fcad55832debc90ddd5f0b78e00c785d0c0c','2025-06-24 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 103','2025-07-08 22:00:00',1,290),(45,'Pedro Romero','user104@example.com','1996-01-07','240c1f7b0bb2d2b1bcf606a96ffa4cfadaddf7b607ec522b00ec24eecb5bf733','2025-07-14 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 104','2025-07-17 22:00:00',1,771),(46,'Raquel Romero','user105@example.com','1962-01-05','56eec59b46f94219fa41e387bd236e459f307a917f1c7db5a93d9328f456df77','2025-06-27 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 105','2025-07-01 22:00:00',1,39),(47,'Laura Martínez','user106@example.com','1985-01-11','ce861924b1dd418fa71d43a634fd4cb826b19eeba484a28f081ea27aa6d400c1','2025-07-13 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 106','2025-07-17 22:00:00',1,422),(48,'Laura Ruiz','user107@example.com','1960-01-17','c04b06e816ec76f8911594887a02b7dacbc51677977a79aba2082a21bdd4dc59','2025-07-17 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 107','2025-07-18 22:00:00',1,679),(49,'Miguel García','user108@example.com','2006-01-26','da492000590171abc7ac715d281b09b398f7deb8b380526922eea6ee1bb4027a','2025-07-04 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 108','2025-07-21 22:00:00',1,145),(50,'Rubén Ruiz','user109@example.com','1974-01-16','0630425087ae850093fbc2a0cbe104c31c3bd77503cb6b2f81f2e9584e4208be','2025-06-25 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 109','2025-07-08 22:00:00',1,319),(51,'Sofía Martínez','user110@example.com','1969-01-08','229c76a1305c3e89dfc3d9cd3f877f6ae31baf08df1c57c54f25f59ab8e94963','2025-06-28 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 110','2025-07-05 22:00:00',1,848),(52,'Marta Sánchez','user111@example.com','1973-01-06','9615744218456f4d8d165c43741f5eaaaf7c8d3a739d640358e2ee1f355a38a4','2025-07-10 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 111','2025-07-15 22:00:00',1,627),(53,'Carlos Alonso','user112@example.com','2006-01-17','d8e700f5e8821f63b4ea3ab6f5ed13c3d657e559201cbd64350bc3c9279d3c9f','2025-06-29 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 112','2025-07-17 22:00:00',1,254),(54,'Raquel Díaz','user113@example.com','2003-01-18','01aebf2e616624d0a360fb3250b24cd9d1c8eeb509b52d72a1a9e938178c1c84','2025-06-30 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 113','2025-07-13 22:00:00',1,789),(55,'Ana Moreno','user114@example.com','2003-01-05','dc6c295d8f8c3b9ee6c799ccfc45eaa7e54a46c987d5d3961db3e37cbcc42dd8','2025-07-03 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 114','2025-07-23 22:00:00',1,968),(56,'Sergio Sánchez','user115@example.com','1981-01-13','5f0ccddf808bda060bc06071a3b8794e5c39e1c60e153e4b541110183914f9e2','2025-07-11 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 115','2025-07-19 22:00:00',1,500),(57,'Patricia Romero','user116@example.com','1964-01-03','e168f989227e21956a4f49d9a96d9f9e7db1548f8f73e6b2fcde2235be9eb645','2025-06-26 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 116','2025-06-30 22:00:00',1,319),(58,'Miguel Moreno','user117@example.com','1977-01-07','c2f0b5c9b78051900168367fa82edbf22b870fd579f69a8c06206dc16a2d6a45','2025-06-22 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 117','2025-07-02 22:00:00',1,973),(59,'Patricia García','user118@example.com','1974-01-12','3211e18a96ee43fd679e54f4b54fc3e7aa94821a2fbc405d63f60f1431587f9d','2025-07-20 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 118','2025-07-23 22:00:00',1,416),(60,'Lucía Sánchez','user119@example.com','1991-01-20','0f60cc0bd8f107c7398b0e1c3b52c615b4d8de65d2dfeb3e4d05cb64c7083e0a','2025-07-19 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 119','2025-07-21 22:00:00',1,84),(61,'Andrés García','user120@example.com','1972-01-25','82091ae73822201c5f42cc8271e60cc5ec0df2765ff92d94bd7b3c6f1748a3b6','2025-07-06 22:00:00',1,'/avatars/default-avatar.png','Biografía del usuario 120','2025-07-11 22:00:00',1,875),(62,'Usuario de prueba','pedro.metidieri@adiper.es','2003-02-02','$2b$12$o2K/LXL74rsJJYAModzlveW1htsNDAT5FSQRTYOfzqp4w3DF4RTM2','2025-07-25 11:46:37',1,'/avatars/default-avatar.png','Esto es un usuario de prueba, la descripción',NULL,1,20),(63,'Ignacio','info@xenior.org','2002-05-05','$2b$12$nPsAwYhtGaqBRpfSg.PWIeYlYcXZXbGjbVEwQrFgpFMlfT8v7gkL2','2025-07-29 10:04:30',1,'/avatars/default-avatar.png',NULL,NULL,1,0),(64,'gegwfagsfs','dagsfaf@gmail.com','1971-04-04','$2b$12$n5O442e9TeNdZhyZFwlePemXvOv8sAmQ63QExkhOcTNy/itNWdhx.','2025-07-29 10:51:30',1,'/avatars/default-avatar.png',NULL,NULL,1,0),(66,'Hola','hola@hotmail.com','2001-05-05','$2b$12$c5FGBMl3UX5Mfm7LfY7Q1.lYwvpyZTeX.hYl8OoNWb8tFKCVdXjFq','2025-07-29 10:55:55',1,'/avatars/default-avatar.png',NULL,NULL,1,0),(67,'Adios','Adios@hotmail.com','2003-05-05','$2b$12$nAR5iTKByNU8vKWyrTSei.7lGd.4Y2/y9Y7Re5945TPtpBUwRbSoi','2025-07-29 10:58:11',1,'/avatars/default-avatar.png',NULL,NULL,1,0),(68,'HolaAdios','holaadios@gmail.com','2005-04-04','$2b$12$BktAGFtElWqwPTJjuQ7zB.4z.ELxkybLxbyojbpK5HCQ4TTPPFSeC','2025-07-29 11:00:26',1,'/avatars/default-avatar.png',NULL,NULL,1,0),(69,'gonzalo','gonzalo@gmail.com','2001-01-01','$2b$12$Qg98urfePVPfdkEPdnuBMOEQmit0YL167qLellG99HUQqio9JCQ.m','2025-07-29 11:04:04',1,'/avatars/default-avatar.png',NULL,NULL,1,0);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valoraciones`
--

DROP TABLE IF EXISTS `valoraciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valoraciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `juego_id` int DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  `puntuacion` int DEFAULT NULL,
  `comentario` text,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `es_destacada` tinyint(1) DEFAULT '0',
  `editada` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `juego_id` (`juego_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `valoraciones_ibfk_1` FOREIGN KEY (`juego_id`) REFERENCES `juegos` (`id`),
  CONSTRAINT `valoraciones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `valoraciones_chk_1` CHECK (((`puntuacion` >= 0) and (`puntuacion` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valoraciones`
--

LOCK TABLES `valoraciones` WRITE;
/*!40000 ALTER TABLE `valoraciones` DISABLE KEYS */;
INSERT INTO `valoraciones` VALUES (1,6,1,5,'muy divertido','2025-07-24 11:49:56',0,0),(2,5,36,5,'','2025-07-24 12:19:57',0,0),(4,1,62,0,'Me gusta mucho este juego','2025-07-29 08:18:45',0,0),(7,4,1,5,'Reseña prueba 3','2025-07-30 07:42:28',0,0),(8,5,1,5,'Resela','2025-07-30 07:47:12',0,0),(9,7,1,5,'fdjtrjeefd','2025-07-30 07:53:42',0,0),(10,8,1,3,'fsjrjterjjdf','2025-07-30 07:54:30',0,0),(11,9,1,4,'','2025-07-30 07:57:07',0,0),(12,10,1,5,'Reseña final','2025-07-30 07:58:18',0,0);
/*!40000 ALTER TABLE `valoraciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-08  9:04:38
