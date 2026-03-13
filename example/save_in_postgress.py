"""
Load COOPER datasets from Hugging Face and persist them into a PostgreSQL database.

This script:
  - Loads measurements_by_cell, topology, and performance_indicators_meanings from CelfAI/COOPER.
  - Optionally computes aggregated views (mean/min by cell, mean by band/site).
  - Creates the database if missing, then writes the main tables via pandas to_sql.

Usage:
  python save_in_postgress.py

Requires: datasets, pandas, sqlalchemy, psycopg2-binary
"""

from datasets import load_dataset
import pandas as pd
from sqlalchemy import create_engine, text

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATASET_REPO = "CelfAI/COOPER"
SPLITS_MEASUREMENTS = ("train", "test")

# Default PostgreSQL connection (override via env or arguments if needed).
DEFAULT_CONFIG = {
    "USERNAME": "postgres",
    "PASSWORD": "postgres",
    "HOST": "localhost",
    "PORT": "5432",
    "DB_NAME": "cooper",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_measurements_by_cell() -> pd.DataFrame:
    """Load measurements_by_cell from COOPER, merge train and test splits."""
    ds = load_dataset(DATASET_REPO, "measurements_by_cell")
    train = ds["train"].to_pandas()
    test = ds["test"].to_pandas()
    return pd.concat([train, test], ignore_index=True)


def load_topology() -> pd.DataFrame:
    """Load topology from COOPER (main split)."""
    ds = load_dataset(DATASET_REPO, "topology")
    return ds["main"].to_pandas()


def load_performance_indicators_meanings() -> pd.DataFrame:
    """Load performance_indicators_meanings from COOPER (main split)."""
    ds = load_dataset(DATASET_REPO, "performance_indicators_meanings")
    return ds["main"].to_pandas()


def prepare_measurements_for_db(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for PostgreSQL (dots -> underscores)."""
    out = df.copy()
    out.columns = out.columns.str.replace(".", "_", regex=False)
    return out


def prepare_performance_indicators_for_db(df: pd.DataFrame) -> pd.DataFrame:
    """Rename 3GPP_reference to reference_3gpp for valid SQL identifier."""
    out = df.copy()
    out.rename(columns={"3GPP_reference": "reference_3gpp"}, inplace=True)
    return out


# ---------------------------------------------------------------------------
# Optional aggregated views (for analytics; not written to DB in this script)
# ---------------------------------------------------------------------------


def compute_aggregations(
    measurements: pd.DataFrame,
    topology: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Join measurements with topology and compute mean/min by cell, mean by band/site.
    Returns a dict of DataFrames for optional export or analysis.
    """
    all_data = pd.merge(measurements, topology, on="LocalCellName", how="left")
    pm_columns = [
        c for c in measurements.columns
        if c not in ("LocalCellName", "datetime")
    ]

    return {
        "mean_by_cell": measurements.groupby("LocalCellName")[pm_columns].mean().reset_index(),
        "min_by_cell": measurements.groupby("LocalCellName")[pm_columns].min().reset_index(),
        "mean_by_band": all_data.groupby("Band")[pm_columns].mean().reset_index(),
        "mean_by_site": all_data.groupby("SiteLabel")[pm_columns].mean().reset_index(),
    }


# ---------------------------------------------------------------------------
# Database setup and population
# ---------------------------------------------------------------------------


def ensure_database(engine_admin, db_name: str) -> None:
    """Create database if it does not exist (idempotent)."""
    with engine_admin.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
        )
        if result.scalar() is None:
            conn.execute(text(f"CREATE DATABASE {db_name} TEMPLATE template0;"))


def get_engine(config: dict, database: str | None = None):
    """Build SQLAlchemy engine for the given database (default: postgres)."""
    db = database or "postgres"
    url = (
        f"postgresql+psycopg2://{config['USERNAME']}:{config['PASSWORD']}"
        f"@{config['HOST']}:{config['PORT']}/{db}"
    )
    return create_engine(url)


def write_tables(engine, measurements: pd.DataFrame, topology: pd.DataFrame, performance_indicators: pd.DataFrame) -> None:
    """Write the three main DataFrames to PostgreSQL (replace existing tables)."""
    measurements.to_sql("measurements", engine, if_exists="replace", index=False)
    performance_indicators.to_sql(
        "performance_indicators_meanings", engine, if_exists="replace", index=False
    )
    topology.to_sql("topology", engine, if_exists="replace", index=False)


def list_public_tables(engine) -> list[tuple]:
    """Return list of (table_name,) in the public schema."""
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public';"
            )
        )
        return result.fetchall()


# ---------------------------------------------------------------------------
# DDL: CREATE TABLE IF NOT EXISTS (run before loading data)
# ---------------------------------------------------------------------------

query_Performance_Indicators_meaning = """
CREATE TABLE IF NOT EXISTS performance_indicators_meanings (
    name TEXT PRIMARY KEY,
    category TEXT,
    description TEXT,
    unit TEXT,
    collection_method TEXT,
    collection_condition TEXT,
    measurement_entity TEXT,
    reference_3gpp TEXT
);
"""

query_Topology = """
CREATE TABLE IF NOT EXISTS topology (
    SiteLabel TEXT,
    LocalCellName TEXT PRIMARY KEY,
    Sector INT,
    PCI INT,
    DuplexMode TEXT,
    Band TEXT,
    dlBandwidth TEXT,
    Azimuth NUMERIC,
    MDT INT,
    EDT INT,
    HBeamwidth INT,
    AntennaHeight NUMERIC,
    GroundHeight INT,
    OperationMode TEXT,
    distance_X NUMERIC,
    distance_Y NUMERIC
);
"""

query_Measurements = """
CREATE TABLE IF NOT EXISTS measurements (
    LocalCellName TEXT REFERENCES topology(LocalCellName) ON DELETE CASCADE,
    datetime TEXT,
    RRC_ConnEstabSucc INT,
    RRC_ConnEstabAtt INT,
    RRC_Setup INT,
    RRC_ConnMax INT,
    MM_HoExeIntraFreqSuccOut INT,
    MM_HoExeIntraFreqReqOut INT,
    MM_HoExeIntraFreqSucc INT,
    MM_HoExeIntraFreqAtt INT,
    MM_HoExecInterFreqReqOut_Cov INT,
    MM_HoExeInterFreqSuccOut_Cov INT,
    MM_HoPrepInterFreqReqOut_Cov INT,
    MM_HoExeInterFreqReqOut INT,
    MM_HoExeInterFreqSuccOut INT,
    MM_HoPrepInterFreqReqOut INT,
    MM_HoPrepIntraFreqReqOut INT,
    MM_HoFailIn_Admit INT,
    MM_HoExeIntraFreqPrepReqIn INT,
    MM_Redirection_Blind INT,
    MM_Redirection_Cov INT,
    CARR_WBCQIDist_Bin0 INT,
    CARR_WBCQIDist_Bin1 INT,
    CARR_WBCQIDist_Bin2 INT,
    CARR_WBCQIDist_Bin3 INT,
    CARR_WBCQIDist_Bin4 INT,
    CARR_WBCQIDist_Bin5 INT,
    CARR_WBCQIDist_Bin6 INT,
    CARR_WBCQIDist_Bin7 INT,
    CARR_WBCQIDist_Bin8 INT,
    CARR_WBCQIDist_Bin9 INT,
    CARR_WBCQIDist_Bin10 INT,
    CARR_WBCQIDist_Bin11 INT,
    CARR_WBCQIDist_Bin12 INT,
    CARR_WBCQIDist_Bin13 INT,
    CARR_WBCQIDist_Bin14 INT,
    CARR_WBCQIDist_Bin15 INT,
    ThpVolDl NUMERIC,
    ThpVolUl NUMERIC,
    ThpTimeDl NUMERIC,
    ThpTimeUl NUMERIC,
    CellUnavail_System INT,
    CellUnavail_Manual INT,
    CellUnavail_EnergySaving INT,
    UECNTX_Est_Att INT,
    UECNTX_Est_Succ INT,
    UECNTX_Rem INT
);
"""


def create_tables_if_not_exist(engine) -> None:
    """Create tables from DDL if they do not exist (topology first, then measurements FK)."""
    with engine.connect() as conn:
        conn.execute(text(query_Performance_Indicators_meaning))
        conn.execute(text(query_Topology))
        conn.execute(text(query_Measurements))
        conn.commit()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(config: dict | None = None) -> None:
    config = config or DEFAULT_CONFIG
    db_name = config["DB_NAME"]

    # 1) Load and prepare data
    measurements = load_measurements_by_cell()
    topology = load_topology()
    performance_indicators = load_performance_indicators_meanings()

    measurements = prepare_measurements_for_db(measurements)
    performance_indicators = prepare_performance_indicators_for_db(performance_indicators)


    # 2) Create the database if it does not exist, then connect to it
    engine_admin = get_engine(config, database="postgres")
    ensure_database(engine_admin, db_name)
    engine = get_engine(config, database=db_name)

    # 3) Create tables from DDL if they do not exist
    create_tables_if_not_exist(engine)

    # 4) Load data into tables (replace existing data)
    write_tables(engine, measurements, topology, performance_indicators)

    # 5) Verify: list tables in public schema
    tables = list_public_tables(engine)
    print("Tables in public schema:", tables)


if __name__ == "__main__":
    main()
