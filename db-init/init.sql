CREATE TABLE IF NOT EXISTS intel_L100_files (
  file_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  uploaded_file_name VARCHAR(255) NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_description TEXT,
  file_series INTEGER, -- This is a foreign key; update the reference if you have a series table
  fingerprint VARCHAR(255),
  description TEXT,
  metad_create_date TIMESTAMP,
  metad_edit_date TIMESTAMP,
  markdown_extract TEXT,
  status VARCHAR(50)
  -- Uncomment and adjust the next line if you have a referenced table for file_series:
  --, FOREIGN KEY (file_series) REFERENCES file_series(file_series_id)
);


