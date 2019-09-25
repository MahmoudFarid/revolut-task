import argparse
import json
import sys


def read_input(from_file=False, file=None):
    ''' Read input from a file or stdin

    Args:
        from_file (bool): Read input from file not stdin

    Returns:
        Json data
    '''
    if from_file:
        with open(file, 'r') as json_data:
            json_data = json.loads(json_data.read())
    else:
        input_text = ''
        for line in sys.stdin.readlines():
            input_text += line
        json_data = json.loads(input_text)

    return json_data


def write_output(final_output):
    """ Write final_output to stdout

    Args:
        final_output (dict): Output data

    Returns:
        None
    """
    sys.stdout.write(json.dumps(final_output, indent=2))
    sys.stdout.write("\n")
    sys.stdout.close()


def is_valid_input(input_data):
    """ make sure that all dicts have the same keys

    Args:
        input_data (list): list of dicts

    Returns:
        True or False
    """
    first_keys = input_data[0].keys()
    for dict_data in input_data:
        if not dict_data.keys() == first_keys:
            sys.stdout.write("Incorrect data, All dicts should have the same keys {}".format(first_keys))
            return False
    return True


def is_valid_key(input_data, keys):
    """ make sure the key is valid agains input_data

    Args:
        input_data (list): list of dicts
        key (str): key

    Returns:
        True or False
    """
    # we call this method after validating is_valid_input()
    first_keys = input_data[0].keys()
    for key in keys:
        if key not in first_keys:
            sys.stdout.write("Key {} not found in data keys {}".format(key, first_keys))
            return False
    return True


def prepare_output(input_data, keys):
    ''' Prepares the final_output dict based on keys

    Args:
        input_data (dict): data from the file or stdin
        keys (list): list of strings that passed in command line to be a leaf value of final_output

    Returns:
        Nested dictionary of dictionaries of arrays, with the specified keys
    '''
    final_output = {}
    temp = final_output  # will override final_output because dict is mutable

    for data in input_data:
        last_key = keys[-1]
        for key in keys:
            if key is not last_key:
                # will pop the value of the key and add it into final_output
                # and pass the empty dict to temp to add the next value into it
                # this is mainly because the dict is mutable and passed by refrence
                if data[key] not in temp:
                        temp[data[key]] = {}
                temp = temp[data.pop(key)]
            else:
                if data.get(key) in temp:
                    # in case we pass only one key and the value of that key already exists
                    # then we append the data into a list not override the old one
                    temp[data.pop(key)].append(data)
                else:
                    # this will be called only when it's the last key
                    # we will pass the remaining data as a list of dict
                    temp[data.pop(key)] = [data]

        # to save the new dict after adding the nesting_level
        temp = final_output

    return final_output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Return a nested dictionary of dictionaries of arrays, with keys specified in arguments')
    # Receives a list of keys to be parsed
    parser.add_argument('keys', type=str, nargs='+', help='Nesting key order')
    parser.add_argument('-f', nargs='?', type=str, help='Name of the file to read from instead of STDIN')
    args = parser.parse_args()

    if args.f:
        input_data = read_input(from_file=True, file=args.f)
    else:
        input_data = read_input()
    if is_valid_input(input_data) and is_valid_key(input_data, args.keys):
        output_dict = prepare_output(input_data, args.keys)
        write_output(output_dict)
