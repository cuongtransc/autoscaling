# PolicyDB
# apps.enabled: 0-not scaled, 1-scaled
# apps.locked: 0-unlocked, 1-locked
# apps.next_time: time in the future the app'll be checked for scaling
#   next_time = last success caused by policyX + policyX.cooldown_period
# policies.metric_type: 0-CPU, 1-memory
# policies.cooldown_period: in second
# policies.measurement_period: in second
# deleted: 0-active, 1-deleted
DROP DATABASE IF EXISTS policydb;
CREATE DATABASE policydb;
USE policydb;
CREATE TABLE apps(\
    Id INT AUTO_INCREMENT PRIMARY KEY, \
    app_uuid VARCHAR(255), \
    name VARCHAR(255), \
    min_instances SMALLINT UNSIGNED, \
    max_instances SMALLINT UNSIGNED, \
    enabled TINYINT UNSIGNED, \
    locked TINYINT UNSIGNED, \
    next_time INT \
);
CREATE TABLE policies(\
    Id INT AUTO_INCREMENT PRIMARY KEY, \
    app_uuid VARCHAR(255), \
    policy_uuid VARCHAR(255), \
    metric_type TINYINT UNSIGNED, \
    upper_threshold FLOAT, \
    lower_threshold FLOAT, \
    instances_out SMALLINT UNSIGNED, \
    instances_in SMALLINT UNSIGNED, \
    cooldown_period SMALLINT UNSIGNED, \
    measurement_period SMALLINT UNSIGNED, \
    deleted TINYINT UNSIGNED \
    
);
# tuna
CREATE TABLE crons(\
    Id INT AUTO_INCREMENT PRIMARY KEY, \
    app_uuid VARCHAR(255), \
    cron_uuid VARCHAR(255), \
    min_instances SMALLINT UNSIGNED, \
    max_instances SMALLINT UNSIGNED, \
    cron_string VARCHAR(255), \
    deleted TINYINT UNSIGNED \
);
# end tuna
-----

# Test data

# Stresser
INSERT INTO apps(app_uuid, name, min_instances, max_instances, enabled, locked, next_time) \
VALUES ("f5bfcbad-7daa-4317-97cc-e42ae46b6ad1", "java-allocateMemory", 1, 5, 1, 0, 0);
INSERT INTO policies(app_uuid, policy_uuid, metric_type, upper_threshold, lower_threshold, instances_out, instances_in, cooldown_period, measurement_period, deleted) \
VALUES ("f5bfcbad-7daa-4317-97cc-e42ae46b6ad1", "b3da4493-58f1-4d65-bf43-e52e7de62151", 1, 0.7, 0.3, 1, 1, 30, 10, 0);
# INSERT INTO policies(app_uuid, policy_uuid, metric_type, upper_threshold, lower_threshold, instances_out, instances_in, cooldown_period, measurement_period, deleted) \
# VALUES ("f5bfcbad-7daa-4317-97cc-e42ae46b6ad1", "b3da4493-58f1-4d65-bf43-e52e7dpolicy", 1, 0.7, 0.3, 1, 1, 30, 10, 0);
INSERT INTO crons(app_uuid, cron_uuid, min_instances, max_instances, cron_string, deleted) \
VALUES ("f5bfcbad-7daa-4317-97cc-e42ae46b6ad1", "b3da4493-58f1-4d65-bf43-e52eacascron", 1, 10, "* * * * * *", false);