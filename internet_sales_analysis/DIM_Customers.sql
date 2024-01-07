-- Cleaning the DimCustomer

SELECT
	C.[CustomerKey],
	--C.[GeographyKey],
	--[CustomerAlternateKey],
	--[Title],
	C.[FirstName],
	--[MiddleName],
	C.[LastName],
	CONCAT(C.[FirstName], ' ', C.[LastName]) AS [FullName],
	--[NameStyle],
	C.[BirthDate],
	CASE
		WHEN C.[MaritalStatus] = 'S' THEN 'Single'
		WHEN C.[MaritalStatus] = 'M' THEN 'Married'
	END AS [MaritalStatus],
	--[Suffix],
	CASE
		WHEN C.[Gender] = 'M' THEN 'Male'
		WHEN C.[Gender] = 'F' THEN 'Female'
	END AS [Gender],
	--[EmailAddress],
	C.[YearlyIncome],
	--[TotalChildren],
	--[NumberChildrenAtHome],
	--[EnglishEducation],
	--[SpanishEducation],
	--[FrenchEducation],
	--[EnglishOccupation],
	--[SpanishOccupation],
	--[FrenchOccupation],
	--[HouseOwnerFlag],
	--[NumberCarsOwned],
	--[AddressLine1],
	--[AddressLine2],
	--[Phone],
	C.[DateFirstPurchase],
	--[CommuteDistance],
	G.City,
	G.EnglishCountryRegionName AS [Country]
FROM
	[AdventureWorksDW2022].[dbo].[DimCustomer] AS C
	LEFT JOIN
	[AdventureWorksDW2022].[dbo].[DimGeography] AS G
	ON C.GeographyKey = G.GeographyKey
ORDER BY
	[CustomerKey] ASC