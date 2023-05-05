import sys


def create_msg(data):
    if type(data) == bytes:
        # Creating message, data will not be encoded since those are all bytes
        data_size = sys.getsizeof(data)
        msg = str(data_size)
        msg += "-"
        return msg.encode() + data
    else:
        # Creating message
        data_size = len(data)
        msg = str(data_size)
        msg += "-"
        msg += data
        return msg.encode()


def get_msg(my_socket):
    data = ''
    current_byte = ''
    try:
        # Receiving 1 byte each cycle until the length field ends
        while current_byte != '-':
            data += my_socket.recv(1).decode()
            current_byte = data[-1]
        data = data[:-1]
        data_len = int(data)
        try:
            # Receiving the data
            data = my_socket.recv(data_len)
            data = data.decode()
        except:
            # If an exception occurs, that means data is already decoded (can't decode bytes)
            pass
    except:
        return False, ""

    return True, data