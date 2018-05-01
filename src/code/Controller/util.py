class Util:
    
    @staticmethod
    def string_to_int_list(text_play):
        play = list(map(int, text_play.split(" ")))

        if len(play) != 4:
            return []
        else:
            return play
    