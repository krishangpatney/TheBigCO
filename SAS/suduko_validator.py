import numpy as np

# convert string to grid
def validator(string):
    if len(string) != (9*9) and all(i.isdigit() for i in string) != True:
        return False
    grid = '\n'.join([string[i:i+9] for i in range(0, len(string), 9)])
    grid = np.array([[int(i) for i in line] for line in grid.split()])
    
    for i in range(9):
        j, k = (i // 3) * 3, (i % 3) * 3

        if sorted(grid[i,:]) == list(range(1, 9)) or sorted(grid[:,i]) == list(range(1, 9)) or sorted(grid[j:j+3, k:k+3].ravel()) == list(range(1, 9)):
            return False
    return True

if __name__ == "__main__":
    # get input 
    # Test String
    print("Test String : 859612437723854169164379528986147352375268914241593786432981675617425893598736241")
    print(validator('859612437723854169164379528986147352375268914241593786432981675617425893598736241'))
    string = input('enter string input : ')
    print(validator(string))