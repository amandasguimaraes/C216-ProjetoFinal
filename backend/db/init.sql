DROP TABLE IF EXISTS "doadores";
DROP TABLE IF EXISTS "doacoes";

CREATE TABLE "doadores" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "telefone" VARCHAR(20) NOT NULL,
    "tipo_sanguineo" VARCHAR(3) NOT NULL,
    "data_nascimento" VARCHAR(255) NOT NULL,
    "endereco" TEXT NOT NULL
);

CREATE TABLE "doacoes" (
    "id" SERIAL PRIMARY KEY,
    "nome_doador" VARCHAR(255) NOT NULL,
    "tipo_sanguineo" VARCHAR(3) NOT NULL,
    "data_doacao" VARCHAR(255) NOT NULL
);

INSERT INTO "doadores" ("nome", "email", "telefone", "tipo_sanguineo", "data_nascimento", "endereco") 
VALUES 
('Pedro Henrique de Souza', 'pedro.souza@gec.inatel.br', '35991234568', 'A+', '2001-08-22', 'Rua Fictícia, 123, São Paulo');

INSERT INTO "doadores" ("nome", "email", "telefone", "tipo_sanguineo", "data_nascimento", "endereco") 
VALUES 
('Amanda Silva Guimarães', 'amanda.silva@gec.inatel.br', '35991234567', 'A+', '2001-08-22', 'Rua Fictícia, 123, São Paulo');

INSERT INTO "doacoes" ("nome_doador", "tipo_sanguineo", "data_doacao") VALUES ('Pedro Henrique de Souza', 'A+', '2024-12-05');
