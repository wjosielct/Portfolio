-- Cleaning the FactInternetSales
SELECT
	[ProductKey],
	[OrderDateKey],
	[DueDateKey],
	[ShipDateKey],
	[CustomerKey],
	--[PromotionKey],
	--[CurrencyKey],
	--[SalesTerritoryKey],
	--[SalesOrderNumber],
	--[SalesOrderLineNumber],
	--[RevisionNumber],
	--[OrderQuantity],
	--[UnitPrice],
	--[ExtendedAmount],
	--[UnitPriceDiscountPct],
	--[DiscountAmount],
	--[ProductStandardCost],
	--[TotalProductCost],
	[SalesAmount] AS [Sales Amount]
	--[TaxAmt],
	--[Freight],
	--[CarrierTrackingNumber],
	--[CustomerPONumber],
	--[OrderDate],
	--[DueDate],
	--[ShipDate]
FROM
	[AdventureWorksDW2022].[dbo].[FactInternetSales]
WHERE
	YEAR([OrderDate]) >= 2021 -- Bringing only orders starting from 2021
ORDER BY
	[OrderDateKey] ASC