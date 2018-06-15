INSERT INTO users
    (username, email, granules_processed, is_admin, is_authorized) VALUES
    ('wbhorn', 'wbhorn@alaska.edu', 0, true, true);


INSERT INTO processes
(name, script, suffix, database_info_required, description, ami_id, ec2_size, supports_pair_processing, text_id)
VALUES
('Notify Only', 'proc_bla.py', 'hello', false, 'Notify the user about new data', 'ami-xxxxxxxx', '1billion', false, 'notify');


