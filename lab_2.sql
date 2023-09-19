CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE requests (
    request_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(client_id),
    request_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);