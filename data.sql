CREATE TABLE IF NOT EXISTS time_tabel (admin_id VARCHAR(255), time VARCHAR(255), duratin VARCHAR(255), day VARCHAR(255), subject VARCHAR(255), branch VARCHAR(244), sem VARCHAR(233));
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','11:00:00','1','Monday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','13:30:00','2','Monday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','11:00:00','1','Tuesday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','14:30:00','2','Tuesday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','13:30:00','2','Wednesday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','08:45:00','2','Thursday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','11:00:00','2','Thursday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','08:45:00','1','Friday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','13:30:00','2','Friday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','15:30:00','1','Friday','AOA','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('101','09:45:00','3','Friday','Mini project','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('102','13:30:00','1','Tuesday','DBMS','CSE','4');
INSERT INTO time_tabel (admin_id,time,duratin,day,subject,branch,sem) VALUES ('102','15:30:00','1','Friday','DBMS','CSE','4');
CREATE TABLE IF NOT EXISTS admin (admin_id VARCHAR(255) PRIMARY KEY,subject VARCHAR(255), branch VARCHAR(244), sem VARCHAR(233));
INSERT INTO admin (admin_id,subject,branch,sem) VALUES ('102','DBMS','CSE','4');
INSERT INTO admin (admin_id,subject,branch,sem) VALUES ('101','AOA','CSE','4');
CREATE TABLE IF NOT EXISTS facedata4 (id INT AUTO_INCREMENT PRIMARY KEY,admin_id VARCHAR(10),branch VARCHAR(100),subject VARCHAR(100),sem VARCHAR(100), excel_data LONGBLOB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
INSERT INTO facedata4 (admin_id,branch,subject,sem,excel_data) VALUES ('101','CSE','AOA','4',NULL);
INSERT INTO facedata4 (admin_id,branch,subject,sem,excel_data) VALUES ('101','CSE','Mini project','4',NULL);
INSERT INTO facedata4 (admin_id,branch,subject,sem,excel_data) VALUES ('102','CSE','DBMS','4',NULL);
INSERT INTO facedata4 (admin_id,branch,subject,sem,excel_data) VALUES ('102','CSE','Mini project','4',NULL);
