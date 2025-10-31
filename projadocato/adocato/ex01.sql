BEGIN;
--
-- Add field data_nascimento to gato
--
CREATE TABLE "new__adocato_gato" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"data_nascimento" date NOT NULL, "nome" varchar(100) NOT NULL, 
"sexo" varchar(1) NOT NULL, "cor" varchar(50) NOT NULL, "descricao" text NULL, 
"disponivel" bool NOT NULL, "raca_id" 
bigint NOT NULL REFERENCES "adocato_raca" ("id") DEFERRABLE INITIALLY DEFERRED);

INSERT INTO "new__adocato_gato" ("id", "nome", "sexo", "cor", 
"descricao", "disponivel", "raca_id", "data_nascimento") SELECT "id", "nome", 
"sexo", "cor", "descricao", "disponivel", "raca_id", '2025-10-31' FROM "adocato_gato";

DROP TABLE "adocato_gato";

ALTER TABLE "new__adocato_gato" RENAME TO "adocato_gato";

CREATE INDEX "adocato_gato_raca_id_ae5eeaf1" ON "adocato_gato" ("raca_id");

COMMIT;