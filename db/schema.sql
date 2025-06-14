DROP DATABASE IF EXISTS InventaireRPG;
CREATE DATABASE InventaireRPG;
USE InventaireRPG;

--  Joueurs
CREATE TABLE Player (
    ID               INT AUTO_INCREMENT PRIMARY KEY,
    UserName         VARCHAR(50)  UNIQUE NOT NULL,
    PlayerLevel      INT          DEFAULT 1,
    ExperiencePoints INT          DEFAULT 0,
    WalletCredits    INT          DEFAULT 0 CHECK (WalletCredits >= 0),
    InventorySlot    INT          DEFAULT 10
);


--  Personnages créés par les joueurs
CREATE TABLE CharacterTable (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerID INT,
    CharacterName VARCHAR(50),
    Class ENUM("Assassin", "Archer", "Barbare", "Berserker", "Chasseur", "Chevalier", "Démoniste", "Druide", "Enchanteresse", "Guerrier","Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin","Prêtresse", "Rôdeur", "Sorcière", "Templier", "Voleur"),
    Strength INT,
    Agility INT,
    Intelligence INT,
    pv INT,
    mana INT,
    AttributePoints INT DEFAULT 0,
    Quest_In_Progress VARCHAR(100) DEFAULT NULL,
    FOREIGN KEY (PlayerID) REFERENCES Player(ID) ON DELETE CASCADE
);

CREATE TABLE CharacterQuest (
    CharacterID INT,
    QuestName VARCHAR(100),
    BeastName VARCHAR(50),
    killNumber INT DEFAULT 0,
    BeastKilled INT DEFAULT 0,
    PRIMARY KEY (CharacterID, QuestName, BeastName),
    FOREIGN KEY (CharacterID) REFERENCES CharacterTable(ID) ON DELETE CASCADE
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
    CharacterID INT,
    ObjectName VARCHAR(100),
    MaxCapacity INT DEFAULT 1,
    Quantity INT DEFAULT 1,
    PRIMARY KEY (PlayerID, CharacterID, ObjectName),
    FOREIGN KEY (PlayerID) REFERENCES Player(ID) ON DELETE CASCADE,
    FOREIGN KEY (CharacterID) REFERENCES CharacterTable(ID) ON DELETE CASCADE,
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
);

--  PNJ
CREATE TABLE NPC (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NpcName VARCHAR(50),
    Dialogue TEXT,
    Type VARCHAR(50)
);

--  Quêtes disponibles dans le jeu.
CREATE TABLE Quest (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    QuestName VARCHAR(100),
    Description VARCHAR(500),
    DifficultyLevel INT,
    RewardXP INT
);

--  Objets récompensés par des quêtes
CREATE TABLE Quest_Objects (
    QuestID INT,
    ObjectName VARCHAR(100),
    Quantity INT,
    PRIMARY KEY (QuestID, ObjectName),
    FOREIGN KEY (QuestID) REFERENCES Quest(ID) ON DELETE CASCADE,
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
    FOREIGN KEY (MonsterID) REFERENCES Bestiary(ID) ON DELETE CASCADE,
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
);

-- Or des monstres
CREATE TABLE MonsterGold (
    MonsterID INT NOT NULL,
    GoldAmount INT NOT NULL,
    DropRate INT NOT NULL,
    PRIMARY KEY (MonsterID),
    FOREIGN KEY (MonsterID) REFERENCES Bestiary(ID) ON DELETE CASCADE
);

-- Or des quêtes
CREATE TABLE QuestGold (
    QuestID INT NOT NULL,
    GoldAmount INT NOT NULL,
    PRIMARY KEY (QuestID),
    FOREIGN KEY (QuestID) REFERENCES Quest(ID) ON DELETE CASCADE
);

-- PNJ ↔ Quêtes
CREATE TABLE NPCQuest (
    NPCID INT,
    QuestName VARCHAR(100),
    PRIMARY KEY (NPCID, QuestName),
    FOREIGN KEY (NPCID) REFERENCES NPC(ID) ON DELETE CASCADE
);

-- PNJ ↔ Objets
CREATE TABLE NPCInventory (
    NPCID INT,
    ObjectName VARCHAR(100),
    Quantity INT DEFAULT 1,
    FOREIGN KEY (NPCID) REFERENCES NPC(ID) ON DELETE CASCADE,
    FOREIGN KEY (ObjectName) REFERENCES ObjectTest(ObjectName)
);
