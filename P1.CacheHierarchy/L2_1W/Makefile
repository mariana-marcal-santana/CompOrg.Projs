CC = gcc
CFLAGS=-Wall -Wextra
TARGET=L2Cache.o
OUTFILE = L2_1W.out

all:
	$(CC) $(CFLAGS) SimpleProgram.c L2Cache.c -o $(TARGET)


run: $(TARGET)
	./$(TARGET) > $(OUTFILE)

clean:
	rm $(TARGET)
	rm -f $(OUTFILE)
