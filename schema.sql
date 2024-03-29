CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    company_role_id TEXT
);

CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    business_id VARCHAR(16) NOT NULL,
    standard_industrial_classification VARCHAR(16) NOT NULL
);

DO $$ BEGIN
    CREATE TYPE buying_or_selling AS ENUM ('sell','buy');
    CREATE TYPE delivery_method_type  AS ENUM ('pickup', 'seller delivers', 'freight');
    CREATE TYPE supply_demand_type AS ENUM ('one time', 'recurring', 'annually', 'weekly');
    CREATE TYPE batch_units_type AS ENUM ('tn', 'm^3', 'kg', 'l', 'kpl');
    CREATE TYPE vehichle_requirement_type AS ENUM ('dry', 'refrigerated', 'tanker', 'flatbed', 'container');
    CREATE TYPE eco_category_type AS ENUM ('electricity', 'biogas', 'biodiesel', 'hydrogen');
    CREATE TYPE category_type AS ENUM (
    'Manure',
    'Grass, waste fodder and green growths',
    'Basket fodder',
    'Plant-based biomasses',
    'Animal-based biomasses',
    'Soil and growing media',
    'Digestion',
    'Wood',
    'Other side streams (not biomass)',
    'Logistics and contracting'
);
    CREATE TYPE subcategory_type AS ENUM (
    'Dry manure',
    'Sludge manure',
    'Separated manure',
    'Other manure',
    'Forest biomass',
    'Treated wood'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(128),
    listing_type buying_or_selling NOT NULL,
    category category_type NOT NULL,
    subcategory subcategory_type,
    delivery_method delivery_method_type NOT NULL,
    supply_demand supply_demand_type NOT NULL,
    is_continuous BOOLEAN DEFAULT true,
    expiration_date TIMESTAMP,
    batch_size INTEGER NOT NULL,
    batch_units batch_units_type NOT NULL,
    image_id INTEGER,
    price NUMERIC NOT NULL,
    delivery_details TEXT,
    description TEXT,
    address TEXT NOT NULL,
    longitude NUMERIC,
    latitude NUMERIC,
    date_created TIMESTAMP,
    vehichle_requirement vehichle_requirement_type,
    complies_with_regulations BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    listing_id INTEGER NOT NULL REFERENCES listings(id),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    start_address TEXT NOT NULL,
    delivery_address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contractors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    business_id VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS contractor_locations (
    id SERIAL PRIMARY KEY,
    contractor_id INTEGER REFERENCES contractors(id),
    address TEXT NOT NULL,
    telephone TEXT,
    email TEXT,
    longitude FLOAT,
    latitude FLOAT,
    delivery_radius INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS eco_types (
    id SERIAL PRIMARY KEY,
    contractor_location_id INTEGER REFERENCES contractor_locations(id),
    eco_type eco_category_type
);

CREATE TABLE IF NOT EXISTS cargo_capabilities (
    id SERIAL PRIMARY KEY,
    contractor_location_id INTEGER REFERENCES contractor_locations(id),
    category category_type NOT NULL,
    subcategory subcategory_type,
    price_per_km INTEGER,
    base_rate INTEGER,
    max_capacity INTEGER,
    max_distance INTEGER,
    unit batch_units_type,
    can_process BOOLEAN DEFAULT False,
    description TEXT
);

CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    name TEXT,
    key VARCHAR(128)
)