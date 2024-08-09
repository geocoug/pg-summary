import logging
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from psycopg2.sql import SQL, Identifier, Literal

from pg_summary.pg_summary import PgSummary, PostgresDB

load_dotenv()

logger = logging.getLogger(__name__)

DATA = Path(__file__).parent / "data.sql"


@pytest.fixture(scope="session")
def global_variables():
    """Set global variables for the test session."""
    return {
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT", 5432),
        "POSTGRES_DB": os.getenv("POSTGRES_DB", "postgres"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", "postgres"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
    }


@pytest.fixture(scope="session")
def db(global_variables):
    """Return a PostgresDB object."""
    db = PostgresDB(
        host=global_variables["POSTGRES_HOST"],
        database=global_variables["POSTGRES_DB"],
        user=global_variables["POSTGRES_USER"],
        passwd=global_variables["POSTGRES_PASSWORD"],
    )
    db.execute(DATA.read_text())
    db.commit()
    db.close()
    yield db
    db.execute(
        """
        delete from public.book_authors;
        delete from staging.book_authors;
        delete from public.authors;
        delete from staging.authors;
        delete from public.books;
        delete from staging.books;
        delete from public.genres;
        delete from staging.genres;
    """,
    )
    db.close()


@pytest.fixture(scope="session")
def pgsummary(global_variables):
    """Return a PgUpsert object."""
    obj = PgSummary(
        host=global_variables["POSTGRES_HOST"],
        database=global_variables["POSTGRES_DB"],
        user=global_variables["POSTGRES_USER"],
        passwd=global_variables["POSTGRES_PASSWORD"],
        schema="public",
        table_or_view="books",
    )
    yield obj
    obj.db.close()


def test_db_connection(db):
    """Test the database connection is successful, then close it."""
    assert db.conn is None
    db.open_db()
    assert db.conn is not None
    db.close()
    assert db.conn is None


def test_db_execute(db):
    """Test a simple query execution."""
    cur = db.execute("SELECT 1")
    assert cur.fetchone()[0] == 1


def test_db_execute_values(db):
    """Test a query execution with values."""
    cur = db.execute(SQL("SELECT {}").format(Literal(1)))
    assert cur.fetchone()[0] == 1
    cur = db.execute(
        SQL(
            """
            select table_name from information_schema.tables
            where table_schema={schema} and {column}={value}
        """,
        ).format(
            schema=Literal("staging"),
            column=Identifier("table_name"),
            value=Literal("genres"),
        ),
    )
    assert cur.fetchone()[0] == "genres"


def test_db_rowdict(db):
    """Test the rowdict function."""
    rows, headers, rowcount = db.rowdict("SELECT 1 as one, 2 as two")
    assert iter(rows)
    assert headers == ["one", "two"]
    assert rowcount == 1
    rows = list(rows)
    assert rows[0]["one"] == 1
    assert rows[0]["two"] == 2


def test_db_rowdict_params(db):
    """Test the rowdict function with parameters."""
    rows, headers, rowcount = db.rowdict(
        SQL("SELECT {one} as one, {two} as two").format(
            one=Literal(1),
            two=Literal(2),
        ),
    )
    assert iter(rows)
    assert headers == ["one", "two"]
    assert rowcount == 1
    rows = list(rows)
    assert rows[0]["one"] == 1
    assert rows[0]["two"] == 2


def test_pgsummary_init(db, pgsummary):
    """Test the PgSummary object initialization."""
    assert pgsummary.db.host == "localhost"
    assert pgsummary.db.database == "dev"
    assert pgsummary.schema == "public"
    assert pgsummary.table_or_view == "books"
    assert pgsummary.include_src is False
