CREATE TABLE Owners (
    ownerID INT PRIMARY KEY,
    oName VARCHAR(50),
    residenceCity VARCHAR(50),
    bDate Date
);

CREATE TABLE Apartments (
    aID INT PRIMARY KEY,
    city VARCHAR(50),
    roomsNum INT,
    ownerID INT NOT NULL,
    FOREIGN KEY (ownerID) REFERENCES Owners
);

CREATE TABLE Rentals (
    renterID INT,
    rYear INT,
    aID INT NOT NULL,
    cost INT,
    PRIMARY KEY (renterID, rYear),
    FOREIGN KEY (aID) REFERENCES Apartments(aID)
);

