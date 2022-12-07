class Directory:
    def __init__(self,name,parent) -> None:
        self.name = name
        self.parent = parent
        self.path = parent.path + self.name + '/' if self.parent else '/'
        self.children = {}
        self.files = {}
        self.size = 0
    
    def addChild(self,child):
        if child.name not in self.children:
            self.children[child.name] = child

    def addFile(self,file):
        if file.name not in self.files:
            self.files[file.name] = file
            curr = self
            while curr is not None:
                curr.size += file.size
                curr = curr.parent

class File:
    def __init__(self,name,parent,size) -> None:
        self.name = name
        self.parent = parent
        self.path = parent.path + self.name
        self.size = size

def get_ls_items(input_lines,curr_idx):
    ls_items = []
    curr_idx += 1
    curr_line = input_lines[curr_idx].strip().split() if curr_idx < len(input_lines) else ['$']
    while curr_line[0] != '$':
        ls_items.append(curr_line)
        curr_idx += 1
        curr_line = input_lines[curr_idx].strip().split() if curr_idx < len(input_lines) else ['$']
    return ls_items

def build_filesystem(input_lines):
    root_dir = Directory('/',None)
    curr_dir = root_dir
    curr_idx = 0
    while curr_idx < len(input_lines):
        curr_line = input_lines[curr_idx].strip().split()
        cmd = curr_line[1]
        if cmd == 'cd':
            if curr_line[2] == '/':
                curr_dir = root_dir
            elif curr_line[2] == '..':
                curr_dir = curr_dir.parent
            else:
                curr_dir = curr_dir.children[curr_line[2]]
            curr_idx += 1
        elif cmd == 'ls':
            ls_items = get_ls_items(input_lines,curr_idx)
            for item in ls_items:
                if item[0] == 'dir':
                    new_dir = Directory(item[1],curr_dir)
                    curr_dir.addChild(new_dir)
                else:
                    new_file = File(item[1],curr_dir,int(item[0]))
                    curr_dir.addFile(new_file)
            curr_idx += 1 + len(ls_items)
    return root_dir

def get_sizes(dir):
    if not dir.children:
        return [dir.size]
    size_list = [dir.size]
    for child in dir.children.values():
        size_list.extend(get_sizes(child))
    return size_list

with open('input.txt','r') as input:
    input_lines = input.readlines()

filesystem = build_filesystem(input_lines)
file_sizes = get_sizes(filesystem) + [filesystem.size]

# Star 1
print(sum([file_size for file_size in file_sizes if file_size <= 100000]))

