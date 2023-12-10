import pytest

import sqlite3
from pathlib import Path


@pytest.fixture(scope="session")
def conn(tmp_path: Path):
    test_db_path = tmp_path / "test.db"
    conn = sqlite3.connect(test_db_path.absolute())

    conn.execute("DROP TABLE IF EXISTS Events")
    conn.execute("CREATE TABLE IF NOT EXISTS Events(eventid, userid, eventname, down)")
    conn.execute(
        """
        INSERT INTO Events VALUES
            (1, 1, 'test1', True),
            (1, 2, 'test1', False),
            (2, 1, 'test2', True)
        """
    )
    conn.commit()

    return conn

