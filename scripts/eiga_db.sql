BEGIN;
CREATE TABLE "eiga_articletype" (
    "id" serial NOT NULL PRIMARY KEY,
    "type" varchar(30) NOT NULL
)
;
CREATE TABLE "eiga_usertype" (
    "id" serial NOT NULL PRIMARY KEY,
    "type" varchar(30) NOT NULL
)
;
CREATE TABLE "eiga_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "userType_id" integer NOT NULL REFERENCES "eiga_usertype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(40) NOT NULL,
    "sex" varchar(1) NOT NULL,
    "age" integer NOT NULL,
    "email" varchar(75) NOT NULL
)
;
CREATE TABLE "eiga_certificate" (
    "id" serial NOT NULL PRIMARY KEY,
    "certificate" varchar(3) NOT NULL
)
;
CREATE TABLE "eiga_disctype" (
    "id" serial NOT NULL PRIMARY KEY,
    "format" varchar(1) NOT NULL,
    "description" varchar(10) NOT NULL
)
;
CREATE TABLE "eiga_dvd" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "purchase_date" date NOT NULL,
    "dub_languages" varchar(100) NOT NULL,
    "subtitle_languages" varchar(100) NOT NULL,
    "special_features" text NOT NULL,
    "disc_format_id" integer NOT NULL REFERENCES "eiga_disctype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "eiga_film" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "genre" varchar(200) NOT NULL,
    "film_cast" varchar(300) NOT NULL,
    "director" varchar(100) NOT NULL,
    "duration" smallint NOT NULL,
    "certificate_id" integer NOT NULL REFERENCES "eiga_certificate" ("id") DEFERRABLE INITIALLY DEFERRED,
    "release_date" date NOT NULL,
    "producer" varchar(200) NOT NULL,
    "distributor" varchar(50) NOT NULL,
    "website" varchar(100) NOT NULL,
    "advice" varchar(100) NOT NULL,
    "dvd_id" integer REFERENCES "eiga_dvd" ("id") DEFERRABLE INITIALLY DEFERRED,
    "synopsis" varchar(300) NOT NULL,
    "thumbnail" varchar(100) NOT NULL,
    "still" varchar(100) NOT NULL
)
;
CREATE TABLE "eiga_article" (
    "id" serial NOT NULL PRIMARY KEY,
    "article_type_id" integer NOT NULL REFERENCES "eiga_articletype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "author_id" integer NOT NULL REFERENCES "eiga_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "headline" varchar(100),
    "title" varchar(100) NOT NULL,
    "body" text NOT NULL,
    "rating" smallint NOT NULL,
    "related_film_id" integer NOT NULL REFERENCES "eiga_film" ("id") DEFERRABLE INITIALLY DEFERRED,
    "pub_date" date NOT NULL,
    "last_updated" date NOT NULL
)
;
CREATE TABLE "eiga_articledetailtype" (
    "id" serial NOT NULL PRIMARY KEY,
    "article_type_id" integer NOT NULL REFERENCES "eiga_articletype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "detail_type" varchar(30) NOT NULL
)
;
CREATE TABLE "eiga_articledetail" (
    "id" serial NOT NULL PRIMARY KEY,
    "article_id" integer NOT NULL REFERENCES "eiga_article" ("id") DEFERRABLE INITIALLY DEFERRED,
    "detail_type_id" integer NOT NULL REFERENCES "eiga_articledetailtype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "detail" varchar(200) NOT NULL
)
;
CREATE INDEX "eiga_user_userType_id" ON "eiga_user" ("userType_id");
CREATE INDEX "eiga_dvd_disc_format_id" ON "eiga_dvd" ("disc_format_id");
CREATE INDEX "eiga_film_certificate_id" ON "eiga_film" ("certificate_id");
CREATE INDEX "eiga_film_dvd_id" ON "eiga_film" ("dvd_id");
CREATE INDEX "eiga_article_article_type_id" ON "eiga_article" ("article_type_id");
CREATE INDEX "eiga_article_author_id" ON "eiga_article" ("author_id");
CREATE INDEX "eiga_article_related_film_id" ON "eiga_article" ("related_film_id");
CREATE INDEX "eiga_articledetailtype_article_type_id" ON "eiga_articledetailtype" ("article_type_id");
CREATE INDEX "eiga_articledetail_article_id" ON "eiga_articledetail" ("article_id");
CREATE INDEX "eiga_articledetail_detail_type_id" ON "eiga_articledetail" ("detail_type_id");
COMMIT;
