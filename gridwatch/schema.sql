-- GridWatch schema. Applied by `flask --app gridwatch init-db`.

DROP TABLE IF EXISTS command_log;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS appliance_state;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id              INTEGER PRIMARY KEY,
    username        TEXT    NOT NULL UNIQUE,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    role            TEXT    NOT NULL DEFAULT 'resident'
                            CHECK (role IN ('resident', 'admin')),
    -- ThingSpeak wiring. status_field is the field number carrying the packed
    -- appliance status string; health lives in status_field + 1 and the sensor
    -- readings occupy fields 1 .. status_field - 1.
    channel_id      TEXT,
    status_field    INTEGER NOT NULL DEFAULT 6,
    read_api_key    TEXT,
    write_api_key   TEXT,
    -- Load-shedding order, most important appliance first, e.g. "Motor_1,LED_1".
    priority        TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_users_email ON users (email);

-- Last known state per appliance. Written whenever a control is used, and
-- refreshed from ThingSpeak so the dashboard has something to show when the
-- network is down.
CREATE TABLE appliance_state (
    user_id     INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    appliance   TEXT    NOT NULL,
    position    INTEGER NOT NULL,
    power       INTEGER NOT NULL DEFAULT 0,
    speed       INTEGER NOT NULL DEFAULT 0,
    direction   INTEGER NOT NULL DEFAULT 0,
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, appliance)
);

CREATE TABLE notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    appliance   TEXT    NOT NULL DEFAULT '',
    message     TEXT    NOT NULL,
    severity    TEXT    NOT NULL DEFAULT 'info'
                        CHECK (severity IN ('info', 'warning', 'critical')),
    seen        INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_notifications_user ON notifications (user_id, seen, id DESC);

-- Audit trail of every control command, with where it was delivered.
CREATE TABLE command_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    appliance   TEXT    NOT NULL,
    payload     TEXT    NOT NULL,
    transport   TEXT    NOT NULL,
    ok          INTEGER NOT NULL DEFAULT 0,
    detail      TEXT    NOT NULL DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_command_log_user ON command_log (user_id, id DESC);
