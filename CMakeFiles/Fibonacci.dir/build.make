# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/martth/Desktop/git_project/gitlab/PyMieSim

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/martth/Desktop/git_project/gitlab/PyMieSim

# Include any dependencies generated for this target.
include CMakeFiles/Fibonacci.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/Fibonacci.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Fibonacci.dir/flags.make

CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o: CMakeFiles/Fibonacci.dir/flags.make
CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o: PyMieSim/FibonnaciMesh.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/martth/Desktop/git_project/gitlab/PyMieSim/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o -c /home/martth/Desktop/git_project/gitlab/PyMieSim/PyMieSim/FibonnaciMesh.cpp

CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/martth/Desktop/git_project/gitlab/PyMieSim/PyMieSim/FibonnaciMesh.cpp > CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.i

CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/martth/Desktop/git_project/gitlab/PyMieSim/PyMieSim/FibonnaciMesh.cpp -o CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.s

# Object files for target Fibonacci
Fibonacci_OBJECTS = \
"CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o"

# External object files for target Fibonacci
Fibonacci_EXTERNAL_OBJECTS =

PyMieSim/Fibonacci.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Fibonacci.dir/PyMieSim/FibonnaciMesh.cpp.o
PyMieSim/Fibonacci.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Fibonacci.dir/build.make
PyMieSim/Fibonacci.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Fibonacci.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/martth/Desktop/git_project/gitlab/PyMieSim/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module PyMieSim/Fibonacci.cpython-38-x86_64-linux-gnu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Fibonacci.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Fibonacci.dir/build: PyMieSim/Fibonacci.cpython-38-x86_64-linux-gnu.so

.PHONY : CMakeFiles/Fibonacci.dir/build

CMakeFiles/Fibonacci.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Fibonacci.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Fibonacci.dir/clean

CMakeFiles/Fibonacci.dir/depend:
	cd /home/martth/Desktop/git_project/gitlab/PyMieSim && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/martth/Desktop/git_project/gitlab/PyMieSim /home/martth/Desktop/git_project/gitlab/PyMieSim /home/martth/Desktop/git_project/gitlab/PyMieSim /home/martth/Desktop/git_project/gitlab/PyMieSim /home/martth/Desktop/git_project/gitlab/PyMieSim/CMakeFiles/Fibonacci.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/Fibonacci.dir/depend

