"""
遍历markdown文件时排除某些文件夹

node_modules:   node
test:           test
build/debug:    C/C++
.:              .git/.imgs,... hidden files    
_:              __pycache__,... excluded files      
"""
EXCLUDE_DIRS_PATTERN = r"^(?!(node_modules|test|build|Debug|privacy|\.|_))+"

"""
遍历markdown文件时排除某些文件

privacy:        google chrome extension
"""
EXCLUDE_FILES_PATTERN = r"^(?!(privacy|CONTRIBUTING))+"
FILENAME = "index"
DEV = True