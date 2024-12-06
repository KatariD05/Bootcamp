-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_eventos
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_eventos` ;

-- -----------------------------------------------------
-- Schema esquema_eventos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_eventos` DEFAULT CHARACTER SET utf8 ;
USE `esquema_eventos` ;

-- -----------------------------------------------------
-- Table `esquema_eventos`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_eventos`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `esquema_eventos`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT now(),
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_eventos`.`eventos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_eventos`.`eventos` ;

CREATE TABLE IF NOT EXISTS `esquema_eventos`.`eventos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `evento` VARCHAR(255) NULL,
  `ubicacion` VARCHAR(255) NULL,
  `fecha` VARCHAR(45) NULL,
  `detalle` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT now(),
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_eventos_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_eventos_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_eventos`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
