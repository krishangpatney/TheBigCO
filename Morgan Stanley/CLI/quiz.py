import requests
import json
import os
import time

def get_questions(number):
    x = json.loads(requests.get(f'https://opentdb.com/api.php?amount={number}').text)
    return x.get('results')

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def filter(s):
    # too lazy to filter sanitized data properly, enjoy this awfulness
    x = s.replace('&quot;','"')
    x = x.replace('&#039;','\'')
    x = x.replace('&amp;','&')
    return x

class Question:
    def __init__(self, j_obj):
        self.category=j_obj.get('category')
        self.type=j_obj.get('type')
        self.difficulty=j_obj.get('difficulty')
        self.question=filter(j_obj.get('question'))
        self.answer=j_obj.get('correct_answer')
        self.options=self._get_options(j_obj.get('incorrect_answers'))
    def _get_options(self,opts):
        opts = opts[:] # clone list
        opts.append(self.answer)
        opts.sort(reverse=True)
        return opts

def print_question(q):
    print(f'Category: {q.category}\n\n{"="*(len(q.question)+4)}\n= {q.question} =\n{"="*(len(q.question)+4)}\n')
    for i,opt in enumerate(q.options):
        print(f'[{i+1}]\t{filter(opt)}')
    print()

def check_answer(num,q):
    if num>0 and num<=len(q.options):
        choice = q.options[num-1]
        if choice == q.answer:
            return True
    return False

def game(rounds=10):
    score=0
    questions = get_questions(rounds)
    for x in questions:
        q = Question(x)
        clear()
        print_question(q)
        choice = input('\nChoice: ')
        correct = check_answer(int(choice),q)
        if correct:
            score+=1
            print('CORRECT!')
            time.sleep(2)
        else:
            print(f'WRONG! Correct answer is {filter(q.answer)}\n\n')
            input('Press enter to continue...')
    clear()
    print(f'You scored {score}/{rounds}')

if __name__=='__main__':
    c = input('Enter the number of rounds: ')
    game(int(c))
