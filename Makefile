OBJS	= source.o
SOURCE	= source.cpp
HEADER	= 
OUT	= Predictor-linux
CC	 = g++
FLAGS	 = -g -c -Wall
LFLAGS	 = 

all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

source.o: source.cpp
	$(CC) $(FLAGS) source.cpp -std=c17


clean:
	rm -f $(OBJS) $(OUT)