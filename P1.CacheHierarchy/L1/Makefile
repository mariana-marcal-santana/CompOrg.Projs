CC = gcc
CFLAGS=-Wall -Wextra
TARGET=L1Cache.o
OUTFILE = L1.out

all:
	$(CC) $(CFLAGS) SimpleProgram.c L1Cache.c -o $(TARGET)


run: $(TARGET)
	./$(TARGET) > $(OUTFILE)

clean:
	rm $(TARGET)
	rm -f $(OUTFILE)
