
--
-- Current Database: "authdb"

--

-- CREATE DATABASE "authdb"
-- create user root with encrypted password 'password';
-- grant all privileges on database authdb to root;


--
-- Table structure for table "Role"
--

DROP TABLE IF EXISTS "Role";


CREATE TABLE "Role" (
  "name" varchar(64) NOT NULL,
  PRIMARY KEY ("name")
);


--
-- Dumping data for table "Role"
--

INSERT INTO "Role" VALUES ('CS_ADMIN'),('fullaccess'),('tenant');

--
-- Table structure for table "UserRole"
--


--
-- Table structure for table "Users"
--

DROP TABLE IF EXISTS "Users";

CREATE TABLE "Users" (
  "name" varchar(128) DEFAULT NULL,
  "notes" text,
  "id" varchar(64) NOT NULL,
  "username" varchar(128) DEFAULT NULL,
  "email" varchar(128) DEFAULT NULL,
  "password_hash" varchar(200) DEFAULT NULL,
  "client_id" int DEFAULT NULL,
  PRIMARY KEY ("id")
);


--
-- Dumping data for table "Users"
--
INSERT INTO "Users" VALUES ('Administrator',NULL,'admin','Admin User','admin@corp.com','password',1003),('demo','demo','demo','demo@gmail.com','demouser','demouser',1),('sam','','sam','Sam','samn@farms.com','password',1038),('ty',NULL,'ty','tyler',NULL,'$2b$12$g6Q17yPJUUEaYuD22/joS.MtP4OXEe3OP831Yu1CBOG5qfbLx5Cj2',1038);


DROP TABLE IF EXISTS "UserRole";

CREATE TABLE "UserRole" (
  "user_id" varchar(64) NOT NULL,
  "notes" text,
  "role_name" varchar(32) NOT NULL,
  PRIMARY KEY ("user_id","role_name"),
  CONSTRAINT "in_client" FOREIGN KEY ("user_id") REFERENCES "Users" ("id") ON DELETE CASCADE,
  CONSTRAINT "in_role" FOREIGN KEY ("role_name") REFERENCES "Role" ("name") ON DELETE CASCADE
);


--
-- Dumping data for table "UserRole"
--
INSERT INTO "UserRole" VALUES ('admin',NULL,'CS_ADMIN'),('admin',NULL,'fullaccess'),('demo','','CS_ADMIN'),('sam','','fullaccess'),('ty',NULL,'CS_ADMIN'),('ty',NULL,'fullaccess');
