CXXFLAGS=-g -std=c++14
TESTS_SOURCE=$(shell find . -type f -iname "test*.cpp")
TESTS_OBJS=$(TESTS_SOURCE:.cpp=.o)
TESTS_EXEC=$(TESTS_OBJS:.o=.test)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $<

test%.test: test%.o
	$(CXX) $(LDFLAGS) -o $@ $<

check: $(TESTS_EXEC)
	@for t in $(TESTS_EXEC); do echo $$t; $$t; done
test: check

clean:
	@rm -f *.o $(TESTS_EXEC)
