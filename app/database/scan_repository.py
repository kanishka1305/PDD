from app.database.connection import get_connection


def save_scan(metadata, filename, filepath):

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT INTO scans
    (
        patient_name,
        patient_id,
        filename,
        filepath,
        modality,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        metadata.get("patient_name"),
        metadata.get("patient_id"),
        filename,
        filepath,
        metadata.get("modality"),
        "uploaded"
    )

    cursor.execute(sql, values)

    conn.commit()

    scan_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return scan_id