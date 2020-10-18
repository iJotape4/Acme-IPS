-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.21 - MySQL Community Server - GPL
-- SO del servidor:              Win64acme
-- HeidiSQL Versión:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para dbipsacme
CREATE DATABASE IF NOT EXISTS `dbipsacme` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbipsacme`;

-- Volcando estructura para tabla dbipsacme.paciente
CREATE TABLE IF NOT EXISTS `paciente` (
  `IdPaciente` int NOT NULL AUTO_INCREMENT,
  `PrimerNombreP` varchar(50) NOT NULL,
  `SegundoNombreP` varchar(50) NOT NULL,
  `PrimerApellidoP` varchar(50) NOT NULL,
  `SegundoApellidoP` varchar(50) NOT NULL,
  `UsuarioP` varchar(50) NOT NULL,
  `ContraseñaP` varchar(50) NOT NULL,
  `DocumentoIdP` int NOT NULL,
  `TipoDocumentoP` varchar(5) NOT NULL,
  `EdadP` int NOT NULL,
  `CorreoElectronicoP` varchar(90) NOT NULL,
  `EPSP` varchar(90) NOT NULL,
  `IdCita` int NOT NULL,
  UNIQUE KEY `IdPaciente` (`IdPaciente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla dbipsacme.paciente: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` (`IdPaciente`, `PrimerNombreP`, `SegundoNombreP`, `PrimerApellidoP`, `SegundoApellidoP`, `UsuarioP`, `ContraseñaP`, `DocumentoIdP`, `TipoDocumentoP`, `EdadP`, `CorreoElectronicoP`, `EPSP`, `IdCita`) VALUES
	(1, 'Jhoan', 'Jesus', 'Ortiz', 'Sandoval', 'jortiz', '132', 1005543307, 'CC', 20, 'jortiz519@unab.edu.co', 'Nueva EPS', 123),
	(2, 'Javier', 'Yesid', 'Parra', 'Carrillo', 'jparra', '123', 1004835678, 'CC', 19, 'jparra@unab.edu.co', 'Nueva EPS', 121);
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
jpainformation_schema