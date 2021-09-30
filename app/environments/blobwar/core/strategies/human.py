


from  environments.blobwar.core.strategies.strategy import*


class Human(Strategy):

    def __init__(self):
        pass

    def name(self):
        return "Human"

    def __ask_cell__(self,is_start=True):
        prompt=None
        if is_start:
            prompt=":"

        else :
            prompt=":"

        line=input(prompt)

        coords=line.strip().split(" ")

        if len(coords)==1:
            return (  int(int(coords[0])/10),int(int(coords[0])%10))
        if len(coords)==2:
            return ( int(int (coords[0])), int(int(coords[1])))

        return None




    def __ask_move__(self):
        print("Enter start point")
        source=None
        while(source==None):
            source=self.__ask_cell__(is_start=True)

        print("Enter end point")
        dest=None
        while dest==None:
            dest=self.__ask_cell__(is_start=False)


        return [(source[0],source[1]) , (dest[0],dest[1])]



    def compute_next_nove(self,configuration):
        if len(configuration.movements())>0:
            while(True):
                mvt=self.__ask_move__()

                if configuration.check_move(mvt):

                    return mvt
                else:
                    print("Invalid move : check your color")

        else :
            return None



