def trim_json(s):
    brace_index = s.find('{')
    bracket_index = s.find('[')
    if brace_index == -1:
        brace_index = len(s)
    if bracket_index == -1:
        bracket_index = len(s)
    index = min(brace_index, bracket_index)
    s = s[index:]
    brace_end_index = s.rfind('}')
    bracket_end_index = s.rfind(']')
    if brace_end_index == -1:
        brace_end_index = len(s) + 1
    if bracket_end_index == -1:
        bracket_end_index = len(s) + 1
    index = max(brace_end_index, bracket_end_index)
    s = s[:index + 1]
    return s


def check_keys(dictionary, keys):
    return all(key in dictionary for key in keys)


def filter_int(string):
    filtered_string = ''.join(filter(str.isdigit, string))
    if filtered_string:
        return int(filtered_string)
    else:
        return None
