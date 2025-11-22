CREATE TABLE user(
    id INTEGER AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB;


CREATE TABLE recipe(
    id INTEGER AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    prep_time VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES user(id)
) ENGINE=InnoDB;


CREATE TABLE ingredient(
    id INTEGER AUTO_INCREMENT,
    recipe_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantity VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(recipe_id) REFERENCES recipe(id)
) ENGINE=InnoDB;


CREATE TABLE instruction(
    id INTEGER AUTO_INCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number TINYINT NOT NULL,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(recipe_id) REFERENCES recipe(id)
) ENGINE=InnoDB;

