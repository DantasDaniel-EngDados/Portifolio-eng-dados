CREATE TABLE temperatura_media_diaria (
    id SERIAL PRIMARY KEY,
    cidade VARCHAR(100),
    data DATE,
    temperatura_media FLOAT
);

CREATE TABLE temperatura_por_cidade (
    id SERIAL PRIMARY KEY,
    cidade VARCHAR(100),
    data DATE,
    temperatura FLOAT
);
