import csv
import json
import os


def _dedupe_headers(raw_headers):
    """
    Make CSV headers unique.

    Empty header cells become "col", "col_1", "col_2", ... and any
    duplicated header name gets a numeric suffix so no column is lost
    when the row is turned into a dict.

    Args:
        raw_headers (list): The raw header row read from the CSV file.

    Returns:
        list: Deduplicated, non-empty header names, same length/order
            as raw_headers.
    """
    headers = []
    seen = {}
    for h in raw_headers:
        name = h if h else "col"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        headers.append(name)
    return headers


def _fieldnames_union(rows):
    """
    Collect every key found across a list of dicts, in first-seen order.

    Used so the output CSV has a column for every field that appears in
    ANY row, even if some rows don't have that field.

    Args:
        rows (list): List of dictionaries.

    Returns:
        list: Ordered list of unique field names.
    """
    fieldnames = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    return fieldnames


def to_json(input_csv, output_json=None):
    """
    Convert a CSV file into a JSON file (list of objects).

    Args:
        input_csv (str): Path to the source CSV file.
        output_json (str, optional): Path to the output JSON file.
            Defaults to the input filename with a .json extension.

    Returns:
        str: Path to the generated JSON file.
    """
    if output_json is None:
        output_json = os.path.splitext(input_csv)[0] + ".json"

    with open(input_csv, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        raw_headers = next(reader)
        headers = _dedupe_headers(raw_headers)
        data = [dict(zip(headers, row)) for row in reader]

    with open(output_json, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    return output_json


def to_csv(input_json, output_csv=None):
    """
    Convert a JSON file (list of objects) into a CSV file.

    Args:
        input_json (str): Path to the source JSON file.
        output_csv (str, optional): Path to the output CSV file.
            Defaults to the input filename with a .csv extension.

    Returns:
        str: Path to the generated CSV file.

    Raises:
        ValueError: If the JSON file contains no data.
    """
    if output_csv is None:
        output_csv = os.path.splitext(input_json)[0] + ".csv"

    with open(input_json, "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    if not data:
        raise ValueError("The JSON file contains no data to convert.")

    fieldnames = _fieldnames_union(data)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval="")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return output_csv