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
    InventorySlot INT DEFAULT 0
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
    pv INT,
    mana INT,
    FOREIGN KEY (PlayerID) REFERENCES Player(ID)
);

-- Objets
CREATE TABLE ObjectTest (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ObjectName VARCHAR(100) UNIQUE,
    Type ENUM('Arme', 'Artefact', 'Potion', 'Armure', 'Potions', 'Sword') DEFAULT Null,
    Strength INT DEFAULT 0,
    Defence INT DEFAULT 0,
    Effects VARCHAR(100) DEFAULT Null,
    Price INT DEFAULT 0
);

--  Inventaire des joueurs
CREATE TABLE Inventory (
    PlayerID INT,
    ObjectName VARCHAR(100),
    MaxCapacity INT DEFAULT 1,
    PRIMARY KEY (PlayerID, ObjectName),
    FOREIGN KEY (PlayerID) REFERENCES Player(ID),
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
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
    ObjectName VARCHAR(100),
    Gold INT,
    PRIMARY KEY (QuestID, ObjectName),
    FOREIGN KEY (QuestID) REFERENCES Quest(ID),
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
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
    MonsterID INT NOT NULL,
    ObjectName VARCHAR(100), 
    DropRate INT,
    Quantity INT,
    PRIMARY KEY (MonsterID, ObjectName),
    FOREIGN KEY (MonsterID) REFERENCES Bestiary(ID),
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
);
