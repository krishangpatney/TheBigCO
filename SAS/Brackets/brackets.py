test = "((brackets) (in this (one)) are correct ())"
fail = "((brackets in this) one are ) in correct ())"
brackets_sad = "(brackets)(\{lol\})this should([fail]])"
brackets_happy = "(brackets)(\{lol\})this should([succeed{}])"

def brackets(s,open,close):
    bracket_count = 0
    for c in s:
        if bracket_count<0: return False
        if c==open:
            bracket_count+=1
        elif c==close:
            bracket_count-=1
    return True if bracket_count==0 else False

def check(s,delims=[('(',')'),('[',']'),('{','}')]):
    return all([brackets(s,*b) for b in delims])

# TESTING

print(check(test)) # Succeed
print(check(fail)) # Fail
print(check(brackets_sad)) # Fail
print(check(brackets_happy)) # Succeed