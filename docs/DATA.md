# Data Model

SQLite file: bot_data.sqlite3

Tables:

- users
  - username TEXT UNIQUE
  - xp INTEGER DEFAULT 0
  - tokens INTEGER DEFAULT 0
  - wins INTEGER DEFAULT 0
  - last_seen INTEGER DEFAULT 0

- redemptions
  - id INTEGER PK
  - username TEXT
  - reward TEXT
  - cost INTEGER
  - created_at INTEGER (epoch seconds)

- metadata
  - key TEXT PRIMARY KEY
  - value TEXT

Notes:
- Tokens are awarded on wins (+5). You can add more sources as desired.
- Use metadata to toggle seasonal modes (e.g., halloween=true).
