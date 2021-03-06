DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Deck CASCADE;
DROP TABLE IF EXISTS Card;
DROP TABLE IF EXISTS Settings;

CREATE TABLE Users(
  id SERIAL PRIMARY KEY,
  login TEXT UNIQUE NOT NULL,
  password_hash TEXT
);

CREATE TABLE Deck(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  user_id INT NOT NULL REFERENCES Users
);

CREATE TABLE Card(
  id SERIAL PRIMARY KEY,
  word TEXT NOT NULL,
  translation TEXT NOT NULL,
  context TEXT,
  deck_id INT NOT NULL REFERENCES Deck
);

CREATE TABLE Settings(
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES Users,
  language TEXT NOT NULL
);

INSERT INTO Users(login) VALUES ('Public');
INSERT INTO Deck(name, user_id) VALUES ('Public deck', (SELECT id FROM Users WHERE login = 'Public'));
