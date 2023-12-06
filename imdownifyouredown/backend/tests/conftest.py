import pytest

import os
import sqlite3


@pytest.fixture
def conn():
    file_dir = os.path.dirname(__file__)
    test_db_path = os.path.join(os.path.dirname(file_dir), "data", "test.db")
    conn = sqlite3.connect(test_db_path)

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

