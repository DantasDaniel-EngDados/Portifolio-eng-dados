SELECT cidade,data, AVG(temperatura_media)
FROM temperatura_media_diaria
GROUP BY cidade,data;