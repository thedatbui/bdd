DROP DATABASE IF EXISTS InventaireRPG;
CREATE DATABASE InventaireRPG;
USE InventaireRPG;

--  Joueurs
CREATE TABLE Player (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50) UNIQUE NOT NULL,
    PlayerLevel INT DEFAULT 1,
    ExperiencePoints INT DEFAULT 0,
    WalletCredits INT DEFAULT 0,
    InventorySlots INT DEFAULT 0
);

--  Personnages créés par les joueurs
CREATE TABLE `Character` (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerID INT,
    CharacterName VARCHAR(50),
    Class ENUM("Assassin", "Archer", "Barbare", "Berserker", "Chasseur","Chevalier", "Démoniste", "Druide", "Enchanteresse", "Guerrier","Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin","Prêtresse", "Rôdeur", "Sorcière", "Templier"),
    Strength INT,
    Agility INT,
    Intelligence INT,
    FOREIGN KEY (PlayerID) REFERENCES Player(ID)
);

-- Objets
CREATE TABLE Object (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ObjectName VARCHAR(100),
    Type ENUM('Arme', 'Artefact', 'Potion', 'Armure'),
    Strength INT,
    Defence INT,
    Effects VARCHAR(100),
    Price INT
);

--  Inventaire des joueurs
CREATE TABLE Inventory (
    PlayerID INT,
    ObjectID INT,
    MaxCapacity INT DEFAULT 1,
    PRIMARY KEY (PlayerID, ObjectID),
    FOREIGN KEY (PlayerID) REFERENCES Player(ID),
    FOREIGN KEY (ObjectID) REFERENCES Object(ID)
);

--  PNJ
CREATE TABLE NPC (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NpcName VARCHAR(50),
    Dialogue TEXT
);

--  Quêtes
CREATE TABLE Quest (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    QuestName VARCHAR(100),
    Description TEXT,
    DifficultyLevel INT,
    RewardXP INT,
    RewardGold INT
);

--  Objets récompensés par des quêtes
CREATE TABLE Quest_Objects (
    QuestID INT,
    ObjectID INT,
    PRIMARY KEY (QuestID, ObjectID),
    FOREIGN KEY (QuestID) REFERENCES Quest(ID),
    FOREIGN KEY (ObjectID) REFERENCES Object(ID)
);

--  Monstres
CREATE TABLE Bestiary (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    BeastName VARCHAR(50),
    Attribute VARCHAR(50),
    Attack INT,
    Defence INT,
    LifePoints INT
);

--  Récompenses obtenues sur les monstres
CREATE TABLE Rewards (
    MonsterID INT,
    ObjectID INT,
    DropRate INT,
    PRIMARY KEY (MonsterID, ObjectID),
    FOREIGN KEY (MonsterID) REFERENCES Bestiary(ID),
    FOREIGN KEY (ObjectID) REFERENCES Object(ID)
);
