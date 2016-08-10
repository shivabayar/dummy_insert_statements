import string
from random import choice
from random import randint
from string import ascii_uppercase

insert = 'INSERT INTO "<SCHEMA_NAME>".<TABLE_NAME> (<columns>) VALUES (<values>);'
FILE_NAME = "table_schema.txt"


class Row:
    options = list()

    def __init__(self, column_name, data_type, size):
        self.column_name = column_name
        self.data_type = data_type
        self.size = size

    def set_options(self, options):
        self.options = options

    def get_options(self):
        return self.options


def generate_random_number(n):
    return randint(n, n + 1)


def generate_random_decimal(size):
    return generate_random_number(size) / 10


def generate_random_str(size):
    if size > 5:
        size = 5
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


def get_dummy_data(row_objs):
    line = ''
    for row in row_objs:
        opt_len = len(row.options)
        temp = ''
        if opt_len > 0 and row.options[0] != '':
            if str(row.data_type).__contains__("VARCHAR2"):
                temp = row.options[randint(0, opt_len - 1)]
            elif str(row.data_type).__contains__("FLOAT"):
                temp = str(float(row.options[randint(0, opt_len - 1)]))
            elif str(row.data_type).__contains__("NUMBER"):
                temp = str(int(row.options[randint(0, opt_len - 1)]))
            elif str(row.data_type).__contains__("DATE"):
                temp = str("TO_DATE('01-Jul-16', 'dd-Mon-yy')")
        else:
            temp = ''
            if str(row.data_type).__contains__("VARCHAR2"):
                temp = generate_random_str(int(row.size))
            elif str(row.data_type).__contains__("FLOAT"):
                temp = str(float(generate_random_decimal(int(row.size))))
            elif str(row.data_type).__contains__("NUMBER"):
                temp = generate_random_number(int(row.size))
            elif str(row.data_type).__contains__("DATE"):
                temp = '2016/07/27 21:02:44'

        line += str(temp) + ','

    print line


def format_lines(all_lines):
    all_lines_len = len(all_lines)
    rows = list()
    i = 0
    while i < all_lines_len:
        options = list()
        all_lines[i] = all_lines[i].replace('\n', '')
        line = all_lines[i].split('"')

        if len(line) >= 2:
            str(line[0]).replace(' ', '')
            options.append(line[1])
            splitted_line = all_lines[i]
            splitted_line = str(splitted_line).replace(' ', '').split(',')
            row = Row(splitted_line[0].upper(), splitted_line[1], splitted_line[2])
            i += 1
            while not str(all_lines[i]).__contains__('"'):
                temp_line = str(all_lines[i]).replace('"', '').replace('\n', '')
                if temp_line != '':
                    options.append(temp_line)
                i += 1
            temp_line = str(all_lines[i]).replace('\n', '').replace('"', '')
            if temp_line != '':
                options.append(temp_line)
            row.set_options(options)
            rows.append(row)
        elif len(line) == 1:
            one_option_line = str(all_lines[i]).split(',')
            if len(one_option_line) == 4 and not one_option_line[3].__contains__('"'):
                option = str(one_option_line[3]).replace('\n', '').replace(' ', '')
                if not option.lower().__eq__("notpopulated") and not option.lower().__eq__("nodata"):
                    options.append(option)
            row = Row(one_option_line[0].upper(), one_option_line[1], one_option_line[2])
            row.set_options(options)
            rows.append(row)
        # print options
        i += 1

    return rows


def get_header(row_objs):
    line = ''
    for row in row_objs:
        line += row.column_name + ','

    print line


if __name__ == "__main__":
    file_ = open(FILE_NAME, "r+")

    lines = file_.readlines()
    insert_statements = list()
    rows = format_lines(lines)
    get_header(rows)
    i = 10
    while i > 0:
        get_dummy_data(rows)
        i -= 1

    file_.close()
