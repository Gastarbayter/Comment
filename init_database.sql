CREATE TABLE IF NOT EXISTS Region (
    id     INTEGER        PRIMARY KEY AUTOINCREMENT  NOT NULL,
    region VARCHAR (300) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS City (
    id        INTEGER        PRIMARY KEY AUTOINCREMENT NOT NULL,
    region_id INTEGER        NOT NULL,
    city      VARCHAR (300) DEFAULT NULL,
    FOREIGN KEY (region_id) REFERENCES Region (id) 
);

CREATE TABLE IF NOT EXISTS Comment (
    id             INTEGER        PRIMARY KEY AUTOINCREMENT NOT NULL,
    surname        VARCHAR (150) NOT NULL,
    name           VARCHAR (150) NOT NULL,
    patronymic     VARCHAR (150) DEFAULT NULL,
    city_id        INTEGER        NOT NULL,
    contact_number VARCHAR (12)   DEFAULT NULL,
    e_mail         VARCHAR (50)   DEFAULT NULL,
    comment        VARCHAR (1000) NOT NULL,
    FOREIGN KEY (city_id )    REFERENCES City (id) 
);

INSERT INTO Region (region)
VALUES ('Краснодарский край'),
       ('Ростовская область'),
       ('Ставропольский край');
       
INSERT INTO City (region_id, city)
VALUES ((SELECT id FROM Region WHERE Region.region = 'Краснодарский край' ),'Краснодар' ),
     ((SELECT id FROM Region WHERE Region.region = 'Краснодарский край'),'Кропоткин' ),
     ((SELECT id FROM Region WHERE Region.region = 'Краснодарский край'),'Славянск' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ростовская область'),'Ростов' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ростовская область'),'Шахты' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ростовская область'),'Батайск' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ставропольский край'),'Ставрополь' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ставропольский край'),'Пятигорск' ),
     ((SELECT id FROM Region WHERE Region.region = 'Ставропольский край'),'Кисловодск' );
 