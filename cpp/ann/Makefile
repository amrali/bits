.PHONY: all clean

ROOT_DIR = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
SRC_DIR = $(ROOT_DIR)

CXX = g++
CXXFLAGS = -std=c++11 -fPIC -Wall -Wextra -pedantic -O0 -ggdb3
CPPFLAGS = -I.
LDFLAGS = -lgd

SRCS =\
	  $(SRC_DIR)/main.cpp \
	  $(SRC_DIR)/image.cpp
O_SRCS = $(SRCS:%.cpp=%.o)
SRCS_DEST = $(ROOT_DIR)/ann

$(SRCS_DEST): $(O_SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $(O_SRCS) $(LDFLAGS)

clean:
	-rm -f $(O_SRCS) $(SRCS_DEST)
