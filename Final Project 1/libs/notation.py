from string import ascii_uppercase

def is_notation(notation):
    return notation[0] in ascii_uppercase and notation[1:].isnumeric()

def notation_to_index(notation, file_size):
    index = [int(file_size) - int(notation[1:]), ascii_uppercase.index(notation[0])]
    return index

def index_to_notation(index, file_size):
    notation = str(ascii_uppercase[int(index[1])]) + str(int(file_size) - int(index[0]))
    return notation

def get_files(file_size):
    return ascii_uppercase[0: int(file_size)]