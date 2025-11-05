-- Select the database to use
USE bug_tracker_db;

-- ----------------------------
--  Wipe existing data
-- ----------------------------
SET FOREIGN_KEY_CHECKS = 0; -- Disable foreign key checks to allow clearing tables
TRUNCATE TABLE Comments;
TRUNCATE TABLE Issues;
TRUNCATE TABLE Users;
TRUNCATE TABLE Projects;
SET FOREIGN_KEY_CHECKS = 1; -- Re-enable foreign key checks

-- ----------------------------
--  Populate 10 Users
-- ----------------------------
INSERT INTO Users (username, email) VALUES
('alice_dev', 'alice@example.com'),       -- ID: 1
('bob_manager', 'bob@example.com'),      -- ID: 2
('charlie_qa', 'charlie@example.com'),   -- ID: 3
('diana_dev', 'diana@example.com'),      -- ID: 4
('erin_ux', 'erin@example.com'),         -- ID: 5
('frank_devops', 'frank@example.com'),   -- ID: 6
('grace_qa', 'grace@example.com'),       -- ID: 7
('heidi_pm', 'heidi@example.com'),       -- ID: 8
('ivan_backend', 'ivan@example.com'),    -- ID: 9
('judy_frontend', 'judy@example.com');   -- ID: 10

-- ----------------------------
--  Populate 4 Projects
-- ----------------------------
INSERT INTO Projects (name, description) VALUES
('Project Phoenix', 'The new web application front-end.'),      -- ID: 1
('Project Zeta', 'The backend API and database migration.'),   -- ID: 2
('Project Omega', 'The mobile application (iOS and Android).'), -- ID: 3
('Project Atlas', 'Internal DevOps and CI/CD pipeline.');      -- ID: 4

-- ----------------------------
--  Populate 20 Issues
-- ----------------------------
-- (project_id, reported_by_user_id, assigned_to_user_id, title, description, status, priority, created_at)
INSERT INTO Issues (project_id, reported_by_user_id, assigned_to_user_id, title, description, status, priority, created_at) VALUES
-- Project 1 (Phoenix)
(1, 1, 10, 'User login fails', 'Users cannot log in with correct credentials.', 'In Progress', 'Critical', '2025-10-01 09:15:00'),
(1, 5, 10, 'Submit button misaligned on Chrome', 'The CSS is broken on the /checkout page.', 'Open', 'Low', '2025-10-02 11:00:00'),
(1, 3, 5, 'Incorrect colors in dark mode', 'The UX-approved color palette is not being used.', 'Open', 'Medium', '2025-10-05 10:00:00'),
(1, 10, 10, 'Footer links are broken', 'All links in the site footer lead to a 404 page.', 'Testing', 'Medium', '2025-10-06 14:00:00'),
(1, 5, 5, 'Font size is unreadable on mobile', 'The body text font size is too small on screens < 400px.', 'Closed', 'Low', '2025-10-03 11:00:00'),
-- Project 2 (Zeta)
(2, 2, 9, 'API gateway returns 503 error', 'The /api/v2/users endpoint is down.', 'Testing', 'High', '2025-10-03 14:30:00'),
(2, 4, 9, 'Database schema needs indexing', 'The `Issues` table query is too slow. Needs indexing on `project_id`.', 'Open', 'Medium', '2025-10-04 16:00:00'),
(2, 9, 9, 'Incorrect user permissions on /admin', 'Users with role ''editor'' can access admin endpoints.', 'In Progress', 'High', '2025-10-07 10:10:00'),
(2, 4, 4, 'Password reset token expires too quickly', 'Password reset tokens should last 1 hour, but expire in 5 minutes.', 'In Progress', 'Medium', '2025-10-07 15:20:00'),
(2, 1, 9, 'CORS error when calling API from staging', 'The staging frontend URL is not in the allowed origins list.', 'Closed', 'Medium', '2025-10-02 18:00:00'),
-- Project 3 (Omega)
(3, 5, 4, 'App crashes on splash screen (Android)', 'The app fails to load on Android 13 devices.', 'Closed', 'Critical', '2025-10-01 10:00:00'),
(3, 3, 4, 'Cannot swipe to delete items from cart', 'Swipe gesture is not working on the main cart list view.', 'Open', 'Medium', '2025-10-06 13:00:00'),
(3, 7, 4, 'Push notifications are not received on iOS', 'APNS integration seems to be misconfigured.', 'Testing', 'High', '2025-10-07 09:00:00'),
(3, 8, NULL, 'Biometric login fails after 3 attempts', 'App should fall back to passcode, but it locks the user out.', 'Open', 'High', '2025-10-08 11:00:00'),
(3, 5, 5, 'Splash screen logo is pixelated', 'The main logo asset is low-resolution.', 'Open', 'Low', '2025-10-08 12:00:00'),
-- Project 4 (Atlas)
(4, 6, 6, 'Jenkins build pipeline is failing', 'The main branch build has been red for 3 hours.', 'In Progress', 'Critical', '2025-10-08 10:00:00'),
(4, 2, 6, 'Staging server disk space is full', 'Alerts firing for /dev/sda1 at 99% capacity.', 'Closed', 'High', '2025-10-07 17:00:00'),
(4, 6, 6, 'Need to update Docker base image', 'Base image has a known security vulnerability (CVE-2025-1234).', 'Open', 'Medium', '2025-10-08 14:00:00'),
(4, 9, 6, 'Terraform script fails on apply', 'Error when trying to provision new S3 bucket.', 'In Progress', 'High', '2025-10-08 15:00:00'),
(4, 8, NULL, 'Set up automated database backups', 'We need nightly backups for the new Zeta prod database.', 'Open', 'Medium', '2025-10-05 16:00:00');

-- ----------------------------
--  Populate 25 Comments
-- ----------------------------
-- (issue_id, user_id, body)
INSERT INTO Comments (issue_id, user_id, body) VALUES
(1, 2, 'Confirming this is a P0 bug. All hands on deck.'),
(1, 10, 'I am working on a fix now. Should be pushed to staging in an hour.'),
(1, 3, 'QA is standing by to test the fix.'),
(2, 5, 'Attaching screenshot of the alignment issue.'),
(3, 8, 'This is blocking the new feature release. Bumping priority.'),
(4, 3, 'Reproduced. This is a regression from the last patch.'),
(6, 2, 'Is this related to the last deployment?'),
(6, 9, 'Yes, I rolled back the change. @charlie_qa can you re-test?'),
(6, 3, 'Retesting now... looks good. Moving to Testing.'),
(7, 9, 'I will handle this after the P0 is fixed.'),
(8, 9, 'I''ve identified the bug. It''s a logic error in the permissions middleware.'),
(9, 4, 'This is a frustrating user experience. Marking as high priority.'),
(10, 6, 'I''ve updated the CORS policy on the staging API gateway.'),
(10, 1, 'Confirmed fixed, thanks Frank! Closing.'),
(11, 4, 'Fix was deployed in v1.0.1. Closing this issue.'),
(12, 10, 'This might be an issue with the gesture handler library.'),
(13, 4, 'The APNS auth key might have expired. Checking developer portal.'),
(14, 8, 'This is a critical security and accessibility issue.'),
(14, 3, 'Able to reproduce on our test devices.'),
(16, 6, 'The build script is failing on the unit test step. Looking at logs.'),
(17, 6, 'I''ve cleared the build cache. Should be resolved. Closing.'),
(18, 6, 'Working on this. I will build a new base image and push to ECR.'),
(19, 6, 'Found the issue. It was a typo in the IAM policy. Fix is pushed.'),
(20, 2, 'Agreed. @frank_devops please prioritize this.'),
(20, 6, 'Acknowledged. I will set up a cron job on the db server.');