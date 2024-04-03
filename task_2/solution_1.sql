-- Решение 1:
-- Перенос статуса с помощью регулярного выражения,
-- регулярное выражение урезает расширение файла.
-- Затем сравнивается название файлов и на основе этого
-- переносится статус в таблицу full_names.
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE short_names.name = REGEXP_REPLACE(full_names.name, '\.[^.]*$', '');
