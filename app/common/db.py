import os
import sqlite3
import time
import uuid


DB = os.getenv(
    "DB_PATH",
    os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ),
        "data",
        "wade.db"
    )
)


def conn():
    os.makedirs(
        os.path.dirname(DB),
        exist_ok=True
    )

    c = sqlite3.connect(DB)

    c.row_factory = sqlite3.Row

    return c


def init():

    with conn() as c:

        c.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                key TEXT,
                lat REAL,
                lng REAL,
                accuracy REAL,
                captured_at INTEGER,
                device_id TEXT,
                depth_lo REAL,
                depth_hi REAL,
                confidence REAL,
                band TEXT,
                flow TEXT,
                verdicts TEXT,
                image_usable INTEGER,
                created_at INTEGER
            )
        """)

        c.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_reports_geo
            ON reports(lat, lng)
        """)


def insert(r):

    rid = uuid.uuid4().hex

    with conn() as c:

        c.execute(
            """
            INSERT INTO reports (
                id,
                key,
                lat,
                lng,
                accuracy,
                captured_at,
                device_id,
                depth_lo,
                depth_hi,
                confidence,
                band,
                flow,
                verdicts,
                image_usable,
                created_at
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
            """,
            (
                rid,
                r["key"],
                r["lat"],
                r["lng"],
                r.get("accuracy"),
                r.get("capturedAt"),
                r.get("deviceId"),
                r["depth_lo"],
                r["depth_hi"],
                r["confidence"],
                r["band"],
                r["flow"],
                r["verdicts"],
                1 if r["image_usable"] else 0,
                int(time.time())
            )
        )

    return rid


def nearby(bbox):

    west, south, east, north = bbox

    with conn() as c:

        rows = c.execute(
            """
            SELECT *
            FROM reports
            WHERE lng BETWEEN ? AND ?
            AND lat BETWEEN ? AND ?
            ORDER BY created_at DESC
            LIMIT 500
            """,
            (
                west,
                east,
                south,
                north
            )
        ).fetchall()

    return rows