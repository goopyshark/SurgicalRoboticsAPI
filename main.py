import requests

# --------------------------------------------------
# Robotic-Assisted Surgical Device Adverse Event Tracker
# Data Source: FDA openFDA Medical Device Adverse Event API
# --------------------------------------------------

# openFDA API endpoint
url = "https://api.fda.gov/device/event.json"

# Search the FDA database for records involving robotic devices
params = {
    "search": 'device.generic_name:robotic',
    "limit": 10
}

# Terms that indicate the device is related to robotic surgery
relevant_terms = [
    "robotic surgical",
    "surgical robot",
    "da vinci",
    "davinci",
    "robotic device",
    "robotic instrument",
    "robotic arm"
]

# Terms used to remove obvious unrelated results
exclude_terms = [
    "gauze",
    "pack",
    "retractor"
]

print("Robotic-Assisted Surgical Device Adverse Event Tracker")
print("Connecting to openFDA...")
print()

try:
    # Send request to the openFDA API
    response = requests.get(url, params=params, timeout=30)

    print("Status Code:", response.status_code)

    # Continue only if the request was successful
    if response.status_code == 200:

        data = response.json()
        results = data.get("results", [])

        print("Connection successful!")
        print("Records received from API:", len(results))
        print()

        relevant_count = 0

        # Examine each adverse event report
        for report in results:

            devices = report.get("device", [])

            # Skip reports without device information
            if not devices:
                continue

            # Examine each device listed in the report
            for device in devices:

                generic_name = device.get("generic_name", "")
                brand_name = device.get("brand_name", "")

                # Combine names so they are easier to search
                combined_name = (
                        generic_name + " " + brand_name
                ).lower()

                # Determine whether the device appears relevant
                is_relevant = any(
                    term in combined_name
                    for term in relevant_terms
                )

                # Determine whether it contains an excluded term
                is_excluded = any(
                    term in combined_name
                    for term in exclude_terms
                )

                # Display only likely robotic surgical devices
                if is_relevant and not is_excluded:

                    relevant_count += 1

                    print("----- ROBOTIC SURGICAL REPORT -----")

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

                    manufacturer = device.get(
                        "manufacturer_d_name", ""
                    )

                    print(
                        "Report Number:",
                        report_number
                    )

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
                        if product_problems
                        else "N/A"
                    )

                    print(
                        "Device Generic Name:",
                        generic_name
                        if generic_name
                        else "N/A"
                    )

                    print(
                        "Device Brand Name:",
                        brand_name
                        if brand_name
                        else "N/A"
                    )

                    print(
                        "Manufacturer:",
                        manufacturer
                        if manufacturer
                        else "N/A"
                    )

                    print()

        print("----------------------------------------")
        print(
            "Relevant robotic surgical devices found:",
            relevant_count
        )

    else:
        print("Request failed.")
        print("Response from openFDA:")
        print(response.text)

except requests.exceptions.RequestException as error:
    print("An error occurred while connecting to openFDA:")
    print(error)