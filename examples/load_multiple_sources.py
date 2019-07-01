from sitdown.readers import ABNAMROReader

reader = ABNAMROReader()

mutations1 = reader.read(r"C:\Users\z428172\Documents\financien\2017\mutaties\TXT180114183005.TAB")
mutations2 = reader.read(r"C:\Users\z428172\Documents\financien\2017\mutaties\TXT180224225233.TAB")

all = mutations1 | mutations2
