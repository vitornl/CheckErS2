class Util:
    
    @staticmethod
    def string_to_int_tuple(string):
        tup = tuple(map(int, string.split(" ")))
        return tup

    @staticmethod
    def int_tuple_to_string(int_tuple):
        return str(int_tuple[0]) + " " + str(int_tuple[1])