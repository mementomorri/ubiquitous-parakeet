CREATE TABLE short_names_mock
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

CREATE TABLE full_names_mock
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

-- Имитация случайных данных в таблице short_names
INSERT INTO short_names_mock (name, status)
SELECT 'name.dummy' || GENERATE_SERIES(1, 700000), RANDOM() < 0.5;

-- Имитация случайных данных в таблице full_names
INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(1, 300000) || CASE WHEN RANDOM() < 0.5 THEN '.mp3' ELSE '.wav' END;

INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(300001, 500000) || CASE WHEN RANDOM() < 0.5 THEN '.flac' ELSE '.doc' END;

INSERT INTO full_names_mock (name)
SELECT 'name.anothername' || GENERATE_SERIES(500001, 700000) || CASE WHEN RANDOM() < 0.5 THEN '.jpg' ELSE '.png' END;

-- Копирование тпблиц для расположения элементов в случайном порядке 
CREATE TABLE short_names AS
SELECT name, status
FROM short_names_mock
ORDER BY RANDOM();

CREATE TABLE full_names AS
SELECT name, status
FROM full_names_mock
ORDER BY RANDOM();
