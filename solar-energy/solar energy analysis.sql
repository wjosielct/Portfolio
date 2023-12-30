/*
Solar Data analysis for cities on the coast from Peru.
Skills used: aggregate functions, joins, subqueries, variables, filtering aggregate values (HAVING), conditional logic (CASE), CTEs.
*/

-- 1) What years is this historical solar data based on?
SELECT
	DISTINCT(year)
FROM
	solardata
;

-- 2) How many cities are there in this database?
SELECT
	COUNT(*) AS number_of_cities
FROM
	peruviancities
;

-- 3) What is the yearly irradation for each city by tilt angle over the years?
SELECT
	city,
    angle,
    `year`,
    SUM(irradiation_tilt_month) AS irradiation_year
FROM
	peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
GROUP BY
	city,
    angle,
    `year`
ORDER BY
	city,
    angle,
    `year`
;

-- 4) What is the average yearly irradiation for each city by angle?
SELECT
	city,
    angle,
    AVG(irradiation_year) AS irradiation_year_average
FROM
	(
		SELECT
			city,
            angle,
            `year`,
            SUM(irradiation_tilt_month) AS irradiation_year
		FROM
			peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
		GROUP BY
			city,
            angle,
            `year`
	) AS tbl1
GROUP BY
	city,
    angle
ORDER BY
	city,
    angle
;
    
-- 5) What are the cities where the average yearly irradiation is above the threshold of 2000 kWh/m2 considered as relatively high?
SELECT
	DISTINCT(city)
FROM
	(
		SELECT
			city,
            angle,
            AVG(irradiation_year) AS irradiation_year_average
		FROM
			(
				SELECT
					city,
                    angle, `year`,
                    SUM(irradiation_tilt_month) AS irradiation_year
				FROM
					peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
				GROUP BY
					city,
                    angle,
                    `year`
			) AS tbl1
		GROUP BY
			city,
            angle
		HAVING
			irradiation_year_average >= 2000
	) AS tbl2
;

-- 6) How has the temperature been evolving in Chiclayo?
-- Storing the city name in a variable to easily check for other cities
SET @city_name = 'Chiclayo' COLLATE utf8mb4_unicode_ci; -- This is a variable

SELECT
	DISTINCT `year`, `month`, temp
FROM
	peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
WHERE
	city = @city_name
ORDER BY
	`year`
;

-- 7) What is best tilt angle for each city for the maximun average yearly irradiation?

-- Using a CTE (Common  Table Expression)
WITH yearly_irradiation_data AS
(
	SELECT
		city,
		angle,
		AVG(irradiation_year) AS irradiation_year_average
	FROM
		(
			SELECT
				city,
				angle,
				`year`,
				SUM(irradiation_tilt_month) AS irradiation_year
			FROM
				peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
			GROUP BY
				city,
				angle,
				`year`
		) AS tbl1
	GROUP BY
		city,
		angle
)

SELECT
	city,
    angle
FROM
	yearly_irradiation_data
WHERE
	(city, irradiation_year_average) IN
    (
		SELECT
			city,
            MAX(irradiation_year_average)
		FROM
			yearly_irradiation_data
		GROUP BY
			city
    )
ORDER BY
	city
;

-- 8) What is best tilt angle for the city of Chiclayo for each season?
-- Storing the city name in a variable to easily check for other cities
SET @city_name = 'Chiclayo' COLLATE utf8mb4_unicode_ci; -- This is a variable

-- Using a CTE (Common Table Expresion)
WITH sesonal_data AS
(
	SELECT
		angle,
        season,
        AVG(irradiation_season) AS irradiation_season_everage
	FROM
		(
			SELECT
				angle,
                `year`,
                season,
                SUM(irradiation_tilt_month) AS irradiation_season
			FROM
				(
					SELECT
						city,
                        angle,
                        `year`,
                        `month`,
                        irradiation_tilt_month,
						CASE
						WHEN `month` IN ('Jan', 'Feb', 'Mar') THEN 'Summer'
						WHEN `month` IN ('Apr', 'May', 'Jun') THEN 'Fall'
						WHEN `month` IN ('Jul', 'Aug', 'Sep') THEN 'Winter'
						WHEN `month` IN ('Oct', 'Nov', 'Dec') THEN 'Spring'
						END AS season
					FROM
						peruviancities LEFT JOIN solardata ON peruviancities.city_index = solardata.city_index
					WHERE
						city = @city_name
				) AS tbl1
			GROUP BY
				angle,
                `year`,
                season
		) AS tbl2
	GROUP BY
		angle,
        season
)

SELECT
	season,
    angle
FROM
	sesonal_data
WHERE
	(season, irradiation_season_everage) IN
    (
		SELECT
			season,
            MAX(irradiation_season_everage)
		FROM
			sesonal_data
		GROUP BY
			season
    )
;