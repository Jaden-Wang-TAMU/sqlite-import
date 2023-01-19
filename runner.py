import sys

from import_all import Import

if __name__ == '__main__':
    # Call the class and run your code here
    #
    # You can assume that sys.argv[1] is the name
    # of the file to import and that it exists.
    #
    my_obj=Import()
    my_obj.import_all(sys.argv[1])
