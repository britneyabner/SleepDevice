import psycopg
import datetime

class Database:
    """Provides functionality to access a local PostgreSQL database.

    Attributes:
        name (str): Name of the database, should be sleepdb
        user (str): User that accesses PostgreSQL database, should be postgres
    """

    def __init__(self, name: str, user: str) -> (str, str):
        self.connect_str = f"dbname={name} user={user}"

    def get_patient_name_from_id(self, id: int):
        """Obtains the first and last name of a patient base on id number.

        Args:
            id (int): Patient ID number

        Returns:
            (str, str): First and last name of the patient
        """
        with psycopg.connect(self.connect_str) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT patient_fname, patient_lname
                    FROM patients
                    WHERE patient_id=%s
                    """, (id,))

                first_name, last_name = cur.fetchone()

        return (first_name, last_name)

    def add_new_patient(self, fname: str, lname: str):
        with psycopg.connect(self.connect_str) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT COUNT(*)
                    FROM patients""")

                max_id = int(cur.fetchone()[0])

        new_id = max_id + 1

        with psycopg.connect(self.connect_str) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                INSERT INTO patients (patient_id, patient_fname, patient_lname)
                VALUES (%s, %s, %s)""", (new_id, fname, lname))

    def add_patient_scores(self, id: int, date: datetime.date,
                           time_slept: datetime.time, motion_score: int,
                           sound_score: int):

        with psycopg.connect(self.connect_str) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO sleep_data (patient_id, sleep_date, time_slept,
                                            motion_score, sound_score)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (id, date, time_slept, motion_score, sound_score))


def test_add_new_patient():
    db = Database("sleepdb", "postgres")
    db.add_new_patient("Britney", "Abner")


def test_get_patient_name_from_id():
    db = Database("sleepdb", "postgres")
    fname, lname = db.get_patient_name_from_id(1)
    print(f"{fname} {lname}")


def test_add_patients_scores():
    db = Database("sleepdb", "postgres")
    date = datetime.date(2024, 12, 2)
    time = datetime.time(8, 5, 20)
    db.add_patient_scores(1, date, time, 90, 75)


if __name__ == "__main__":
    test_get_patient_name_from_id()
    test_add_patients_scores()
