

INSERT INTO users (username, password, email) VALUES ('testikayttaja1', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi1@gmail.com') ON CONFLICT DO NOTHING;  -- pass: testpassword
INSERT INTO users (username, password, email) VALUES ('testikayttaja2', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi2@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja3', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi3@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja4', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi4@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikayttaja5', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi5@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja1', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi6@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja2', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi7@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testikuljettaja3', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'testi8@gmail.com') ON CONFLICT DO NOTHING;
INSERT INTO users (username, password, email) VALUES ('testuser', 'scrypt:32768:8:1$Yu7GsrH9WAn3PKS5$da21d2d2d46ac35eb018cf7aff7597fb1128e6fad5ce643b15ebc2274965f6d221b845dc7fb0f3273eb994c3157b5f614b2d2f18404c7e9b585da852dfcc9bbb', 'test@test.com');

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
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (4, 'sell', 'Wood (treated wood)',  'pickup', 'one time', 1, 'tn', 550, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrella.', 'Isokoskentie, Kiiskilä', 24.6858813, 63.8003589, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (1, 'sell', 'Wood (forest biomass)',  'pickup', 'one time', 1, 'tn', 700, 'Kuivaa jalavaa, vaahteraa ja harvennuspuuta metsätien varrelta.', 'Tampereentie 5, 31670 Urjala', 23.5494974, 61.0815604, '1') ON CONFLICT DO NOTHING;
INSERT INTO listings (user_id, listing_type, category, delivery_method, supply_demand, batch_size, batch_units, price, description, address, longitude, latitude, complies_with_regulations) VALUES (4, 'sell', 'Wood (treated wood)',  'pickup', 'one time', 1, 'tn', 710, 'Rikkinäisiä kuorma-lavoja.', 'Rantakankaantie 16, Alajärvi', 23.9481132, 62.8319709, '1') ON CONFLICT DO NOTHING;

INSERT INTO contractors (user_id, name, created_at, business_id) 
VALUES 
    (1, 'Kuljetus Oy Laakso', NOW(), '1234567-A'), 
    (2, 'M & T Trans Oy', NOW(), '1234567-B'), 
    (3, 'Wise Logistics Oy', NOW(), '1234567-C'), 
    (4, 'MPT-Kuljetus Oy', NOW(), '1234567-D'), 
    (5, 'Matti Jokimäki Oy', NOW(), '1234567-E'), 
    (6, 'Alueurakointi Poutiainen Oy', NOW(), '1234567-F'), 
    (7, 'Kuljetusliike Järveläinen Oy', NOW(), '1234567-G'), 
    (8, 'RH-Trans Oy', NOW(), '1234567-H'),
    (9, 'Transport Oy Ab', NOW(), '1234567-I')
ON CONFLICT DO NOTHING;

INSERT INTO contractor_locations (contractor_id, address, telephone, email, longitude, latitude, delivery_radius)
VALUES
    (1, 'Urpunistintie 8, 03400 Vihti', '040-123456', 'testilocation@gmail.com', 24.33768, 60.41596, 500),
    (1, 'Kehäkatu, 86300 oululainen', '040-123456', 'testilocation@gmail.com', 24.81586, 64.27193, 200),
    (1, 'Saaninranta, 448800 Pihtipudas', '040-123456', 'testilocatin@gmail.com', 25.60259, 63.845, 700),
    (2, 'Kullaantie, 29350 Ulvila', '040-123456', 'testilocation@gmail.com', 22.16209, 61.46592, 500),
    (2, 'Saukkolantie, 08500 Lohja', '040-123456', 'testilocation@gmail.com', 24.10896, 60.27905, 350),
    (3, 'Käpykankaantie, 78210 Lohja', '040-123456', 'testilocation@gmail.com', 27.8562, 62.3068, 600),
    (4, 'Talonpojankatu, 67100 Kokkola', '040-123456', 'testilocation@gmail.com', 23.15841, 63.83384, 550),
    (5, 'Karjakatu, 90130 Oulu', '040-123456', 'testilocation@gmail.com', 25.48896, 65.0073, 400),
    (6, 'Ranniotie, 99600 Sodankylä', '040-123456', 'testilocation@gmail.com', 26.5722, 67.4292, 600),
    (7, 'Launeenkatu, 15610 Lahti', '040-123456', 'testilocation@gmail.com', 25.65424, 60.96962, 200),
    (9, 'Mantokoskentie, 99980 Utsjoki', '040-123456', 'testilocation@gmail.com', 27.00864, 69.87624, 300)
ON CONFLICT DO NOTHING;

INSERT INTO cargo_capabilities (contractor_location_id, type, price_per_km, base_rate, max_capacity, max_distance, unit, can_process)
VALUES
    (1, 'Wood (treated wood)', 6, 100, 5, 500, 'tn', '0'),
    (1, 'Plant-based biomasses', 5, 44, 3, 400, 'tn', '0'),
    (1, 'Digestion', 3, 77, 2, 550, 'tn', '1'),
    (2, 'Plant-based biomasses', 3, 45, 3, 300, 'tn', '0'),
    (2, 'Animal-based biomasses', 7, 178, 1, 400, 'tn', '0'),
    (2, 'Digestion', 3, 50, 9, 100, 'tn', '1'),
    (3, 'Digestion', 3, 60, 4, 400, 'tn', '1'),
    (3, 'Plant-based biomasses', 3, 45, 3, 100, 'tn', '0'),
    (3, 'Soil and growing media', 9, 220, 3, 600, 'tn', '0'),
    (3, 'Wood (forest biomass)', 6, 100, 10, 300, 'tn', '0'),
    (4, 'Animal-based biomasses', 6, 178, 3, 300, 'tn', '0'),
    (4, 'Plant-based biomasses', 5, 119, 2, 600, 'tn', '0'),
    (4, 'Soil and growing media', 5, 600, 2, 400, 'tn', '0'),
    (4, 'Dry manure', 5, 60, 2, 300, 'tn', '0'),
    (4, 'Digestion', 3, 77, 6, 500, 'tn', '1'),
    (5, 'Soil and growing media', 5, 125, 2, 400, 'tn', '0'),
    (5, 'Digestion', 3, 60, 2, 600, 'tn', '1'),
    (5, 'Wood (treated wood)', 7, 100, 8, 500, 'tn', '0'),
    (5, 'Animal-based biomasses', 4, 120, 2, 300, 'tn', '0'),
    (6, 'Sludge manure', 5, 60, 3, 500, 'tn', '0'),
    (6, 'Plant-based biomasses', 3, 45, 3, 400, 'tn', '0'),
    (6, 'Digestion', 7, 200, 5, 100, 'tn', '1'),
    (7, 'Soil and growing media', 5, 800, 2, 300, 'tn', '0'),
    (8, 'Plant-based biomasses', 7, 90, 1, 500, 'tn', '0'),
    (8, 'Plant-based biomasses', 3, 45, 3, 500, 'tn', '0'),
    (9, 'Digestion', 3, 77, 2, 600, 'tn', '0'),
    (9, 'Plant-based biomasses', 6, 80, 6, 400, 'tn', '0'),
    (9, 'Digestion', 3, 77, 5, 300, 'tn', '0')
ON CONFLICT DO NOTHING;

INSERT INTO api_keys (name, key) VALUES ('Test API key', 'test_api_key')
ON CONFLICT DO NOTHING;