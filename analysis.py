import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Robotic-Assisted Surgical Device Adverse Event Tracker
# Preliminary Data Analysis
# --------------------------------------------------

print()
print("Robotic-Assisted Surgical Device Adverse Event Tracker")
print("Preliminary Data Analysis")
print()


# ---------------- DATABASE CONNECTION ----------------

connection = sqlite3.connect("surgical_robotics.db")

query = """
SELECT
    report_number,
    event_type,
    date_received,
    product_problems,
    generic_name,
    brand_name,
    manufacturer,
    collected_at
FROM adverse_events
"""


try:

    # Load SQLite data into a Pandas DataFrame
    df = pd.read_sql_query(query, connection)


    # ==================================================
    # DATASET SUMMARY
    # ==================================================

    print("=" * 55)
    print("DATASET SUMMARY")
    print("=" * 55)

    print("Total reports in database:", len(df))
    print()

    print("Columns:")

    for column in df.columns:
        print("-", column)

    print()


    # ==================================================
    # EVENT TYPE ANALYSIS
    # ==================================================

    print("=" * 55)
    print("EVENT TYPES")
    print("=" * 55)

    event_counts = (
        df["event_type"]
        .fillna("N/A")
        .value_counts()
    )

    print(event_counts)
    print()


    # ---------------- EVENT TYPE PERCENTAGES ----------------

    print("=" * 55)
    print("EVENT TYPE PERCENTAGES")
    print("=" * 55)

    event_percentages = (
            event_counts / len(df) * 100
    ).round(1)

    for event_type, percentage in event_percentages.items():
        print(f"{event_type}: {percentage}%")

    print()


    # ---------------- EVENT TYPE VISUALIZATION ----------------

    event_counts.plot(
        kind="bar",
        title="Reported Adverse Events by Event Type"
    )

    plt.xlabel("Event Type")
    plt.ylabel("Number of Reports")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        "event_types.png",
        dpi=300
    )

    print(
        "Event type chart saved as: event_types.png"
    )
    print()

    plt.show()


    # ==================================================
    # MANUFACTURER ANALYSIS
    # ==================================================

    print("=" * 55)
    print("TOP MANUFACTURERS")
    print("=" * 55)

    # Create a cleaned manufacturer column.
    # This does NOT modify the original SQLite database.
    df["manufacturer_clean"] = df["manufacturer"].copy()

    # Normalize variations of Intuitive Surgical.
    # Examples include:
    # INTUITIVE SURGICAL, INC.
    # INTUITIVE SURGICAL INC
    # INTUITIVE
    # INTUITVE SURGICAL SERVICES, INC.
    #
    # The FDA data remains unchanged in the database.

    intuitive_mask = (
        df["manufacturer"]
        .fillna("")
        .str.upper()
        .str.contains("INTUIT")
    )

    df.loc[
        intuitive_mask,
        "manufacturer_clean"
    ] = "INTUITIVE SURGICAL"

    manufacturer_counts = (
        df["manufacturer_clean"]
        .fillna("N/A")
        .value_counts()
        .head(10)
    )

    print(manufacturer_counts)
    print()


    # ---------------- MANUFACTURER PERCENTAGES ----------------

    print("=" * 55)
    print("MANUFACTURER PERCENTAGES")
    print("=" * 55)

    manufacturer_percentages = (
            manufacturer_counts / len(df) * 100
    ).round(1)

    for manufacturer, percentage in manufacturer_percentages.items():
        print(
            f"{manufacturer}: {percentage}%"
        )

    print()


    # ---------------- MANUFACTURER VISUALIZATION ----------------

    manufacturer_counts.plot(
        kind="bar",
        title="Reports by Manufacturer"
    )

    plt.xlabel("Manufacturer")
    plt.ylabel("Number of Reports")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        "manufacturers.png",
        dpi=300
    )

    print(
        "Manufacturer chart saved as: manufacturers.png"
    )
    print()

    plt.show()


    # ==================================================
    # DEVICE ANALYSIS
    # ==================================================

    print("=" * 55)
    print("TOP DEVICE GENERIC NAMES")
    print("=" * 55)

    device_counts = (
        df["generic_name"]
        .fillna("N/A")
        .value_counts()
        .head(10)
    )

    print(device_counts)
    print()


    # ==================================================
    # BRAND ANALYSIS
    # ==================================================

    print("=" * 55)
    print("TOP DEVICE BRANDS")
    print("=" * 55)

    brand_counts = (
        df["brand_name"]
        .fillna("N/A")
        .value_counts()
        .head(10)
    )

    print(brand_counts)
    print()


    # ==================================================
    # PRODUCT PROBLEM ANALYSIS
    # ==================================================

    print("=" * 55)
    print("TOP PRODUCT PROBLEMS")
    print("=" * 55)

    # Some reports contain multiple product problems.
    # Split the stored comma-separated values so each
    # problem can be counted separately.

    problems = (
        df["product_problems"]
        .fillna("N/A")
        .str.split(",")
        .explode()
        .str.strip()
    )

    problem_counts = (
        problems
        .value_counts()
        .head(10)
    )

    print(problem_counts)
    print()


    # ==================================================
    # MISSING DATA ANALYSIS
    # ==================================================

    print("=" * 55)
    print("MISSING / N/A VALUES")
    print("=" * 55)

    for column in [
        "report_number",
        "event_type",
        "date_received",
        "product_problems",
        "generic_name",
        "brand_name",
        "manufacturer",
        "collected_at"
    ]:

        missing_count = (
                df[column].isna().sum()
                + (df[column] == "N/A").sum()
        )

        print(
            f"{column}: {missing_count}"
        )

    print()


    # ==================================================
    # COLLECTION INFORMATION
    # ==================================================

    print("=" * 55)
    print("COLLECTION INFORMATION")
    print("=" * 55)

    records_with_timestamp = (
        df["collected_at"]
        .notna()
        .sum()
    )

    records_without_timestamp = (
        df["collected_at"]
        .isna()
        .sum()
    )

    print(
        "Records with collection timestamp:",
        records_with_timestamp
    )

    print(
        "Records without collection timestamp:",
        records_without_timestamp
    )

    print()


    # ==================================================
    # SAMPLE DATA
    # ==================================================

    print("=" * 55)
    print("SAMPLE RECORDS")
    print("=" * 55)

    print(
        df[
            [
                "report_number",
                "event_type",
                "generic_name",
                "brand_name"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print()


    # ==================================================
    # ANALYSIS SUMMARY
    # ==================================================

    print("=" * 55)
    print("ANALYSIS SUMMARY")
    print("=" * 55)

    print(
        "Total reports analyzed:",
        len(df)
    )

    print(
        "Most common event type:",
        event_counts.index[0]
    )

    print(
        "Most common manufacturer:",
        manufacturer_counts.index[0]
    )

    print(
        "Most common product problem:",
        problem_counts.index[0]
    )

    print()


    # ==================================================
    # ANALYSIS COMPLETE
    # ==================================================

    print("=" * 55)
    print("ANALYSIS COMPLETE")
    print("=" * 55)

    print(
        "Charts created:"
    )

    print(
        "- event_types.png"
    )

    print(
        "- manufacturers.png"
    )


except Exception as error:

    print()
    print("An error occurred during analysis:")
    print(error)


finally:

    connection.close()

    print()
    print("Database connection closed.")