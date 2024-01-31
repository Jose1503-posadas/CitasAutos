-- Crear la tabla 'usuarios' --
CREATE TABLE usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Insertar algunos datos de ejemplo --
INSERT INTO usuarios (username, password) VALUES
    ('joss', '1234'),
    ('moni', '4321');