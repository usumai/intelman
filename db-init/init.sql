CREATE TABLE IF NOT EXISTS intelman.intel_l100_files (
  file_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  uploaded_file_name VARCHAR(255) NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_description TEXT,
  doc_id INTEGER, 
  fingerprint VARCHAR(255),
  metad_create_date TIMESTAMP,
  metad_edit_date TIMESTAMP,
  markdown_extract TEXT,
  title VARCHAR(255),
  version VARCHAR(50),
  author VARCHAR(255),
  owner VARCHAR(255),
  status VARCHAR(255)
);

---------------------------------------------------------------------------
-- Table: intel_l101_docs
-- Columns: doc_id, create_date, create_user, delete_date, delete_user, doc_name,
--          doc_desc, doc_author, doc_owner, owner_group_id, doc_weights
CREATE TABLE IF NOT EXISTS intel_l101_docs (
  doc_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  doc_name VARCHAR(255) NOT NULL,
  doc_desc TEXT,
  doc_author VARCHAR(255),
  doc_owner VARCHAR(50),
  owner_group_id INTEGER,
  doc_weights JSONB
  -- If you later decide on a foreign key:
  --, FOREIGN KEY (owner_group_id) REFERENCES intel_l102_group(group_id)
);

---------------------------------------------------------------------------
-- Table: intel_l102_candidate_settings
-- Will specify what the file could be a candidate for
CREATE TABLE IF NOT EXISTS intel_l102_candidate_settings (
  candidate_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  candidate_name VARCHAR(255),
  candidate_desc VARCHAR(255),
  candidate_fields VARCHAR(255),
  owner_group_id INTEGER
);

INSERT INTO intel_l102_candidate_settings (create_user,candidate_name,candidate_desc,candidate_fields
) VALUES (
    'admin',
    'volumetrics',
    'file contains information about a stock code/item of supply/product, and contains measurements (length, width, height, weight)',
    'stock_code_number, item_length_m, item_width_m, item_height_m, item_weight_kg'
);
INSERT INTO intel_l102_candidate_settings (create_user,candidate_name,candidate_desc,candidate_fields
) VALUES (
    'admin',
    'event',
    'file contains information about one or more events with a dates',
    'event_date, event_description, event_tags'
);

---------------------------------------------------------------------------
-- Table: intel_l103_candidacy
-- Will highlight that the file is a candidate for something
CREATE TABLE IF NOT EXISTS intel_l103_candidacy (
  candidacy_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  candidate_id INTEGER,
  file_id INTEGER,
  candidacy_result VARCHAR(255),
  result_status VARCHAR(255)
);

---------------------------------------------------------------------------
-- Table: intel_l105_models
-- Columns: model_id, create_date, create_user, delete_date, delete_user,
--          model_file_name, model_desc
CREATE TABLE IF NOT EXISTS intel_l105_models (
  model_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  model_file_name VARCHAR(255) NOT NULL,
  model_desc TEXT
);

---------------------------------------------------------------------------
-- Table: intel_l106_deployments
-- Columns: deployment_id, create_date, create_user, delete_date, delete_user,
--          owner_group_id, model_id, deployment_name, deployment_desc
CREATE TABLE IF NOT EXISTS intel_l106_deployments (
  deployment_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  owner_group_id INTEGER,
  model_id INTEGER NOT NULL,
  deployment_name VARCHAR(255) NOT NULL,
  deployment_desc TEXT
  --, FOREIGN KEY (owner_group_id) REFERENCES intel_l102_group(group_id)
  --, FOREIGN KEY (model_id) REFERENCES intel_l105_models(model_id)
);

---------------------------------------------------------------------------
-- Table: intel_l107_deployment_docs
-- Columns: deployment_doc_id, create_date, create_user, delete_date, delete_user,
--          deployment_id, doc_id
CREATE TABLE IF NOT EXISTS intel_l107_deployment_docs (
  deployment_doc_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  deployment_id INTEGER NOT NULL,
  doc_id INTEGER NOT NULL
  --, FOREIGN KEY (deployment_id) REFERENCES intel_l106_deployments(deployment_id)
  --, FOREIGN KEY (doc_id) REFERENCES intel_l101_docs(doc_id)
);

---------------------------------------------------------------------------
-- Table: intel_l120_group
-- Columns: group_id, create_date, create_user, delete_date, delete_user, group_name, group_desc
CREATE TABLE IF NOT EXISTS intel_l120_group (
  group_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  group_name VARCHAR(255) NOT NULL,
  group_desc TEXT
);
INSERT INTO intel_l120_group (create_user,group_name,group_desc) 
VALUES ('admin','LAB','Primary group owners');

---------------------------------------------------------------------------
-- Table: intel_l121_group_users
-- Columns: group_user_id, create_date, create_user, delete_date, delete_user,
--          group_id, user_id, expiry_date
CREATE TABLE IF NOT EXISTS intel_l121_group_users (
  group_user_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  group_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  expiry_date TIMESTAMP
  -- Optionally, add foreign keys once the reference tables exist:
  --, FOREIGN KEY (group_id) REFERENCES intel_l102_group(group_id)
  --, FOREIGN KEY (user_id) REFERENCES users(user_id)
);

---------------------------------------------------------------------------
-- Table: intel_l122_group_docs
-- Columns: group_doc_id, create_date, create_user, delete_date, delete_user,
--          group_id, doc_id, expiry_date
CREATE TABLE IF NOT EXISTS intel_l122_group_docs (
  group_doc_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  group_id INTEGER NOT NULL,
  doc_id INTEGER NOT NULL,
  expiry_date TIMESTAMP
  --, FOREIGN KEY (group_id) REFERENCES intel_l102_group(group_id)
  --, FOREIGN KEY (doc_id) REFERENCES intel_l101_docs(doc_id)
);




---------------------------------------------------------------------------
-- Table: intel_L200_process
-- Columns: process_id, create_date, create_user, delete_date, delete_user,
--          group_id, process_name, process_desc
CREATE TABLE IF NOT EXISTS intel_L200_process (
  process_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  group_id INTEGER,  -- For access control; can reference intel_l102_group(group_id)
  process_name VARCHAR(255) NOT NULL,
  process_desc TEXT
  --, FOREIGN KEY (group_id) REFERENCES intel_l102_group(group_id)
);

---------------------------------------------------------------------------
-- Table: intel_L201_process_steps
-- Columns: step_id, create_date, create_user, delete_date, delete_user,
--          process_id, step_desc, step_action, parameter_one, parameter_two
CREATE TABLE IF NOT EXISTS intel_L201_process_steps (
  step_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  process_id INTEGER NOT NULL,
  step_desc TEXT,
  step_action VARCHAR(255),
  parameter_one TEXT,
  parameter_two TEXT
  --, FOREIGN KEY (process_id) REFERENCES intel_L200_process(process_id)
);

---------------------------------------------------------------------------
-- Table: intel_L210_interaction
-- Columns: interaction_id, create_date, create_user, delete_date, delete_user,
--          process_id, current_step_id
CREATE TABLE IF NOT EXISTS intel_L210_interaction (
  interaction_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  process_id INTEGER NOT NULL,
  current_step_id INTEGER
  --, FOREIGN KEY (process_id) REFERENCES intel_L200_process(process_id)
  --, FOREIGN KEY (current_step_id) REFERENCES intel_L201_process_steps(step_id)
);

---------------------------------------------------------------------------
-- Table: intel_L211_working_notes
-- Columns: workings_id, create_date, create_user, delete_date, delete_user,
--          interaction_id, working_notes
CREATE TABLE IF NOT EXISTS intel_L211_working_notes (
  workings_id SERIAL PRIMARY KEY,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  create_user VARCHAR(50) NOT NULL,
  delete_date TIMESTAMP,
  delete_user VARCHAR(50),
  interaction_id INTEGER NOT NULL,
  working_notes TEXT
  --, FOREIGN KEY (interaction_id) REFERENCES intel_L210_interaction(interaction_id)
);
