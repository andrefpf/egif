# ======================================
# CONFIG
# ======================================

PROJECT_NAME = egif

FLAGS = -c -I include/

C_FILES = $(wildcard ./src/*.c)
H_FILES = $(wildcard ./include/*.h)
O_FILES = $(subst .c,.o,$(subst src,objects,$(C_FILES)))

# ======================================
# COMPILATION
# ======================================

all: obj_folder $(PROJECT_NAME) clean

$(PROJECT_NAME): $(O_FILES) ./objects/main.o
	gcc -o program $^

./objects/%.o: ./src/%.c ./include/%.h
	gcc -o $@ $< $(FLAGS)

./objects/main.o: main.c $(H_FILES)
	gcc -o $@ $< $(FLAGS)

obj_folder:
	@mkdir -p objects

clean:
	@rm -rf ./objects/*.o*	
	@rmdir objects
