CC = g++

TARGET = Predictor-linux

all: $(TARGET)

$(TARGET): source.cpp
$(CC) -o $(TARGET) source.cpp

