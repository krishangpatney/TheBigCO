import numpy as np

# convert string to grid
def create_grid(string):
    grid = '\n'.join([string[i:i+9] for i in range(0, len(string), 9)])
    grid = np.array([[int(i) for i in line] for line in grid.split()])
    return grid

# Return True if it is valid else False
def validator(grid):
    for i in range(9):
        j, k = (i // 3) * 3, (i % 3) * 3
        # checks each row and col, and 3x3 grids 
        if sum(grid[i,:]) != 45 or sum(grid[:,i]) != 45 or sum(grid[j:j+3, k:k+3].ravel()) != 45:
            return False
    return True

if __name__ == "__main__":
    # get input 
    string = input('enter string input : ')
    print(validator(create_grid(string)))