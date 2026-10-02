"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """this pulls out the systolic readings from the encounter records."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])

    return readings


def mean_systolic(readings):
    """return the mean of the systolic readings, or None if the list is empty."""
    if len(readings) == 0:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """return the number of unique patient IDs in the encounters using set"""
    patient_ids = set()

    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])

    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """return a list of patient IDs whose systolic reading is at or above the cutoff."""
    patients = []

    for encounter in encounters:
        patient_id = encounter["patient_id"]
        systolic = encounter["systolic"]

        if systolic >= cutoff and patient_id not in patients:
            patients.append(patient_id)

    return patients
