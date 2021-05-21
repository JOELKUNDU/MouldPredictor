CC = g++

# the build target executable:
TARGET = Predictor
CFLAGS = -I

all: $(TARGET)

$(TARGET): source.c++
$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c

clean:
$(RM) $(TARGET)