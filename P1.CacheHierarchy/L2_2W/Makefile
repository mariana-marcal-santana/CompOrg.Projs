CC = gcc
CFLAGS=-Wall -Wextra
TARGET=L2Cache2W.o
OUTFILE = L2_2W.out

all:
	$(CC) $(CFLAGS) SimpleProgram.c L2Cache2W.c -o $(TARGET)


run: $(TARGET)
	./$(TARGET) > $(OUTFILE)

clean:
	rm $(TARGET)
	rm -f $(OUTFILE)
