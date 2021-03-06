import Sorter, Interpreter

class OpBuild:
    Dest = ''
    SortFiles = []

    def __init__(self,DestIn, SortFilesIn):
        self.Dest = DestIn  # hold string of file destination to pass to sorter
        self.SortFiles = SortFilesIn  # hold list of files to sort to pass to sorter

    # noinspection PyUnreachableCode
    def BuildOps(self, TokenType):  #check syntax and build operation
        opList = []
        state = 0

        opbuilder = [0, '', '', '']  # [operator, operand 1, mod 1, operand 2, mod 2]

        for x in TokenType:

            # path statement
            if ((x[0] == "path") or (x[0] == "clear")) and (state == 0):
                #state = 1
                state = 0
                opbuilder[0] = 0
                opbuilder[1] = x
                opList.append(opbuilder)
                opbuilder = [0, '', '', '']

            # if filename(.modname)(!)=string
            # name
            elif (x[0] == "filename" or x[0] == "metaname") and (state == 0):
                state = 2
                opbuilder[1] = x
            # name(.)
            elif (x[0] == "dot") and (state == 2):
                state = 3
            # name(.modname)
            elif (x[0] == "modname") and (state == 3):
                opbuilder[2] = x
                state = 4
            # name(.modname)(!)
            elif (x[0] == "inv") and (state == 4 or state == 2):
                opbuilder[0] = 6
                state = 5
            # name(.modname)(!)=
            elif (x[1] == "=") and ((state == 2) or (state == 4) or (state == 5)):
                mod = False
                if opbuilder[0] == 6:
                    mod = True
                opbuilder[0] = self.GetEquiv(x[1],mod)
                state = 6
            # name(.modname)(!)= string
            elif (x[0] == "string") and (state == 6):
                state = 7
                opbuilder[3] = x

            # if filesize = size
            # filesize
            elif (x[0] == "filesize") and (state == 0):
                state = 8
                opbuilder[1] = x
            # filesize (!)
            elif (x[0] == "inv") and (state == 8):
                opbuilder[0] = 6
                state = 9
            # filesize(!)=
            elif (x[0] == "equivalence") and ((state == 8) or (state == 9)):
                mod = False
                if opbuilder[0] == 6:
                    mod = True
                opbuilder[0] = self.GetEquiv(x[1], mod)
                state = 10
            # filesize (!)= size
            elif (x[0] == "size") and (state == 10):
                state = 7
                opbuilder[3] = x

            # if filetime(!)= time
            # filetime
            elif x[0] == "filetime" and (state == 0):
                opbuilder[1] = x
                state = 12
            # filetime(!)
            elif (x[0] == "inv") and (state == 12):
                opbuilder[0] = 6
                state = 15
            # filetime(!)=
            elif (x[0] == "equivalence") and (state == 15 or state == 12):
                mod = False
                if opbuilder[0] == 6:
                    mod = True
                opbuilder[0] = self.GetEquiv(x[1], mod)
                state = 16
            # filetime(!)= date
            elif (x[0] == "time" or x[0] == "date") and (state == 16):
                state = 7
                opbuilder[3] = x

            # :end if
            elif (x[0] == "endif") and ((state == 7)):
                opList.append(opbuilder)
                opbuilder = [0, '', '', '']
                state = 0

            # end line after path and clear
            elif (x[0] == "endline") and ((state == 1)):
                state = 0
                #opList.append(opbuilder)
                #opbuilder = [0, '', '', '']
            # end line after if(s)
            elif x[0] == "endline" and state == 0:
                # opbuilder[1] = x
                # opbuilder[0] = 1
                # opList.append(opbuilder)
                # opbuilder = [0, '', '', '']
                state = 0

            else:
                op_error = f"Invalid operation: {x[1]}"
                print(op_error)
                # print(state)
                return op_error

        Sorter.sorter(opList, self.Dest, self.SortFiles)

    def GetEquiv(self, symbol, mod = False):

        if symbol == '=':     # 1 is =, 6 is !=
            if mod:
                return 6
            else:
                return 1
        elif symbol == '>=':  # 2 is >=
            if mod:
                return 3
            else:
                return 2
        elif symbol == '<':   # 3 is <
            if mod:
                return 2
            else:
                return 3
        elif symbol == '<=':  # 4 is <=
            if mod:
                return 5
            else:
                return 4
        elif symbol == '>':   # 5 is >
            if mod:
                return 4
            else:
                return 5
        else:
            return 7          # 7 is invalid symbol
