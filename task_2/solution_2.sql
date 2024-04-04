-- Решение 2:
-- Разделение имени файла на части с помощью функции split_part
-- и сравнение на основе результата
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE split_part(full_names.name, '.', 1) = short_names.name;
