CREATE TABLE IF NOT EXISTS stocks (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id integer NOT NULL,
    symbol text NOT NULL,
    price numeric NOT NULL,
    shares numeric NOT NULL,
    operation text NOT NULL check("operation" in ('buy', 'sell')),
    date timestamp
);