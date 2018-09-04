CREATE TABLE `pets` (
 `id` VARCHAR(10) NOT NULL,
 `name` VARCHAR(100),
 `kind` VARCHAR(50),
 `gender` VARCHAR(6),
 `age` INT,
 `owner_id` INT,
 PRIMARY KEY(`id`)
);

CREATE TABLE `owners` (
 `id` VARCHAR(10) NOT NULL,
 `name` VARCHAR(100),
 `surname` VARCHAR(100),
 `street_address` VARCHAR(200),
 `city` VARCHAR(100),
 `state` VARCHAR(2),
 `state_full` VARCHAR(50),
 `zip_code` VARCHAR(10),
 PRIMARY KEY(`id`)
);

CREATE TABLE `procedure_history` (
 `id` INT NOT NULL,
 `pet_id` INT NOT NULL,
 `date` DATE,
 `procedure_id` INT,
 PRIMARY KEY(`id`)
);

CREATE TABLE `procedure_details` (
 `id` INT NOT NULL,
 `type` VARCHAR(100),
 `sub_code` DATE,
 `description` TEXT,
 `price` INT,
 PRIMARY KEY(`id`)
);
