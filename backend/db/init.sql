DROP TABLE IF EXISTS "receptores";
DROP TABLE IF EXISTS "doadores";

CREATE TABLE "receptores" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "telefone" VARCHAR(20) NOT NULL,
    "tipo_sanguineo" VARCHAR(3) NOT NULL,
    "data_nascimento" DATE NOT NULL,
    "endereco" TEXT NOT NULL,
    "necessidade_sangue" BOOLEAN NOT NULL
);

CREATE TABLE "doadores" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "telefone" VARCHAR(20) NOT NULL,
    "tipo_sanguineo" VARCHAR(3) NOT NULL,
    "data_nascimento" DATE NOT NULL,
    "endereco" TEXT NOT NULL
);

INSERT INTO "receptores" ("nome", "email", "telefone", "tipo_sanguineo", "data_nascimento", "endereco", "necessidade_sangue") 
VALUES 
('Pedro Henrique de Souza', 'pedro.souza@gec.inatel.br', '35991234568', 'A+', '2001-08-22', 'Rua Fictícia, 123, São Paulo', FALSE);

INSERT INTO "doadores" ("nome", "email", "telefone", "tipo_sanguineo", "data_nascimento", "endereco") 
VALUES 
('Amanda Silva Guimarães', 'amanda.silva@gec.inatel.br', '35991234567', 'A+', '2001-08-22', 'Rua Fictícia, 123, São Paulo');
