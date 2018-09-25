import re

ARRAY_START = "##[##"
ARRAY_END = "##]##"

LABEL_PATTERN = '##[a-zA-Z]+\|[a-zA-Z]##'
POSSIBLE_LABEL_PATTERN = '(.+)'

ARRAY_START_REGEX = '.+##\[##'
ARRAY_END_REGEX = '##\]##.+'


def is_array_start(line):
    return ARRAY_START in line


def is_array_end(line):
    return ARRAY_END in line


def get_label(format_line):
    try:
        label = re.search(LABEL_PATTERN, format_line, re.IGNORECASE).group(0)
        return label.replace(ARRAY_START, '').replace(ARRAY_END, '').split('|')[0].replace("##", "")
    except:
        return None


def is_number(format_line):
    try:
        label = re.search(LABEL_PATTERN, format_line, re.IGNORECASE).group(0)
        return label.replace(ARRAY_START, '').replace(ARRAY_END, '').split('|')[1].replace("##", "") == 'N'
    except:
        return False


def get_value(format_line, data_line):
    rr = re.search(ARRAY_START_REGEX, format_line)
    try:
        format_line = format_line.replace(rr.group(0), '')
    except:
        pass
    try:
        label = re.search(LABEL_PATTERN, format_line, re.IGNORECASE).group(0)
        regex = format_line.replace(label, POSSIBLE_LABEL_PATTERN)
        return re.search(regex, data_line).group(1)
    except:
        return None


def is_valid(data_line, format_line):  # write better
    rr = re.search(ARRAY_START_REGEX, format_line)
    try:
        format_line = format_line.replace(rr.group(0), '')
    except:
        pass

    label = re.search(LABEL_PATTERN, format_line, re.IGNORECASE).group(0)
    regex = format_line.replace(label, POSSIBLE_LABEL_PATTERN)
    try:
        ok = re.search(regex, data_line).group(0)
        return True
    except:
        pass
    return False


def add_field_to_result(field_converters, field_name, result, value, ignored_fields):
    converters = field_converters.get(field_name)
    if converters is not None:
        for converter in converters:
            new_field_name = converter["new_field_name"]
            result[new_field_name] = converter["converter"](value)
    if ignored_fields is None or field_name not in ignored_fields:
        result[field_name] = value


def parse(format, data, field_converters={}, ignored_fields=[]):
    format_lines = format.split('\n')
    data_lines = data.split('\n')

    data_index = -1
    format_index = -1

    array_start_index = 0
    results = []
    result = {}
    while data_index + 2 <= len(data_lines) and format_index < len(format_lines) - 1:
        data_index += 1
        format_index += 1

        if format_lines[format_index] == data_lines[data_index]:
            continue
        if is_array_start(format_lines[format_index]):
            array_start_index = format_index
        if is_array_end(format_lines[format_index]):
            array_length = format_index - array_start_index
            format_index -= array_length
            results.append(result)
            result = {}

        format_label = get_label(format_lines[format_index])
        number = is_number(format_lines[format_index])
        if format_label is not None:
            if is_valid(data_lines[data_index], format_lines[format_index]):
                value = get_value(format_lines[format_index], data_lines[data_index])
                value = value.replace('"', '')
                if number:
                    add_field_to_result(field_converters, format_label, result, float(value), ignored_fields)
                else:
                    add_field_to_result(field_converters, format_label, result, value, ignored_fields)
                # warn('%r||%s|%s|: |%s| --> |%s|' % (
                # number, format_label, value, format_lines[format_index], data_lines[data_index]))
            else:
                data_index -= 1
    if len(results) < 1:
        results.append(result)
    return results


def jpar_with_file(data_path, format_path, field_converters):
    pass  # implement


def jpar_with_url(data_path, format_path, field_converters):
    pass  # implement
