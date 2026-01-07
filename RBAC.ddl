CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
   	password VARCHAR(100) NOT null
);

CREATE TABLE roles (
    id INT PRIMARY KEY,
    role_name VARCHAR(50) NOT null
);

CREATE TABLE permissions (
    id INT PRIMARY KEY,
    resource VARCHAR(50)
);

CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE role_permissions (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id)
);
