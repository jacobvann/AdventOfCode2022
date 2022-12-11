# --- Day 7: No Space Left On Device ---
# You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear
# much louder sounds in the distance; how big do the animals get out here, anyway?
#
# The device the Elves gave you has problems with more than just its communication system. You try to run a system
# update:
#
# $ system-update --please --pretty-please-with-sugar-on-top
# Error: No space left on device
# Perhaps you can delete some files to make space for the update?
#
# You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input).
# For example:
#
# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k
# The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or
# files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of
# directories and listing the contents of the directory you're currently in.
#
# Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:
#
# cd means change directory. This changes which directory is the current directory, but the specific result depends on
# the argument:
# cd x moves in one level: it looks in the current directory for the directory named x and makes it the current
# directory.
# cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the
# current directory.
# cd / switches the current directory to the outermost directory, /.
# ls means list. It prints out all of the files and directories immediately contained by the current directory:
# 123 abc means that the current directory contains a file named abc with size 123.
# dir xyz means that the current directory contains a directory named xyz.
# Given the commands and output in the example above, you can determine that the filesystem looks visually like this:
#
# - / (dir)
#   - a (dir)
#     - e (dir)
#       - i (file, size=584)
#     - f (file, size=29116)
#     - g (file, size=2557)
#     - h.lst (file, size=62596)
#   - b.txt (file, size=14848514)
#   - c.dat (file, size=8504156)
#   - d (dir)
#     - j (file, size=4060174)
#     - d.log (file, size=8033020)
#     - d.ext (file, size=5626152)
#     - k (file, size=7214296)
# Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a).
# These directories also contain files of various sizes.
#
# Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
# To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the
# sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic
# size.)
#
# The total sizes of the directories above can be found as follows:
#
# The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
# The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596),
# plus file i indirectly (a contains e which contains i).
# Directory d has total size 24933642.
# As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
# To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total
# sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As
# in this example, this process can count files more than once!)
#
# Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those
# directories?


# need to implement some kind of tree ... do i make a class?
# "file" - contains a name and a size
# "directory" - contains an array of either files or directories


class FileSystem:
    def __init__(self, name, fs_type):
        self.name = name
        self.fs_type = fs_type
        self.size = 0
        self.children = []
        self.parent = self
        self.path = ''
        self.level = 1

    def add_file(self, file):
        if self.fs_type == 'FILE':
            return

        # check if it exists
        for child in self.children:
            if file.name == child.name:
                return

        file.parent = self
        file.path = self.path + '/' + file.name
        file.level = self.level + 1
        print("Adding file: {} at level {} parented to {}".format(file.name, file.level, self.name))
        self.children.append(file)

    def add_directory(self, directory):
        if self.fs_type == 'FILE':
            return

        # check if it exists
        for child in self.children:
            if directory.name == child.name:
                return

        directory.parent = self
        directory.path = directory.name
        directory.level = self.level + 1
        print("Adding directory: {} at level {} parented to {}".format(directory.name, directory.level, self.name))
        self.children.append(directory)

    def list(self, recursive=False):
        # print all kids
        for child in self.children:
            child.print()
            if recursive:
                child.list(recursive)


    def print(self):
        if self.fs_type == 'FILE':
            print("{} {}: {} (size = {})".format("|"+"-----"*(self.level-1), self.fs_type, self.name, self.size))
        else:
            print("{} {}: {}".format("|"+"-----"*(self.level-1), self.fs_type, self.path))

    def get_size(self):
        if self.fs_type == 'FILE':
            return self.size
        else:
            size = 0
            for child in self.children:
                size += child.get_size()
            return size

    # def find(self, name):
    #     for child in self.children:
    #         if child.name == name:
    #             return child
    #     new_dir = Directory(name)
    #     self.add_directory(new_dir)
    #     return new_dir




class Tree:
    def __init__(self, node_name, node_type, parent=False, size=0):
        self.children = []
        self.parent = parent
        self.name = node_name
        self.node_type = node_type
        self.size = size

    def add_file(self, name, size):
        if not self.get_child(name):
            new_tree = Tree(name, 'FILE', self, size)
            self.children.append(new_tree)
            return new_tree
        return self.get_child(name)

    def add_directory(self, name):
        if not self.get_child(name):
            new_tree = Tree(name, 'DIR', self)
            self.children.append(new_tree)
            return new_tree
        return self.get_child(name)

    def get_tree_size(self):
        sz = int(self.size)
        for child in self.children:
            sz += child.get_tree_size()
        return sz

    def get_parent(self):
        if not self.parent:
            return self
        else:
            return self.parent

    def get_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return child
        return False

    def get_full_path(self):
        if not self.parent:
            return "/"
        else:
            return self.parent.get_full_path() + "/" + self.name

    def list(self, level=0):
        if self.node_type == "DIR":
            #print("| {} {} {} [{}]".format("-"*level, self.node_type, self.name, self.get_tree_size()))
            # print("{}\t{}".format(self.name, self.get_tree_size()))
            if self.get_tree_size() >= 1518953:
               print("{} >>>>>> {}".format(self.name, self.get_tree_size()))
        # if self.node_type == "FILE":
            # print("| {} {} {} {}".format("-"*level, self.node_type, self.name, self.size))

        for child in self.children:
            child.list(level+1)

# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    root = Tree("root", "DIR")
    cwd = root

    # read through all the lines
    for i in range(len(lines)):
        line = lines[i].replace("\n", "")
        # print(line)
        # determine what the cmd is

        # change directory
        if line[:4:] == "$ cd":
            dir_name = line[5::]
            # go back a directory
            if dir_name == "..":
                cwd = cwd.get_parent()
            # create a new directory and enter it
            else:
                # print(" > ADDED DIRECTORY {} to {}".format(dir_name, cwd.name))
                cwd = cwd.add_directory(dir_name)
        # list ... we don't need to do anything here
        elif line[:4:] == "$ ls":
            continue
        # directory
        elif line[:4:] == "dir ":
            dir_name = line[4::]
            # add the directory if it doesn't exist
            cwd.add_directory(dir_name)
            # print(" > ADDED DIRECTORY {} to {}".format(dir_name, cwd.name))
        # files?
        elif len(line.split(" ")) == 2: # and int(line.split(" ")[0]) > 0:
            file_name = line.split(" ")[1]
            file_size = line.split(" ")[0]
            cwd.add_file(file_name, file_size)
            # print(" > ADDED FILE {}".format(file_name))

        # root.list(recursive=True)
        # print("\n---------\n\n")

    f.close()
    print("\n\n")

    root.list()
    print("total space = 70000000")
    print("free space = {}".format(70000000-root.get_tree_size()))
    print("required to install = 30000000")
    print("additional space needed = {}".format(30000000-28481047))
