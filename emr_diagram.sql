emr_patients-- Create database for EMR system
CREATE DATABASE IF NOT EXISTS emr_system;
USE emr_system;

-- Patient information table
CREATE TABLE emr_patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    medical_id VARCHAR(20) UNIQUE NOT NULL,  -- Medical identification number
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('M', 'F', 'O') NOT NULL,    -- M: Male, F: Female, O: Other
    address TEXT,
    phone_number VARCHAR(15),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Medical visit information table
CREATE TABLE emr_visits (
    visit_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    doctor_id VARCHAR(20) NOT NULL,
    department_id VARCHAR(20) NOT NULL,
    facility_id VARCHAR(20) NOT NULL,
    visit_date DATETIME NOT NULL,
    symptoms TEXT,
    diagnosis TEXT,
    notes TEXT,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES emr_patients(patient_id)
);

-- Prescription information table
CREATE TABLE emr_prescriptions (
    prescription_id VARCHAR(20) PRIMARY KEY,
    visit_id VARCHAR(20) NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    instructions TEXT,
    prescribed_by VARCHAR(20) NOT NULL,
    prescribed_date DATETIME NOT NULL,
    status ENUM('active', 'completed', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES emr_visits(visit_id)
);

-- Medical test information table
CREATE TABLE emr_tests (
    test_id VARCHAR(20) PRIMARY KEY,
    visit_id VARCHAR(20) NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    test_type ENUM('laboratory', 'imaging', 'other') NOT NULL,
    ordered_by VARCHAR(20) NOT NULL,
    ordered_date DATETIME NOT NULL,
    performed_date DATETIME,
    results TEXT,
    status ENUM('ordered', 'in_progress', 'completed', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES emr_visits(visit_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_patient_medical_id ON emr_patients(medical_id);
CREATE INDEX idx_visit_patient_id ON emr_visits(patient_id);
CREATE INDEX idx_visit_date ON emr_visits(visit_date);
CREATE INDEX idx_prescription_visit_id ON emr_prescriptions(visit_id);
CREATE INDEX idx_test_visit_id ON emr_tests(visit_id);