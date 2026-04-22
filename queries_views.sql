--Query 1
-- View 1: Legal rental contracts
-- A legal rental contract is one where the owner was 18+ when the contract started
CREATE VIEW LegalRentals AS
SELECT r.renterID, r.rYear, r.aID, r.cost
FROM Rentals r
JOIN Apartments a ON r.aID = a.aID
JOIN Owners o ON a.ownerID = o.ownerID
WHERE r.rYear - YEAR(o.bDate) >= 18;

-- View 2: Legal owners (owners who have only legal rental contracts)
CREATE VIEW LegalOwners AS
SELECT DISTINCT o.ownerID
FROM Owners o
EXCEPT
SELECT DISTINCT a.ownerID
FROM Apartments a JOIN
Rentals r ON a.aID = r.aID
WHERE NOT EXISTS
(SELECT 1
FROM LegalRentals lr
WHERE lr.renterID = r.renterID
AND lr.rYear = r.rYear
AND lr.aID = lr.aID );

-- View 3: Apartments that were rented for 3 years or less
CREATE VIEW ApartmentsRentedMax3Years AS
SELECT aID
FROM Rentals
GROUP BY aID
HAVING COUNT(DISTINCT rYear) <= 3;

-- View 4: Maximum cost per apartment with renter details
CREATE VIEW MaxCostPerApartment AS
SELECT r.aID, r.renterID, r.cost
FROM Rentals r
WHERE r.cost = (
    SELECT MAX(r2.cost)
    FROM Rentals r2
    WHERE r2.aID = r.aID
);
------
------Query 2
-- View 1: Minimalist Owners
-- Owner who has 3 or fewer renters per apartment per year (or no rentals at all)
CREATE VIEW MinimalistOwners AS
SELECT DISTINCT o.ownerID
FROM Owners o
WHERE NOT EXISTS (
    SELECT 1
    FROM Apartments a
    WHERE a.ownerID = o.ownerID
    AND EXISTS (
        SELECT r.aID, r.rYear
        FROM Rentals r
        WHERE r.aID = a.aID
        GROUP BY r.aID, r.rYear
        HAVING COUNT(r.renterID) > 3
    )
);

-- View 2: Minimalist Renters
-- Renter who never paid more than 2000 per month AND never lived alone
CREATE VIEW MinimalistRenters AS
SELECT DISTINCT r1.renterID
FROM Rentals r1
WHERE NOT EXISTS (
    -- Never paid more than 2000
    SELECT 1
    FROM Rentals r2
    WHERE r2.renterID = r1.renterID
    AND r2.cost > 2000
)
AND NOT EXISTS (
    -- Never lived alone (always had roommates)
    SELECT 1
    FROM Rentals r3
    WHERE r3.renterID = r1.renterID
    AND NOT EXISTS (
        SELECT 1
        FROM Rentals r4
        WHERE r4.aID = r3.aID
        AND r4.rYear = r3.rYear
        AND r4.renterID != r3.renterID
    )
);
-- View 3: Rentals by Minimalist Renters from Minimalist Owners
CREATE VIEW MinimalistRentals AS
SELECT DISTINCT r.aID, r.renterID
FROM Rentals r
JOIN MinimalistRenters mr ON r.renterID = mr.renterID
JOIN Apartments a ON r.aID = a.aID
JOIN MinimalistOwners mo ON a.ownerID = mo.ownerID;
---
--Query 3
-- View 1: Diverse Owners
-- Owner with at least one apartment, all apartments in different cities,
-- none in the city where owner lives
CREATE VIEW DiverseOwners AS
SELECT DISTINCT o.ownerID
FROM Owners o
WHERE EXISTS (
    -- Has at least one apartment
    SELECT 1 FROM Apartments a WHERE a.ownerID = o.ownerID
)
AND NOT EXISTS (
    -- No apartment in owner's residence city
    SELECT 1
    FROM Apartments a
    WHERE a.ownerID = o.ownerID
    AND a.city = o.residenceCity
)
AND NOT EXISTS (
    -- No two apartments in the same city
    SELECT 1
    FROM Apartments a1, Apartments a2
    WHERE a1.ownerID = o.ownerID
    AND a2.ownerID = o.ownerID
    AND a1.aID != a2.aID
    AND a1.city = a2.city
);

-- View 2: Problematic Renters
-- Renter who never lived with the same roommate twice
CREATE VIEW ProblematicRenters AS
SELECT DISTINCT r1.renterID
FROM Rentals r1
WHERE NOT EXISTS (
    -- Check if this renter ever lived with the same roommate twice
    SELECT 1
    FROM Rentals r2, Rentals r3, Rentals r4, Rentals r5
    WHERE r2.renterID = r1.renterID              -- first rental of our renter
    AND r3.renterID = r1.renterID                -- second rental of our renter
    AND r4.renterID != r1.renterID               -- roommate in first rental
    AND r5.renterID = r4.renterID                -- same roommate in second rental
    AND r2.aID = r4.aID AND r2.rYear = r4.rYear  -- roommate shares first apartment-year
    AND r3.aID = r5.aID AND r3.rYear = r5.rYear  -- same roommate shares second apartment-year
    AND (r2.aID != r3.aID OR r2.rYear != r3.rYear)  -- different apartment-year combinations
);

