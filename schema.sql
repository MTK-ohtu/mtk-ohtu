DROP TYPE IF EXISTS buying_or_selling CASCADE;
DROP TYPE IF EXISTS delivery_method_type CASCADE; 
DROP TYPE IF EXISTS supply_demand_type CASCADE;
DROP TYPE IF EXISTS batch_units_type CASCADE;
DROP TYPE IF EXISTS vehichle_requirement_type CASCADE;
DROP TYPE IF EXISTS category_type CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    company_role_id TEXT
);

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    business_id VARCHAR(16) NOT NULL,
    standard_industrial_classification VARCHAR(16) NOT NULL
);

CREATE TYPE buying_or_selling AS ENUM ('sell','buy');
CREATE TYPE delivery_method_type  AS ENUM ('pickup', 'seller delivers', 'freight');
CREATE TYPE supply_demand_type AS ENUM ('one time', 'recurring', 'annually', 'weekly');
CREATE TYPE batch_units_type AS ENUM ('tn', 'm3', 'kg', 'l', 'pcs', 'batch');
CREATE TYPE vehichle_requirement_type AS ENUM ('dry', 'refrigerated', 'tanker', 'flatbed', 'container');
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
    'Logistics and contracting',
    'Other'
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    listing_type buying_or_selling NOT NULL,
    category category_type NOT NULL,
    subcategory VARCHAR(16),
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
    coordinates POINT,
    vehichle_requirement vehichle_requirement_type,
    complies_with_regulations BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    listing_id INTEGER NOT NULL REFERENCES listings(id),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    start_address TEXT NOT NULL,
    delivery_address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics_contractors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    business_id VARCHAR(16),
    address TEXT NOT NULL,
    cargo_capabilities vehichle_requirement_type[]
);