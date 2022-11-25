##########################
##### COMPILER FLAGS #####
##########################

CFLAGS= -Wall -Wextra -pedantic -fdiagnostics-color=always
CFLAGS+=$(CPPFLAGS) -O0 -g3 -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls
LDFLAGS+=-fsanitize=address


############################
##### FILES TO COMPILE #####
############################

# Program:
list_test: list.o list_test.o
table_test: table.o table_test.o list.o dico.o
dico_test: list.o table.o dico.o dico_test.o
correction: list.o table.o dico.o correction.o

# Format is:
## program_name: file_name1.o file_name2.o


# Object files
list.o: list.c list.h
list_test.o: list.h list_test.c
table.o: list.h table.c table.h
table_test.o: list.h table.h table_test.c
dico.o: table.h list.h dico.c
dico_test.o: table.h list.h dico.h dico_test.c
correction.o : table.h list.h dico.h correction.c




# Format is:
## file_name.o: <dependency.o> <header_file.h> file_name.c


##########################
##### OTHER COMMANDS #####
##########################

clean:
	rm -f *.o *_test
	rm -f correction

# For the test, replace `linked_list_int_test` with your program name.
test: linked_list_int_test
	./linked_list_int_test

.SILENT: clean
