-- Cleaning the DimProduct
SELECT
	P.[ProductKey],
	P.[ProductAlternateKey] AS [Product Code],
	SC.[EnglishProductSubcategoryName] AS [Product Subcategory], -- This comes from the Subcategory table
	C.[EnglishProductCategoryName] AS [Product Category], -- This comes from the Category table
	--[WeightUnitMeasureCode],
	--[SizeUnitMeasureCode],
	P.[EnglishProductName] AS [Product Name],
	--[SpanishProductName],
	--[FrenchProductName],
	--[StandardCost],
	--[FinishedGoodsFlag],
	P.[Color] AS [Product Color],
	--[SafetyStockLevel],
	--[ReorderPoint],
	--[ListPrice],
	P.[Size] AS [Product Size],
	--[SizeRange],
	--[Weight],
	--[DaysToManufacture],
	P.[ProductLine] AS [Product Line],
	--[DealerPrice],
	--[Class],
	--[Style],
	P.[ModelName] AS [Model Name],
	--[LargePhoto],
	P.[EnglishDescription] AS [Product Description],
	--[FrenchDescription],
	--[ChineseDescription],
	--[ArabicDescription],
	--[HebrewDescription],
	--[ThaiDescription],
	--[GermanDescription],
	--[JapaneseDescription],
	--[TurkishDescription],
	--[StartDate],
	--[EndDate],
	ISNULL(P.[Status], 'Outdate') AS [Product Status]
FROM
	[AdventureWorksDW2022].[dbo].[DimProduct] AS P
	LEFT JOIN
	[AdventureWorksDW2022].[dbo].[DimProductSubcategory] AS SC
	ON P.[ProductSubcategoryKey] = SC.[ProductSubcategoryKey]
	LEFT JOIN
	[AdventureWorksDW2022].[dbo].[DimProductCategory] AS C
	ON SC.[ProductCategoryKey] = C.[ProductCategoryKey]