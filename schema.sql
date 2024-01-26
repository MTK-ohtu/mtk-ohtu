CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    roles TEXT[]
);

CREATE TABLE IF NOT EXISTS sellers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES sellers(id),
    name TEXT,
    price INTEGER,
    description TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    location TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    status TEXT
);

CREATE TABLE IF NOT EXISTS buyers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
    address TEXT,
    phone TEXT
);