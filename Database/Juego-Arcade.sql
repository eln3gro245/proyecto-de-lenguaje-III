DROP TABLE "Entities";


CREATE TABLE IF NOT EXISTS "Entities"(
id INT PRIMARY KEY,
nombre TEXT,
escala REAL DEFAULT 1.0,
hp INTEGER DEFAULT 100,
speed REAL,
jump REAL,
force REAL,
is_climbing INTEGER DEFAULT 0
)

INSERT INTO "Entities"(nombre, escala, hp, speed, jump, force) VALUES ('Jugador', 1.0, 5, 5.0, 12.0, 15.0)

select * FROM "Entities"