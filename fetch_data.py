import pandas as pd
import os

def _get_patient_header(df, patient_id, section_title):
    patient_rows = df[df['patient_id'] == patient_id]
    if patient_rows.empty:
        return None, f"No {section_title.lower()} data found for patient {patient_id}"

    patient_info_cols = [
        'full_name', 'birthdate', 'ssn', 'drivers', 'passport', 'prefix', 'marital',
        'race', 'ethnicity', 'gender', 'birthplace', 'patient_address', 'patient_city',
        'patient_state', 'county', 'fips', 'patient_zip', 'lat', 'lon',
        'healthcare_expenses', 'healthcare_coverage', 'income'
    ]
    patient_info = patient_rows.iloc[0][patient_info_cols]

    note_lines = [f"\n📌 Patient Information (ID: {patient_id})"]
    for col, val in patient_info.items():
        note_lines.append(f"- {col.replace('_', ' ').title()}: {val}")
    note_lines.append(f"\n{section_title}:")
    
    return patient_rows, note_lines


def generate_clean_medication_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "💊 Medications")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['medication_start_ts']}]: {row['medication_description']} (Code: {row['medication_code']}) | Age: {row['age_at_medication']} | "
            f"Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
            f"Reason: {row.get('medication_reason_description', 'N/A')} | Notes: {row.get('medications_notes', 'None')}"
        )
    return "\n".join(note_lines)


def generate_clean_allergy_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🤧 Allergies")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        base = f"[{row['recorded_ts']}]: Age: {row.get('age_at_allergy', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | " \
               f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']}"
        parts = []
        if pd.notna(row['allergy_description']):
            parts.append(f"Main Allergy: {row['allergy_description']} (Category: {row['allergy_category']})")
        if pd.notna(row['allergy_description1']):
            parts.append(f"Related: {row['allergy_description1']} (Severity: {row['allergy_severity1']})")
        if pd.notna(row['allergy_description2']):
            parts.append(f"Related: {row['allergy_description2']} (Severity: {row['allergy_severity2']})")
        note_lines.append(f"- {base} | " + " | ".join(parts))
    return "\n".join(note_lines)


def generate_clean_imaging_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🩻 Imaging Studies")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['recorded_ts']}]: {row['modality_description']} of {row['bodysite_description']} (Modality Code: {row['modality_code']}, SOP: {row['sop_description']}) | "
            f"Age: {row['age_at_imaging']} | Procedure Code: {row['procedure_code']} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | Reason: {row.get('encounter_reason', 'N/A')}"
        )
    return "\n".join(note_lines)


def generate_clean_procedure_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "✂️ Procedures")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['prcedure_start_ts']} - {row.get('procedure_stop_ts', 'N/A')}]: {row['procedure_description']} (System: {row['procedure_system']}, Code: {row['procedure_code']}) | "
            f"Age: {row['age_at_procedure']} | Reason: {row.get('procedure_reason_description', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_condition_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🩺 Conditions")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['condition_start_ts']} - {row.get('condition_stop_ts', 'N/A')}]: {row['condition_description']} (System: {row['condition_system']}, Code: {row['condition_code']}) | "
            f"Age: {row['age_at_condition']} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_careplan_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "📋 Careplans")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['careplan_start_ts']} - {row.get('careplan_stop_ts', 'N/A')}]: {row['careplan_description']} | Age: {row['age_at_careplan']} | "
            f"Reason: {row.get('careplan_reason_description', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_immunization_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "💉 Immunizations")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['recorded_ts']}]: {row['immunization_description']} (Code: {row['immunization_code']}) | Age: {row['age_at_immunization']} | "
            f"Provider: {row['provider_name']} ({row['provider_speciality']}) | Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
            f"Encounter: {row['encounter_description']} | Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_observation_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🧪 Observations")
    if isinstance(note_lines, str): return note_lines

    # Get the maximum recorded timestamp and filter for all observations on that date
    if not patient_rows.empty:
        # Convert to datetime and extract date part only
        patient_rows['date_only'] = pd.to_datetime(patient_rows['recorded_ts']).dt.date
        max_date = patient_rows['date_only'].max()
        latest_observations = patient_rows[patient_rows['date_only'] == max_date]
        
        for _, row in latest_observations.iterrows():
            note_lines.append(
                f"- [{row['recorded_ts']}]: {row['observation_description']} (Code: {row['observation_code']}) = {row['observation_value']} {row['observation_units']} | "
                f"Type: {row['observation_type']} | Category: {row['observation_category']} | Age: {row['age_at_observation']} | "
                f"Provider: {row['provider_name']} ({row['provider_speciality']}) | Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
                f"Encounter: {row['encounter_description']} | Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
            )
    return "\n".join(note_lines)


import pandas as pd

def _get_patient_header(df, patient_id, section_title):
    patient_rows = df[df['patient_id'] == patient_id]
    if patient_rows.empty:
        return None, f"No {section_title.lower()} data found for patient {patient_id}"

    patient_info_cols = [
        'full_name', 'birthdate', 'ssn', 'drivers', 'passport', 'prefix', 'marital',
        'race', 'ethnicity', 'gender', 'birthplace', 'patient_address', 'patient_city',
        'patient_state', 'county', 'fips', 'patient_zip', 'lat', 'lon',
        'healthcare_expenses', 'healthcare_coverage', 'income'
    ]
    patient_info = patient_rows.iloc[0][patient_info_cols]

    note_lines = [f"\n📌 Patient Information (ID: {patient_id})"]
    for col, val in patient_info.items():
        note_lines.append(f"- {col.replace('_', ' ').title()}: {val}")
    note_lines.append(f"\n{section_title}:")
    
    return patient_rows, note_lines


def generate_clean_medication_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "💊 Medications")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['medication_start_ts']}]: {row['medication_description']} (Code: {row['medication_code']}) | Age: {row['age_at_medication']} | "
            f"Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
            f"Reason: {row.get('medication_reason_description', 'N/A')} | Notes: {row.get('medications_notes', 'None')}"
        )
    return "\n".join(note_lines)


def generate_clean_allergy_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🤧 Allergies")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        base = f"[{row['recorded_ts']}]: Age: {row.get('age_at_allergy', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | " \
               f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']}"
        parts = []
        if pd.notna(row['allergy_description']):
            parts.append(f"Main Allergy: {row['allergy_description']} (Category: {row['allergy_category']})")
        if pd.notna(row['allergy_description1']):
            parts.append(f"Related: {row['allergy_description1']} (Severity: {row['allergy_severity1']})")
        if pd.notna(row['allergy_description2']):
            parts.append(f"Related: {row['allergy_description2']} (Severity: {row['allergy_severity2']})")
        note_lines.append(f"- {base} | " + " | ".join(parts))
    return "\n".join(note_lines)


def generate_clean_imaging_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🩻 Imaging Studies")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['recorded_ts']}]: {row['modality_description']} of {row['bodysite_description']} (Modality Code: {row['modality_code']}, SOP: {row['sop_description']}) | "
            f"Age: {row['age_at_imaging']} | Procedure Code: {row['procedure_code']} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | Reason: {row.get('encounter_reason', 'N/A')}"
        )
    return "\n".join(note_lines)


def generate_clean_procedure_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "✂️ Procedures")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['prcedure_start_ts']} - {row.get('procedure_stop_ts', 'N/A')}]: {row['procedure_description']} (System: {row['procedure_system']}, Code: {row['procedure_code']}) | "
            f"Age: {row['age_at_procedure']} | Reason: {row.get('procedure_reason_description', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_condition_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🩺 Conditions")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['condition_start_ts']} - {row.get('condition_stop_ts', 'N/A')}]: {row['condition_description']} (System: {row['condition_system']}, Code: {row['condition_code']}) | "
            f"Age: {row['age_at_condition']} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_careplan_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "📋 Careplans")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['careplan_start_ts']} - {row.get('careplan_stop_ts', 'N/A')}]: {row['careplan_description']} | Age: {row['age_at_careplan']} | "
            f"Reason: {row.get('careplan_reason_description', 'N/A')} | Provider: {row['provider_name']} ({row['provider_speciality']}) | "
            f"Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | Encounter: {row['encounter_description']} | "
            f"Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_immunization_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "💉 Immunizations")
    if isinstance(note_lines, str): return note_lines

    for _, row in patient_rows.iterrows():
        note_lines.append(
            f"- [{row['recorded_ts']}]: {row['immunization_description']} (Code: {row['immunization_code']}) | Age: {row['age_at_immunization']} | "
            f"Provider: {row['provider_name']} ({row['provider_speciality']}) | Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
            f"Encounter: {row['encounter_description']} | Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
        )
    return "\n".join(note_lines)


def generate_clean_observation_note(df, patient_id):
    patient_rows, note_lines = _get_patient_header(df, patient_id, "🧪 Observations")
    if isinstance(note_lines, str): return note_lines

    # Get the maximum recorded timestamp and filter for all observations on that date
    if not patient_rows.empty:
        # Convert to datetime and extract date part only
        patient_rows['date_only'] = pd.to_datetime(patient_rows['recorded_ts']).dt.date
        max_date = patient_rows['date_only'].max()
        latest_observations = patient_rows[patient_rows['date_only'] == max_date]
        
        for _, row in latest_observations.iterrows():
            note_lines.append(
                f"- [{row['recorded_ts']}]: {row['observation_description']} (Code: {row['observation_code']}) = {row['observation_value']} {row['observation_units']} | "
                f"Type: {row['observation_type']} | Category: {row['observation_category']} | Age: {row['age_at_observation']} | "
                f"Provider: {row['provider_name']} ({row['provider_speciality']}) | Org: {row['organization_name']} - {row['organization_city']}, {row['organization_state']} | "
                f"Encounter: {row['encounter_description']} | Total Cost: ${row['total_claim_cost']:.2f} (Payer Coverage: ${row['payer_coverage']:.2f})"
            )
    return "\n".join(note_lines)


# Map section to corresponding generator function
section_generators = {
    'medications': generate_clean_medication_note,
    'allergies': generate_clean_allergy_note,
    'imaging': generate_clean_imaging_note,
    'procedures': generate_clean_procedure_note,
    'conditions': generate_clean_condition_note,
    'careplans': generate_clean_careplan_note,
    'immunizations': generate_clean_immunization_note,
    'observations': generate_clean_observation_note,
}

# Map section to CSV filename
section_filenames = {
    'medications': 'medications.csv',
    'allergies': 'allergies.csv',
    'imaging': 'imaging_studies.csv',
    'procedures': 'procedures.csv',
    'conditions': 'conditions.csv',
    'careplans': 'careplans.csv',
    'immunizations': 'immunizations.csv',
    'observations': 'observations.csv',
}

def generate_note(section: str, df: pd.DataFrame, patient_id: str) -> str:
    section = section.lower().strip()
    if section not in section_generators:
        return f"❌ Unknown section: '{section}'"
    return section_generators[section](df, patient_id)

def generate_note_auto(section: str, patient_id: str, data_folder: str = './data') -> str:
    section = section.lower().strip()
    if section not in section_generators or section not in section_filenames:
        return f"❌ Unknown section: '{section}'"

    file_path = os.path.join(data_folder, section_filenames[section])
    if not os.path.exists(file_path):
        return f"❌ File not found for section '{section}': {file_path}"

    df = pd.read_csv(file_path)
    return section_generators[section](df, patient_id)
