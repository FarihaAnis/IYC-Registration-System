def keyboardInput(caption, datatype, errormessage, defaultvalue=None):
    value = None
    isErrorInput = True
    while (isErrorInput):
        try:
            value = input(caption)
            if (defaultvalue == None):
                value = datatype(value)
            else:
                if (value == ""):
                    value = defaultvalue
                else:
                    value = datatype(value)
        except:
            print(errormessage)
        else:
            isErrorInput = False
    return value