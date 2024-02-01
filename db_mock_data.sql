INSERT INTO users (username, password, email, created_at, roles) VALUES ('testikayttaja1', 'salasana123', 'testi1@gmail.com', NOW(), '{"myyja"}') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email, created_at, roles) VALUES ('testikayttaja2', 'salasana123', 'testi2@gmail.com', NOW(), '{"myyja"}') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email, created_at, roles) VALUES ('testikayttaja3', 'salasana123', 'testi3@gmail.com', NOW(), '{"myyja"}') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email, created_at, roles) VALUES ('testikayttaja4', 'salasana123', 'testi4@gmail.com', NOW(), '{"myyja"}') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email, created_at, roles) VALUES ('testikayttaja5', 'salasana123', 'testi5@gmail.com', NOW(), '{"myyja"}') ON CONFLICT DO NOTHING;

INSERT INTO sellers (user_id, name) VALUES (1, 'testimyyja1') ON CONFLICT DO NOTHING;
INSERT INTO sellers (user_id, name) VALUES (2, 'testimyyja2') ON CONFLICT DO NOTHING;
INSERT INTO sellers (user_id, name) VALUES (3, 'testimyyja3') ON CONFLICT DO NOTHING;
INSERT INTO sellers (user_id, name) VALUES (4, 'testimyyja4') ON CONFLICT DO NOTHING;
INSERT INTO sellers (user_id, name) VALUES (5, 'testimyyja5') ON CONFLICT DO NOTHING;

INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (1, 'Mädätteet', 250, 'Biokaasulaitoksen mädätettä. Kuivamädäte.', NULL, NOW(), 'Papinkankaantie 15, 80330 Joensuu') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (1, 'Puu', 700, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrelta.', NULL, NOW(), 'Tampereentie 5, 31670 Urjala') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (2, 'Metsäbiomassa', 300, 'Harvennuspuuta Suomesta.', NULL, NOW(), 'Vattuperkkiöntie 2, 85500 Nivala') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (2, 'Nurmi', 30, 'Vanhempia luomukelpoisia säilörehunurmia noin 10 ha.', NULL, NOW(), 'Siggansintie 3, 10140 Siuntio') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (3, 'Hävikkirehu', 40, 'Vanhempia luomukelpoisia säilörehunurmia noin 10 ha.', NULL, NOW(), 'Åtorpintie 60, 07280 Porvoo') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (3, 'Viherkasvustot', 75, 'Ylimääräistä viherkasvustoa halvalla.', NULL, NOW(), 'Porokartanontie 1, Sodankylä') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (4, 'Puu', 550, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrella.', NULL, NOW(), 'Isokoskentie, Kiiskilä') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (4, 'Käsitelty puu', 710, 'Rikkinäisiä kuorma-lavoja.', NULL, NOW(), 'Rantakankaantie 16, Alajärvi') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (4, 'Korsirehu', 35, 'Vuoden 2022 säilörehupaaleja, verkot ja muovit osin rikki.', NULL, NOW(), 'Männiköntie 10, 41400 Jyväskylä') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (5, 'Maa-aines', 1000, 'Ylimääräistä maa-ainesta halvalla.', NULL, NOW(), 'Uudenkyläntie 182, 58700 Sulkava') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (5, 'Tuhka', 40, 'Fossiilittomasti tuotetun tuhkan neutralointikyky on 26-30 % Ca. Raskasmetallipitoisuudet alittavat lannoiteasetuksen peltolevityksen raja-arvot.', NULL, NOW(), 'Ritolantie 30, 60720 Ilmajoki') ON CONFLICT DO NOTHING;
INSERT INTO products (seller_id, name, price, description, image, created_at, location) VALUES (5, 'Eläinperäinen biomassa', 15, 'Mädätteitä Suomesta.', NULL, NOW(), 'Hakalantie 3, 86710 Kärsämäki') ON CONFLICT DO NOTHING;