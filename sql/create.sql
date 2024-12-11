CREATE TABLE patients (
    patient_fname       VARCHAR(80),
    patient_lname       VARCHAR(80),
    patient_id          INT PRIMARY KEY
);

CREATE TABLE sleep_data (
    patient_id          INT REFERENCES patients (patient_id) on DELETE CASCADE,
    sleep_date          DATE,
    time_slept          INTERVAL,
    motion_score        INT CHECK (motion_score >= 0 AND motion_score <= 100),
    sound_score         INT CHECK (sound_score >= 0 AND sound_score <= 100),
    PRIMARY KEY (patient_id, sleep_date)
);
