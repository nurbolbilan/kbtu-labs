import psycopg2


class DBManager:
    """Handles all PostgreSQL database interactions for the Snake game."""

    def __init__(self):
        # Database connection parameters — update these to match your setup
        self.params = {
            "dbname": "snake_game",
            "user": "postgres",
            "password": "Nurbol",
            "host": "localhost",
        }
        self._init_db()

    def _init_db(self):
        """Create the required tables if they don't already exist."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id       SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id            SERIAL PRIMARY KEY,
                        player_id     INTEGER REFERENCES players(id),
                        score         INTEGER   NOT NULL,
                        level_reached INTEGER   NOT NULL,
                        played_at     TIMESTAMP DEFAULT NOW()
                    );
                """)

    def get_user_id(self, username: str) -> int:
        """Return the player's ID, creating a new record if the username doesn't exist."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                # Insert if not exists; return the new id if inserted
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) "
                    "ON CONFLICT (username) DO NOTHING RETURNING id;",
                    (username,),
                )
                res = cur.fetchone()
                if res:
                    return res[0]
                # Username already existed — fetch the existing id
                cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
                return cur.fetchone()[0]

    def save_game(self, user_id: int, score: int, level: int):
        """Persist a completed game session to the database."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) "
                    "VALUES (%s, %s, %s);",
                    (user_id, score, level),
                )

    def get_top_10(self) -> list:
        """Fetch the top 10 all-time scores across all players.
        Returns a list of (username, score, level_reached, played_at) tuples."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.username, gs.score, gs.level_reached, gs.played_at
                    FROM   game_sessions gs
                    JOIN   players p ON gs.player_id = p.id
                    ORDER  BY gs.score DESC
                    LIMIT  10;
                """)
                return cur.fetchall()

    def get_pb(self, user_id: int) -> int:
        """Return the player's personal best score (0 if they have never played)."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT MAX(score) FROM game_sessions WHERE player_id = %s;",
                    (user_id,),
                )
                res = cur.fetchone()[0]
                return res if res else 0