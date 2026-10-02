#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(DATA_PATH):
    """An encounter is a dict with three keys: patient_id, visit_date, and systolic.
    patient_id is a string, visit_date is a string, and systolic is an int.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # TODO: read the rows and skip the header line.
    # TODO: keep a row only when it has three fields, int() can read the
    #       systolic field, and the reading is plausible.
    # TODO: count every other data row as skipped, the blank line included,
    #       and print one line per skipped row so you can see what dropped out.
#==================================================================================
    with DATA_PATH.open("r", encoding="utf-8") as data_file:
        rows = data_file.readlines()
        skipped = 0
        encounters = []
        for row in rows[1:]:                      # rows[0] is the header line
            if not row.strip():                   # an export often ends with a blank line
                print("Skipping a blank row.")
                skipped += 1
                continue
            fields = row.strip().split(",")
            if len(fields) != 3:                  # an extra comma leaves too many pieces to unpack
                print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
                skipped += 1
                continue
            patient_id, visit_date, raw_systolic = fields
            try:
                systolic = int(raw_systolic)
            except ValueError as error:
                print(f"Skipping {patient_id}: {error}")
                continue

            if systolic < 60 or systolic > 250:
                print(f"Skipping {patient_id}: implausible systolic {systolic}")
                skipped += 1
                continue
            else:
                encounters.append({"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic})
#==================================================================================
    # TODO: end with `return encounters, skipped`.

    return encounters, skipped


def main():
    """This writes the two report files, then reads them back and prints them"""
    encounters, skipped = read_encounters(DATA_PATH)
    assert encounters, f"no usable readings in {DATA_PATH}"
    if not DATA_PATH.exists():
        print(f"Cannot find {DATA_PATH}: run this script from the folder containing clinic_vitals.csv.")
        return

# debug 
    # print("main() started")
    # print("Current DATA_PATH:", DATA_PATH)
    # print("Current OUTPUT_DIR:", OUTPUT_DIR)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
#==================================================================================
    readings = systolic_readings(encounters)
    lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_text = "\n".join(lines) + "\n"

    OUTPUT_DIR.mkdir(exist_ok=True)           # no error when output/ already exists
    report_path = OUTPUT_DIR / "vitals_report.txt"

    # print("About to write:", report_path)     # debugging checkpoint
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)
#==================================================================================
    # TODO: read the file back and print it, so you can see what was saved.
#==================================================================================
    with open(report_path, "r", encoding="utf-8") as report_file:      #read back the file we just wrote
        saved_text = report_file.read()

    print(f"Read back from {report_path}:")
    print(saved_text, end="")
    print(f"Saved report matches: {saved_text == report_text}")
    assert saved_text == report_text, "the saved report does not match the text we built"

    one_line = saved_text.strip().replace("\n", " | ")
    print(f"Checkpoint passed: {len(lines)} lines saved to {report_path}")
    print(f"Report on one line: {one_line}")
#==================================================================================
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.
    cutoff = 140
    reason = "I chose a cutoff value of 140 because Systolic BP of 140 mmHg or higher is considered Stage 2 Hypertension, thus worth following up with the patients to manage their blood pressure."
    followup_patients = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ]

    followup_lines.extend(followup_patients)

    followup_text = "\n".join(followup_lines) + "\n"

    followup_path = OUTPUT_DIR / "followup_list.txt"

    # print("About to write:", followup_path) #debugging checkpoint

    with open(followup_path, "w", encoding="utf-8") as followup_file:
        followup_file.write(followup_text)

if __name__ == "__main__":
    main()
