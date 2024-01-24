CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
    email TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    roles TEXT[]
);

CREATE TABLE sellers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES sellers(id),
    name TEXT,
    price INTEGER,
    description TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    location TEXT,
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    status TEXT,
);

CREATE TABLE buyers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
    address TEXT,
    phone TEXT,
);