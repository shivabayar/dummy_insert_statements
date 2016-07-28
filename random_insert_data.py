import string
from random import choice
from random import randint
from string import ascii_uppercase

SCHEMA_NAME = "DWNOVA"
TABLE_NAME = "trade"
insert = 'INSERT INTO "<SCHEMA_NAME>".<TABLE_NAME> (<columns>) VALUES (<values>);'
FILE_NAME = "table_schema.txt"


def generate_random_number(n):
    return randint(n, n + 1)


def generate_random_decimal(size):
    return generate_random_number(size) / 10


def generate_random_str(size):
    return ''.join(choice(ascii_uppercase) for i in range(size))


def get_insert_statements(lines_, inserts):
    columns = list()
    for line in lines_:
        line = line.split(',')
        if line[1].__contains__("VARCHAR"):
            columns.append((line[0], "'" + generate_random_str(int(line[2])) + "'"))
        elif line[1].__contains__("FLOAT"):
            columns.append((line[0], str(float(generate_random_decimal(int(line[2]))))))
        elif line[1].__contains__("NUMBER"):
            columns.append((line[0], str(generate_random_number(int(line[2])))))
        elif line[1].__contains__("DATE"):
            columns.append((line[0], "TO_DATE('2016/07/27 21:02:44', 'yyyy/mm/dd hh24:mi:ss')"))

    insert_statement = string.replace(inserts, "<columns>", ','.join(c[0] for c in columns))
    insert_statement = string.replace(insert_statement, "<values>", ','.join(c[1] for c in columns))
    insert_statement = string.replace(insert_statement, "<SCHEMA_NAME>", SCHEMA_NAME)
    insert_statement = string.replace(insert_statement, "<TABLE_NAME>", TABLE_NAME)

    return insert_statement


if __name__ == "__main__":
    file_ = open(FILE_NAME, "r+")

    lines = file_.readlines()
    insert_statements = list()

    for i in range(0, 100):
        insert_statements.append(get_insert_statements(lines, insert))

    for i in insert_statements:
        print i
    file_.close()
