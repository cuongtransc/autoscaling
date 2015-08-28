## PolicyDB Database structure
___________________________
> `apps` table

|Field|Data type|Description|
|---|---|---|
|Id|INT|AUTO_INCREMENT PRIMARY KEY|
|app_uuid|VARCHAR(255)|--|
|name|VARCHAR(255)|--|
|min_instances|SMALLINT UNSIGNED|--|
|max_instances|SMALLINT UNSIGNED|--|
|enabled|TINYINT UNSIGNE|--|
|locked|TINYINT UNSIGNE|--|
|next_time|INT|--|

___________________________
> `policies` table

|Field|Data type|Description|
|---|---|---|
|Id|INT|AUTO_INCREMENT PRIMARY KEY|
|app_uuid|VARCHAR(255)|--|
|policy_uuid|VARCHAR(255)|--|
|metric_type|TINYINT UNSIGNED|--|
|upper_threshold|FLOAT|--|
|lower_threshold|FLOAT|--|
|instances_out|SMALLINT UNSIGNED|--|
|instances_in|SMALLINT UNSIGNED|--|
|cooldown_period|SMALLINT UNSIGNEDSMALLINT UNSIGNED|--|
|measurement_period|SMALLINT UNSIGNED|--|
|deleted|TINYINT UNSIGNE|--|

___________________________
> `crons` table

|Field|Data type|Description|
|---|---|---|
|Id|INT|AUTO_INCREMENT PRIMARY KEY|
|app_uuid|VARCHAR(255)|--|
|cron_uuid|VARCHAR(255)|--|
|min_instances|SMALLINT UNSIGNED|--|
|max_instances|SMALLINT UNSIGNED|--|
|cron_string|VARCHAR(255)|--|
|deleted|TINYINT UNSIGNED|--|

