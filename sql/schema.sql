PRAGMA foreign_keys = ON;

CREATE TABLE tourguides(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname VARCHAR(20) NOT NULL,
  lastname VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  phone INTEGER NOT NULL,
  photofile VARCHAR(64) NOT NULL,
  majorone VARCHAR(40) NOT NULL,
  majortwo VARCHAR(40),
  majorthree VARCHAR(40),
  minorone VARCHAR(40),
  college VARCHAR(80),
  city VARCHAR(30) NOT NULL,
  state VARCHAR(30) NOT NULL,
  rate INTEGER NOT NULL,
  econe VARCHAR(40) NOT NULL,
  ectwo VARCHAR(40) NOT NULL,
  ecthree VARCHAR(40),
  ecfour VARCHAR(40),
  ecfive VARCHAR(40),
  currentgrade VARCHAR(20) NOT NULL,
  postgradplan VARCHAR(80) NOT NULL,
  aboutme VARCHAR(2000) NOT NULL,
  tourdescription VARCHAR(2000) NOT NULL
);

CREATE TABLE students(
  username VARCHAR(20) PRIMARY KEY,
  firstname VARCHAR(20) NOT NULL,
  lastname VARCHAR(20),
  email VARCHAR(20),
  phonenumber INTEGER,
  password VARCHAR(20)
);
