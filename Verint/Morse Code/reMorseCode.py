import numpy as np
import matplotlib.pyplot as plt
import wave
import struct
import math
import sys
class Morse:
    freq = 240 #C4 middle C
    T = 1/freq
    sample = 44100
    samples_in_T = int(sample*T)

    encKey = {
        'a':'.-', 'b':'-...','c':'-.-.','d':'-..',
        'e':'.', 'f':'..-.' ,'g':'--.','h':'....',
        'i':'..','j':'.---','k':'-.-','l':'.-..',
        'm':'--' ,'n':'-.' ,'o':'---','p':'.--.',
        'q':'--.-','r':'.-.','s':'...','t':'-',
        'u':'..-', 'v':'...-', 'w':'.--','x':'-..-',
        'y':'-.--','z':'--..',
        '1':'.----', '2':'..---','3':'...--','4':'....-',
        '5':'.....','6':'-....','7':'--...','8':'---..',
        '9':'----.','0':'-----',' ':'       '
    }

    decKey = {
        '.-':'a', '-...':'b','-.-.':'c','-..':'d',
        '.':'e', '..-.':'f' ,'--.':'g','....':'h',
        '..':'i','.---':'j','-.-':'k','.-..':'l',
        '--':'m' ,'-.':'n' ,'---':'o','.--.':'p',
        '--.-':'q','.-.':'r','...':'s','-':'t',
        '..-':'u', '...-':'v', '.--':'w','-..-':'x',
        '-.--':'y','--..':'z',
        '.----':'1', '..---':'2','...--':'3','....-':'4',
        '.....':'5','-....':'6','--...':'7','8':'---..',
        '----.':'9','-----':'0','':' '  
    }

    def __init__(self, unencoded=""):
        self.unencoded = unencoded
        self.encoded = ""
        return

    # write morse code to file
    def toFile(self,input,file="morse.txt"):
        with open(file, 'w') as f:
            f.write(input)
        return

    # setter method to update morse
    def setText(self,text):
        self.unencoded = text

    # encode array into morse code as text
    def encode_text(self):
        morseArr=  []
        
        for char in self.unencoded:
            if char!=" ":
                morseArr.append(Morse.encKey.get(char)+"   ")
            else:
                morseArr.append(Morse.encKey.get(char))
        self.encoded = ''.join(morseArr)
        self.toFile(self.encoded)
        return ''.join(self.encoded)

    # decode morse code text
    def decode_text(self, morse):
        morse = morse.split(Morse.encKey[' '])
        for word in range(len(morse)):
            
            morse[word] = morse[word].split('   ')
            
            for i in range(len(morse[word])):
                morse[word][i] = Morse.decKey.get(morse[word][i],'')
            morse[word] = ''.join(morse[word])

        morse = ''.join(morse)
        
        #remove trailing space
        return morse[:-1]

    def generate_audio(self):

        # specify morse code time dutations        
        DOT = int((Morse.sample*0.5)/Morse.samples_in_T)
        DASH = int((Morse.sample*1)/Morse.samples_in_T)

        # 3 space characters in a row
        SPACE = int((Morse.sample*0.75)/Morse.samples_in_T)

        # build a fourier series to sample wave
        x = np.arange(DOT*Morse.samples_in_T)
        y = np.empty(Morse.samples_in_T)
        for i in range(Morse.samples_in_T):
            y1 = 0
            #more samples = more accurate wave
            # tradeoff between quality and exe time
            for j in range(0,20,4):
                y1+=4/(math.pi*((2+j)/2))*math.sin((2+j)*math.pi*i/Morse.samples_in_T)
            y[i]=y1

        # create arrays that represent each sound type
        dot    = np.tile(y,DOT)
        dash   = np.tile(y,DASH)
        space  = np.zeros(SPACE) 
        inter  = np.zeros(DOT) 
       
        # plt.plot(x,y)
        # plt.show()
        sound_arr = np.empty((1))

        for char in self.encoded:
            print(char, end="")
            if(char == '.'):
                sound_arr = np.hstack((sound_arr,dot))
                sound_arr = np.hstack((sound_arr,inter))
            elif(char=='-'):
                sound_arr = np.hstack((sound_arr,dash))
                sound_arr = np.hstack((sound_arr,inter))
            elif(char == ' '):
                sound_arr = np.hstack((sound_arr,space))

        self.save_audio(sound_arr)

    def save_audio(self,track):
        fout = wave.open("morse.wav","w")
        fout.setnchannels(1) # Mono
        fout.setsampwidth(2) # Sample is 2 Bytes
        fout.setframerate(Morse.sample)
        fout.setcomptype('NONE','Not Compressed')
        BinStr = bytearray()
        for i in range(track.size):
            BinStr.extend(struct.pack('h', int(round(track[i]*10000))))#.decode(sys.stdout.encoding)
        fout.writeframesraw(BinStr)
        fout.close()

# demo example
txt = "hello"
runner = Morse(txt)

# returns morse code
# file called morse.txt has also
# been created
morse_txt = runner.encode_text()

# Output text is the same as the input text
print(runner.decode_text(morse_txt) == txt) 
runner.generate_audio()