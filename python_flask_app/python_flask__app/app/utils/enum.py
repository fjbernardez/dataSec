import enum

class EnumUtils(enum.Enum):
    key = "I9fWp52DOM1T4hzgqaHH2TUlkCvKwTLNDznh9ffJRsw="
    query = "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE ( TABLE_SCHEMA IN (SELECT SCHEMA_NAME from information_schema.schemata WHERE SCHEMA_NAME RLIKE '[^ information_schema, sys, performance_schema, mysql]') ) ORDER BY TABLE_SCHEMA, TABLE_NAME;"
