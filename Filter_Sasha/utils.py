def read_classification_from_file(filepath):
    my_dict = {}
    with open(filepath, "rt", encoding='utf-8') as f:
        for line in f:
            key_value = line.split()
            if len(key_value) == 2:
                my_dict[key_value[0]] = key_value[1]

    return my_dict

def write_classification_to_file(filepath, my_dict):
    with open(filepath, "wt", encoding='utf-8') as f:
        for key, value in my_dict.items():
            print(key, value, file=f)

if __name__ == "__main__":
    filename = read_classification_from_file('text.txt')
    write_classification_to_file('new_text.txt', filename)

