import requests
import sqlite3


# --------------------------------------------------
# Robotic-Assisted Surgical Device Adverse Event Tracker
# Data Source: FDA openFDA Medical Device Adverse Event API
# --------------------------------------------------

# ---------------- DATABASE SETUP ----------------

connection = sqlite3.connect("surgical_robotics.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS adverse_events (
    report_number TEXT PRIMARY KEY,
    event_type TEXT,
    date_received TEXT,
    product_problems TEXT,
    generic_name TEXT,
    brand_name TEXT,
    manufacturer TEXT
)
""")

connection.commit()


# ---------------- API SETUP ----------------

url = "https://api.fda.gov/device/event.json"

params = {
    "search": 'device.generic_name:robotic',
    "limit": 10
}


# ---------------- FILTERING ----------------

relevant_terms = [
    "robotic surgical",
    "surgical robot",
    "da vinci",
    "davinci",
    "robotic device",
    "robotic instrument",
    "robotic arm"
]

exclude_terms = [
    "gauze",
    "pack",
    "retractor"
]


print("Robotic-Assisted Surgical Device Adverse Event Tracker")
print("Connecting to openFDA...")
print()


# ---------------- API REQUEST ----------------

try:
    response = requests.get(url, params=params, timeout=30)

    print("Status Code:", response.status_code)

    if response.status_code == 200:

        data = response.json()
        results = data.get("results", [])

        print("Connection successful!")
        print("Records received from API:", len(results))
        print()

        relevant_count = 0
        new_records = 0
        duplicate_records = 0

        # Examine every adverse event report
        for report in results:

            devices = report.get("device", [])

            if not devices:
                continue

            # Examine every device associated with the report
            for device in devices:

                generic_name = device.get("generic_name", "")
                brand_name = device.get("brand_name", "")
                manufacturer = device.get("manufacturer_d_name", "")

                combined_name = (
                        generic_name + " " + brand_name
                ).lower()

                is_relevant = any(
                    term in combined_name
                    for term in relevant_terms
                )

                is_excluded = any(
                    term in combined_name
                    for term in exclude_terms
                )

                if is_relevant and not is_excluded:

                    relevant_count += 1

                    report_number = report.get(
                        "report_number", "N/A"
                    )

                    event_type = report.get(
                        "event_type", ""
                    )

                    date_received = report.get(
                        "date_received", "N/A"
                    )

                    product_problems = report.get(
                        "product_problems", []
                    )

                    # Convert the list of product problems
                    # into a single string for SQLite
                    product_problems_text = ", ".join(
                        product_problems
                    )

                    # ---------------- DATABASE INSERT ----------------

                    cursor.execute("""
                    INSERT OR IGNORE INTO adverse_events (
                        report_number,
                        event_type,
                        date_received,
                        product_problems,
                        generic_name,
                        brand_name,
                        manufacturer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        report_number,
                        event_type if event_type else "N/A",
                        date_received,
                        product_problems_text
                        if product_problems_text else "N/A",
                        generic_name
                        if generic_name else "N/A",
                        brand_name
                        if brand_name else "N/A",
                        manufacturer
                        if manufacturer else "N/A"
                    ))

                    # rowcount tells us whether SQLite
                    # actually inserted the record
                    if cursor.rowcount > 0:
                        new_records += 1
                        record_status = "NEW RECORD SAVED"
                    else:
                        duplicate_records += 1
                        record_status = "DUPLICATE - NOT SAVED"

                    # ---------------- DISPLAY RESULT ----------------

                    print("----- ROBOTIC SURGICAL REPORT -----")

                    print("Report Number:", report_number)

                    print(
                        "Event Type:",
                        event_type if event_type else "N/A"
                    )

                    print(
                        "Date Received:",
                        date_received
                    )

                    print(
                        "Product Problems:",
                        product_problems
                        if product_problems else "N/A"
                    )

                    print(
                        "Device Generic Name:",
                        generic_name
                        if generic_name else "N/A"
                    )

                    print(
                        "Device Brand Name:",
                        brand_name
                        if brand_name else "N/A"
                    )

                    print(
                        "Manufacturer:",
                        manufacturer
                        if manufacturer else "N/A"
                    )

                    print("Database Status:", record_status)
                    print()

        # Save database changes
        connection.commit()

        # ---------------- DATABASE SUMMARY ----------------

        cursor.execute(
            "SELECT COUNT(*) FROM adverse_events"
        )

        total_database_records = cursor.fetchone()[0]

        print("----------------------------------------")
        print(
            "Relevant robotic surgical devices found:",
            relevant_count
        )
        print(
            "New records saved:",
            new_records
        )
        print(
            "Duplicate records skipped:",
            duplicate_records
        )
        print(
            "Total records currently in database:",
            total_database_records
        )

    else:
        print("Request failed.")
        print("Response from openFDA:")
        print(response.text)


except requests.exceptions.RequestException as error:
    print("An error occurred while connecting to openFDA:")
    print(error)


finally:
    # Always close the database connection
    connection.close()