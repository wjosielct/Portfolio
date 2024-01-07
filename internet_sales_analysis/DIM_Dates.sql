-- Cleaning the DimDate

SELECT
	[DateKey],
	[FullDateAlternateKey] AS Date,
	[DayNumberOfWeek] AS DayOfWeek,
	[EnglishDayNameOfWeek] AS Day,
	--[SpanishDayNameOfWeek],
	--[FrenchDayNameOfWeek],
	[DayNumberOfMonth] AS DayNumber,
	--[DayNumberOfYear],
	--[WeekNumberOfYear],
	[EnglishMonthName] AS Month,
	LEFT([EnglishMonthName], 3) AS MonthShort,
	--[SpanishMonthName],
	--[FrenchMonthName],
	[MonthNumberOfYear] AS MonthNumber,
	[CalendarQuarter] AS Quarter,
	[CalendarYear] AS Year,
	[CalendarSemester] AS Semester
	--[FiscalQuarter],
	--[FiscalYear],
	--[FiscalSemester]
FROM
	[AdventureWorksDW2022].[dbo].[DimDate]
