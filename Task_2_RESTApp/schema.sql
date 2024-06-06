-- schema.sql
CREATE TABLE IF NOT EXISTS sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    active BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    active BOOLEAN NOT NULL,
    type TEXT CHECK(type IN ('preplay', 'inplay')) NOT NULL,
    sport_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Pending', 'Started', 'Ended', 'Cancelled')) NOT NULL,
    scheduled_start DATETIME NOT NULL,
    actual_start DATETIME,
    FOREIGN KEY (sport_id) REFERENCES sports(id)
);

CREATE TABLE IF NOT EXISTS selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event_id INTEGER NOT NULL,
    price DECIMAL(5,2) NOT NULL,
    active BOOLEAN NOT NULL,
    outcome TEXT CHECK(outcome IN ('Unsettled', 'Void', 'Lose', 'Win')) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);
