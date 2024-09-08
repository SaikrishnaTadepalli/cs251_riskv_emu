# Compiler
CXX := g++

# Compiler flags
CXXFLAGS := -std=c++11 -Wall -Wextra

# Directories
SRC_DIR := ./emulator
BUILD_DIR := ./build

# Source files
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

# Target executable
TARGET := main

# Main target
$(TARGET): $(OBJS) $(BUILD_DIR)/main.o
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile each source file into object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/main.o: main.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Clean target
clean:
	rm -rf $(BUILD_DIR) $(TARGET)

.PHONY: clean
