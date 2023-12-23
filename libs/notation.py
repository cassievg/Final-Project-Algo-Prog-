from string import ascii_uppercase

# Check notation. If the first character is a capital letter and the rest is numbers, it is a notation
def is_notation(notation):
    return notation[0] in ascii_uppercase and notation[1:].isnumeric()

# Converts chess notation form to index (the coordinate that is recognised by the board)
def notation_to_index(notation, file_size):
    index = [int(file_size) - int(notation[1:]), ascii_uppercase.index(notation[0])]
    return index

# Converts index to chess notation form
def index_to_notation(index, file_size):
    notation = str(ascii_uppercase[int(index[1])]) + str(int(file_size) - int(index[0]))
    return notation

# This is just to get the file of the piece
def get_files(file_size):
    return ascii_uppercase[0: int(file_size)]