-- Решение 2:
-- Перенос статуса с помощью паттерна,
-- проверяем на схожесть строк при помощи оператора LIKE
-- и копируем по совпадению.
INSERT INTO full_names (status)
SELECT status FROM short_names
WHERE full_names.names LIKE short_names.names + '%';
