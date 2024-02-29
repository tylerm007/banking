
--
-- Current Schema: banking
--

-- create database ontimize;
-- create user demo with encrypted password 'demouser';
-- grant all privileges on database ontimize to demo;

-- ApiLogicServer create --project_name=ontimize --db_url=postgresql://demo:demouser@localhost/ontimize
--
-- Table structure for table Account
--


--
-- Table structure for table AccountType
--

DROP TABLE IF EXISTS "AccountType";


CREATE TABLE "AccountType" (
  "AcctID" SERIAL primary key,
  "NAME" varchar(25) NOT NULL
);

--
-- Dumping data for table AccountType
--


INSERT INTO "AccountType" VALUES (1,'Checking'),(2,'Savings');

--
-- Table structure for table Branch
--

DROP TABLE IF EXISTS "Branch";


CREATE TABLE "Branch" (
  "OFFICEID" SERIAL primary key,
  "NAME" varchar(100) DEFAULT NULL,
  "ADDRESS" varchar(100) DEFAULT NULL,
  "STARTDATE" DATE DEFAULT NULL
);


--
-- Dumping data for table Branch
--


INSERT INTO "Branch" VALUES (3,'Bedfordview Pri15641456165v BNKG Suite sc','Priority House 5 Iris Road Bedfordview Gauteng','2024-02-24 00:00:00'),(4,'Bultfontein Service Centre','President Swart Street Bultfontein','2024-02-24 00:00:00'),(70,'Westridge Park Service Centre','Shop 69 Westridge Park sc.','2024-02-24 00:00:00'),(101,'Jozi ','Centro City 11 Trump st.','2024-02-24 00:00:00'),(102,'Majadahonda','Sta. María de la Cabeza, esq. Dr. Calero 2822','2024-02-24 00:00:00'),(103,'Torrejón','Pl. Mayor, 10 (28850) Torrejón Ardoz','2024-02-24 00:00:00'),(1471,'ImatiaBank Innovation','Edificio Citexvi, Fonte das Abelleiras, s/n · Local 27, 36310 Vigo, Pontevedra','2024-02-24 00:00:00'),(3200,'Pepesfg','Plaza España','2024-02-24 00:00:00'),(123124,'test','RUA ITAQUARI 180 apt 1302','2024-02-24 00:00:00');


--
-- Table structure for table Customer
--

DROP TABLE IF EXISTS "Customer";


CREATE TABLE "Customer" (
  "CUSTOMERID" SERIAL primary key,
  "NAME" varchar(75) DEFAULT NULL,
  "SURNAME" varchar(75) DEFAULT NULL,
  "EMAIL" varchar(100) DEFAULT NULL,
  "ADDRESS" varchar(200) DEFAULT NULL,
  "STARTDATE" DATE DEFAULT NULL,
  "OFFICEID" INTEGER DEFAULT '1',
  "PHOTO" TEXT,
  CONSTRAINT CustomerInBranchFK FOREIGN KEY ("OFFICEID") REFERENCES "Branch" ("OFFICEID")
);


--
-- Dumping data for table Customer
--


INSERT INTO "Customer" VALUES (10602,'James','Alan','james.alan@alan.inc','13, Downing Street','2024-02-24 00:00:00',3,NULL),(10604,'Markus','Bugle','Mark.Bugle@ontimize.com','22 Holloway Road','2024-02-24 00:00:00',3,NULL),(10606,'Tomás Miguel','Baños Márquez','','Al. Huerto los Mortolitos, Totana ','2024-02-24 00:00:00',3,NULL),(10607,'Lidya Esther','Buendía Lorente','','C/ Carlos III, 63 - 7.a A, Cartagena','2024-02-24 00:00:00',3,NULL),(10808,'Billy','Buttercup','Billy.Buttercup@ontimize.com','2 The Piazza','2024-02-24 00:00:00',3,NULL),(10810,'Marie','C.Johnson','marie.johnson@gmail.com','57 Great Marlborough Street, London','2024-02-24 00:00:00',3,NULL),(10811,'Pablo','Fernández Blanco','pablo.fernandez@yahoo.es','C/Barcelona s/n','2024-02-24 00:00:00',3,NULL),(10815,'Bridget','Corbirock','Bridget.Corbirock@yahoo.com','43 Carnaby Street','2024-02-24 00:00:00',3,NULL),(10834,'John','Green','','3 Oxford Street','2024-02-24 00:00:00',3,NULL),(19271,'Aubrey','Engels','Aubrey.Engels@ontimize.com','Tidorestraat 58-128','2024-02-24 00:00:00',4,NULL),(19320,'Heidi','Fischer','Heidi.Fischer@Imatia.com','Glacischaussee 20','2024-02-24 00:00:00',3,NULL),(19336,'Marlene','De Jong','Marlene.DeJong@Imatia.com','12 Rue Marbeau','2024-02-24 00:00:00',3,NULL),(19337,'Louise','Bakker','Louise.Bakker@Imatia.com','Marsopstrasse 2','2024-02-24 00:00:00',3,NULL),(19343,'Jeanne','Galouzeau','Jeanne.Galouzeau@Imatia.com','70 Rue de Miromesnil','2024-02-24 00:00:00',3,NULL),(19352,'Elektra','Christopoulos','Elektra.Christopoulos@Ontimize.com','Paikou 4','2024-02-24 00:00:00',3,NULL),(19359,'Juan','Dominguez ','Juan.Dom@Ontimize.com','Calle de Iparraguirre, 42','2024-02-24 00:00:00',3,NULL),(19362,'Philippe','Brown','Brown@gmail.com','Rosebank Rd 15','2024-02-24 00:00:00',3,NULL),(19363,'Michael','Calaghan','Michael.Calaghan@gmail.com','154-168 Boswall Pkwy, Edinburgh, City of Edinburgh EH5 2','2024-02-24 00:00:00',3,NULL),(19364,'Suez','Ashworth','Sue.Ashworth@Ontimize.com','Nymphenburger Strasse 55','2024-02-24 00:00:00',3,NULL),(19365,'Wing','Andersen','Wing.Andersen@gmail.com','56 Gurranebraher Ave','2024-02-24 00:00:00',3,NULL),(19527,'David','Blanco Balado','ddddde@gmail.com','Cddddd 89','2024-02-24 00:00:00',3,NULL),(19530,'Ruli','Cristobal','Holahola@gmail.com','calle imaginaria 123','2024-02-24 00:00:00',3,NULL),(19532,'Jimmy','Butler','jimmybuckets@gmail.com',NULL,'2024-02-24 00:00:00',3,NULL),(19534,'Michael','Fassbender','fassbender@gmail.com','Massachussets','2024-02-24 00:00:00',3,NULL),(19535,'Patata','Asada',NULL,NULL,'2024-02-24 00:00:00',3,NULL);


DROP TABLE IF EXISTS "Account";

CREATE TABLE "Account" (
  "ACCOUNTID" SERIAL primary key,
  "CUSTOMERID" INTEGER DEFAULT NULL,
  "ACCOUNTTYPEID" INTEGER DEFAULT NULL,
  "ACCOUNTTYPENAME" varchar(25) DEFAULT NULL,
  "BALANCE" NUMERIC(15,2) DEFAULT '0.00',
  "STARTDATE" DATE DEFAULT NULL,
  "ENDDATE" DATE DEFAULT NULL,
  "ENTITYID" INTEGER DEFAULT '1',
  "OFFICEID" INTEGER DEFAULT '1',
  "CDID" varchar(25) DEFAULT NULL,
  "ANID" varchar(25) DEFAULT NULL,
  "INTERESRATE" NUMERIC(15,2) DEFAULT '0.00',
  CONSTRAINT AccountTypeFK FOREIGN KEY ("ACCOUNTTYPEID") REFERENCES "AccountType" ("AcctID"),
  CONSTRAINT CustomerHasAccountFK FOREIGN KEY ("CUSTOMERID") REFERENCES "Customer" ("CUSTOMERID")
) ;


--
-- Dumping data for table Account
--

INSERT INTO "Account" VALUES (6,10602,1,'Checking',1001.00,'2024-02-24 00:00:00',NULL,1,1,NULL,NULL,0.00),(7,10602,2,'Savings',99.00,'2024-02-24 00:00:00','2024-02-27 09:33:49',1,1,NULL,NULL,0.00);


--
-- Table structure for table Employees
--

DROP TABLE IF EXISTS "Employees";


CREATE TABLE "Employees" (
  "EMPLOYEEID" SERIAL primary key,
  "EMPLOYEETYPEID" INTEGER DEFAULT '1',
  "EMPLOYEESURNAME" varchar(15) NOT NULL,
  "EMPLOYEENAME" varchar(15) NOT NULL,
  "OFFICEID" INTEGER DEFAULT '1',
  "EMPLOYEEADDRESS" varchar(100) DEFAULT NULL,
  "EMPLOYEESTARTDATE" DATE DEFAULT CURRENT_TIMESTAMP,
  "EMPLOYEEPHOTOTO" TEXT,
  "NAME" varchar(100) DEFAULT NULL,
  "EMPLOYEEPHONE" varchar(50) DEFAULT NULL,
  CONSTRAINT EmployeeWorksInBranch FOREIGN KEY ("OFFICEID") REFERENCES "Branch" ("OFFICEID")
);

--
-- Dumping data for table Employees
--


INSERT INTO "Employees" VALUES (6378,1,'Robinson','Mark',3,'12 Brompton Road Knightsbridge. London UK','2024-02-24 00:00:00',NULL,NULL,'0500 430994'),(6379,1,'Smith','Caroline',3,'12 Brixton Road, London. United Kingdom‎','2024-02-24 00:00:00',NULL,NULL,'0845 46 40'),(6539,1,'Periwinkle','Christopher',3,'25 Mortimer Street. London','2024-02-24 00:00:00',NULL,NULL,'(010444) 11899'),(6741,1,'Burdock','Claudy',3,'25 Regent Street. London','2024-02-24 00:00:00',NULL,NULL,'07624 175096'),(6840,1,'Doyle','Antony',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'070 6145 6297'),(6841,1,'Novotny','Cameron',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'055 5182 6835'),(6842,1,'Looper','Christopher',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'07624 810266'),(6843,1,'Anderson','Cecile',3,'46th & 48th Street, 156 Avenue, San Andres Colony. London','2024-02-24 00:00:00',NULL,NULL,'055 9055 6294'),(6844,1,'Anderson','Cheryl',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0845 46 48'),(6845,1,'Legendre','Charlotte',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0898 547 2304'),(6846,1,'Singht','Curtis',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'055 3676 5432'),(6890,1,'Lemacks','Craig',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0800 570661'),(6891,1,'Butt','James',3,'John B Jr','2024-02-24 00:00:00',NULL,NULL,'07624 817175'),(6892,1,'Darakjy','Josephine',3,'Jeffrey A Esq','2024-02-24 00:00:00',NULL,NULL,'0800 177 7086'),(6893,1,'Venere','Art',3,'James L Cpa','2024-02-24 00:00:00',NULL,NULL,'(016977) 4951'),(6894,1,'Paprocki','Lenna',3,'639 Main St','2024-02-24 00:00:00',NULL,NULL,'0898 148 8226');


--
-- Table structure for table Transaction
--

DROP TABLE IF EXISTS "Transaction";


CREATE TABLE "Transaction" (
  "TransactionID" SERIAL primary key,
  "AccountID" INTEGER DEFAULT NULL,
  "TransactionType" VARCHAR(25) DEFAULT NULL,
  "TotalAmount" NUMERIC(15,2) DEFAULT '0.00',
  "Deposit" NUMERIC(15,2) DEFAULT '0.00',
  "Withdrawl" NUMERIC(15,2) DEFAULT '0.00',
  "ItemImage" text,
  "TransactionDate" DATE DEFAULT NULL,
  CONSTRAINT Transaction_ibfk_1 FOREIGN KEY ("AccountID") REFERENCES "Account" ("ACCOUNTID")
);

--
-- Dumping data for table Transaction
--


INSERT INTO "Transaction" VALUES (1,6,'Deposit',1000.00,1000.00,0.00,NULL,'2024-02-24 00:00:00'),(2,7,'Deposit',100.00,100.00,0.00,NULL,'2024-02-24 00:00:00'),(4,7,'Withdrawal',-1.00,0.00,1.00,NULL,'2024-02-24 00:00:00'),(5,6,'Deposit',1.00,1.00,0.00,NULL,'2024-02-24 00:00:00');

--
-- Table structure for table Transfer
--

DROP TABLE IF EXISTS "Transfer";


CREATE TABLE "Transfer" (
  "TransactionID" SERIAL primary key,
  "FromAccountID" INTEGER DEFAULT NULL,
  "ToAccountID" INTEGER DEFAULT NULL,
  "Amount" NUMERIC(15,2) DEFAULT '0.00',
  TransactionDate DATE DEFAULT NULL,
  CONSTRAINT FromAccount FOREIGN KEY ("FromAccountID") REFERENCES "Account" ("ACCOUNTID"),
  CONSTRAINT ToAccount FOREIGN KEY ("ToAccountID") REFERENCES "Account" ("ACCOUNTID")
) ;

--
-- Dumping data for table Transfer
--


INSERT INTO "Transfer" VALUES (1,7,6,1.00,'2024-02-24 00:00:00');

