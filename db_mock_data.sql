

INSERT INTO users (username, password, email) VALUES ('testikayttaja1', 'salasana123', 'testi1@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja2', 'salasana123', 'testi2@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja3', 'salasana123', 'testi3@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja4', 'salasana123', 'testi4@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja5', 'salasana123', 'testi5@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja1', 'salasana123', 'testi6@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja2', 'salasana123', 'testi7@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja3', 'salasana123', 'testi8@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testuser', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'test@test.com'); -- pass: testpassword

INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, complies_with_regulations) VALUES (1, 'sell', 'Digestion', 'pickup', 'one time', 1, 'tn', 250, 'Keskustassa.', 'Karkkila', '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (4, 'sell', 'Basket fodder',  'pickup', 'one time', 1, 'tn', 35, 'Vuoden 2022 säilörehupaaleja, verkot ja muovit osin rikki.', 'Männiköntie 10, 41400 Jyväskylä',26.214065536083947, 62.264343999999994, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (2, 'sell', 'Plant-based biomasses',  'pickup', 'one time', 1, 'tn', 300, 'Harvennuspuuta Suomesta.', 'Vattuperkkiöntie 2, 85500 Nivala', 24.9342153, 63.8923984, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (5, 'sell', 'Other side streams (not biomass)',  'pickup', 'one time', 1, 'tn', 40, 'Fossiilittomasti tuotetun tuhkan neutralointikyky on 26-30 % Ca. Raskasmetallipitoisuudet alittavat lannoiteasetuksen peltolevityksen raja-arvot.', 'Ritolantie 30, 60720 Ilmajoki', 22.7118248, 62.7315596, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (5, 'sell', 'Soil and growing media',  'pickup', 'one time', 1, 'tn', 1000, 'Ylimääräistä maa-ainesta halvalla.', 'Uudenkyläntie 182, 58700 Sulkava', 28.323367600537907, 61.79652605, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (1, 'sell', 'Digestion',  'pickup', 'one time', 1, 'tn', 250, 'Biokaasulaitoksen mädätettä. Kuivamädäte.', 'Papinkankaantie 15, 80330 Joensuu', 29.8356994, 62.5668921, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (5, 'sell', 'Animal-based biomasses',  'pickup', 'one time', 1, 'tn', 15, 'Mädätteitä Suomesta.', 'Hakalantie 3, 86710 Kärsämäki', 25.7667884, 63.9603873, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (3, 'sell', 'Grass, waste fodder and green growths',  'pickup', 'one time', 1, 'tn', 75, 'Ylimääräistä viherkasvustoa halvalla.', 'Porokartanontie 1, Sodankylä', 27.3667281, 68.3336791, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (2, 'sell', 'Grass, waste fodder and green growths',  'pickup', 'one time', 1, 'tn', 30, 'Vanhempia luomukelpoisia säilörehunurmia noin 10 ha.', 'Siggansintie 3, 10140 Siuntio', 24.1444409, 60.1367265, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (3, 'sell', 'Grass, waste fodder and green growths',  'pickup', 'one time', 1, 'tn', 40, 'Vanhempia luomukelpoisia säilörehunurmia noin 10 ha.', 'Åtorpintie 60, 07280 Porvoo', 25.7364406, 60.4667942, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (4, 'sell', 'Wood',  'pickup', 'one time', 1, 'tn', 550, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrella.', 'Isokoskentie, Kiiskilä', 24.6858813, 63.8003589, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (1, 'sell', 'Wood',  'pickup', 'one time', 1, 'tn', 700, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrelta.', 'Tampereentie 5, 31670 Urjala', 23.5494974, 61.0815604, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (4, 'sell', 'Wood',  'pickup', 'one time', 1, 'tn', 710, 'Rikkinäisiä kuorma-lavoja.', 'Rantakankaantie 16, Alajärvi', 23.9481132, 62.8319709, '1') ON CONFLICT DO NOTHING;

-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor1', NOW(), '1234567-A', 'Urpunistintie 8, 03400 Vihti', 60.41596, 24.33768, 500) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor2', NOW(), '1234567-B', 'Kehäkatu, 86300 oululainen', 64.27193, 24.81586, 200) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor3', NOW(), '1234567-C', 'Saaninranta, 448800 Pihtipudas', 63.845, 25.60259, 700) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor4', NOW(), '1234567-D', 'Kullaantie, 29350 Ulvila', 61.46592, 22.16209, 500) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor5', NOW(), '1234567-E', 'Saukkolantie, 08500 Lohja', 60.27905, 24.10896, 350) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor6', NOW(), '1234567-F', 'Käpykankaantie, 78210 Lohja', 62.3068, 27.8562, 600) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor7', NOW(), '1234567-G', 'Talonpojankatu, 67100 Kokkola', 63.83384, 23.15841, 550) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor8', NOW(), '1234567-H', 'Karjakatu, 90130 Oulu', 65.0073, 25.48896, 400) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor9', NOW(), '1234567-I', 'Ranniotie, 99600 Sodankylä', 67.4292, 26.5722, 600) ON CONFLICT DO NOTHING;
-- INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) VALUES (6, 'TestContractor10', NOW(), '1234567-J', 'Launeenkatu, 15610 Lahti', 60.96962, 25.65424, 200) ON CONFLICT DO NOTHING;

INSERT INTO logistics_contractors (user_id, name, created_at, business_id, address, longitude, latitude, delivery_radius) 
VALUES 
    (6, 'TestContractor1', NOW(), '1234567-A', 'Urpunistintie 8, 03400 Vihti', 24.33768, 60.41596, 500), 
    (6, 'TestContractor2', NOW(), '1234567-B', 'Kehäkatu, 86300 oululainen', 24.81586, 64.27193, 200), 
    (6, 'TestContractor3', NOW(), '1234567-C', 'Saaninranta, 448800 Pihtipudas', 25.60259, 63.845, 700), 
    (6, 'TestContractor4', NOW(), '1234567-D', 'Kullaantie, 29350 Ulvila', 22.16209, 61.46592, 500), 
    (6, 'TestContractor5', NOW(), '1234567-E', 'Saukkolantie, 08500 Lohja', 24.10896, 60.27905, 350), 
    (6, 'TestContractor6', NOW(), '1234567-F', 'Käpykankaantie, 78210 Lohja', 27.8562, 62.3068, 600), 
    (6, 'TestContractor7', NOW(), '1234567-G', 'Talonpojankatu, 67100 Kokkola', 23.15841, 63.83384, 550), 
    (6, 'TestContractor8', NOW(), '1234567-H', 'Karjakatu, 90130 Oulu', 25.48896, 65.0073, 400), 
    (6, 'TestContractor9', NOW(), '1234567-I', 'Ranniotie, 99600 Sodankylä', 26.5722, 67.4292, 600), 
    (6, 'TestContractor10', NOW(), '1234567-J', 'Launeenkatu, 15610 Lahti', 25.65424, 60.96962, 200) 
ON CONFLICT DO NOTHING;

INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (1, 'Manure', 5, 60) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (1, 'Wood', 6, 100) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (2, 'Plant-based biomasses', 3, 45) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (2, 'Animal-based biomasses', 7, 178) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (3, 'Digestion', 3, 60) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (3, 'Soil and growing media', 9, 220) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (4, 'Wood', 6, 100) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (4, 'Animal-based biomasses', 6, 178) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (5, 'Plant-based biomasses', 5, 119) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (5, 'Soil and growing media', 5, 600) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (6, 'Manure', 5, 60) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (6, 'Soil and growing media', 5, 125) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (7, 'Digestion', 3, 60) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (7, 'Wood', 7, 100) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (8, 'Animal-based biomasses', 4, 120) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (8, 'Manure', 5, 60) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (9, 'Soil and growing media', 5, 800) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (9, 'Plant-based biomasses', 7, 90) ON CONFLICT DO NOTHING;
INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (10, 'Digestion', 3, 77) ON CONFLICT DO NOTHING;