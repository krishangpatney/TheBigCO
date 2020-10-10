import numpy as np
import matplotlib.pyplot as plt
import wave
import struct
import math

from numpy.lib.function_base import append

class Morse:
    """
        Capital letters are converted to lowercase
        Takes input and generates 
            morse.txt file
            morse.wav file

            Turns encoded morse into text
            Not implemented- audio to text


    """

    freq = 480 #C4 middle C
    T = 1/freq
    sample = 44100
    samples_in_T = int(sample*T)

    # disgusting i know
    # its just a char map of askii to morse
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
    def toFile(self,input,file="morse"):
        with open(str(file)+".txt", 'w') as f:
            f.write(input)
        print("Morse Saved to "+file+".txt")
        return

    def fromFile(self, filepath="morse.txt"):
        with open(filepath) as file:
            #stored as single line. retrieve single line
            data =  file.readline()
        return self.decode_text(data)

    # setter method to update morse
    def setText(self,text):
        self.unencoded = text
        return text
    # encode array into morse code as text
    def encode_text(self, txt=""):
        print("Generating Morse...")
        morseArr=  []
        
        if (txt):
            self.setText(txt)

        for char in self.unencoded:
            
            #filter out non alpha chars
            if(Morse.encKey.get(char.lower(),False)):
                if char!=" ":
                    morseArr.append(Morse.encKey.get(char.lower())+"   ")
                else:
                    morseArr.append(Morse.encKey.get(char))
        self.encoded = ''.join(morseArr)
        self.toFile(self.encoded)
        return ''.join(self.encoded)

    # decode morse code text
    def decode_text(self, morse):
        print("...end=")
        morse = morse.split(Morse.encKey[' '])
        for word in range(len(morse)):
            
            morse[word] = morse[word].split('   ')
            
            for i in range(len(morse[word])):
                morse[word][i] = Morse.decKey.get(morse[word][i],'')
            morse[word] = ''.join(morse[word])

        morse = ''.join(morse)
        
        #remove trailing space
        return morse[:-1]

    def generate_audio(self, filename="morse"):
        print("Creating Audio File...")

        if filename == "":
            filename = "morse"
        
        # specify morse code time dutations        
        DOT = int((Morse.sample*0.5)/Morse.samples_in_T)
        DASH = int((Morse.sample*1)/Morse.samples_in_T)

        # 3 space characters in a row
        LETTER_SPACE = int(DOT * Morse.samples_in_T)
        WORD_SPACE =  LETTER_SPACE*3
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
        word_space  = np.zeros(WORD_SPACE) 
        letter_space  = np.zeros(LETTER_SPACE) 
        
        #init sound array
        sound_arr = np.empty((1))

        # map inputs to sounds
        for char in self.encoded:
            if(char == '.'):
                sound_arr = np.hstack((sound_arr,dot))
                sound_arr = np.hstack((sound_arr,letter_space))
            elif(char=='-'):
                sound_arr = np.hstack((sound_arr,dash))
                sound_arr = np.hstack((sound_arr,letter_space))
            elif(char == ' '):
                sound_arr = np.hstack((sound_arr,word_space))

        self.save_audio(sound_arr, filename)

    def save_audio(self,track, filename="morse"):
        print("Saving Audio file")

        #create eav file
        fout = wave.open(str(filename)+".wav","w")

        #setup params
        fout.setnchannels(1) # Mono
        fout.setsampwidth(2) # Sample is 2 Bytes
        fout.setframerate(Morse.sample)
        fout.setcomptype('NONE','Not Compressed')

        #encode data into raw bytes
        BinStr = bytearray()
        for i in range(track.size):
            BinStr.extend(struct.pack('h', int(round(track[i]*10000))))
        fout.writeframesraw(BinStr)
        fout.close()
        print("Saved: "+filename+".wav")



def show_commands():
    print(
        """
        help - displays this message
        morse <text to be converted to morse>
            e.g> morse hello world
        fromFile retrieve, decode and display more code from txt file
            e.g> fromFile morse.txt
        makeAudio [optional <filename (default=morse )>]
            generate morse morse code as wav audio file

            e.g> makeAudio morse
            e.g> makeAudio


        """
    )

runner = Morse()
commands = {
    "help":lambda x:show_commands(),
    "morse":lambda x:runner.encode_text(x),
    "fromFile":lambda f:print(runner.fromFile(f)),
    "makeAudio":lambda x:runner.generate_audio(x)
}

while(True):
    usrInput = input("\nEnter Command (help for info, q to quit):")
    if usrInput == "q":
        break
    try:
        inputs = usrInput.split(" ")
        if(len(inputs) == 1):
            inputs.append("")
        commands.get(inputs[0])(" ".join(inputs[1:]))
    except Exception as e:
        #print(e)
        show_commands()

print("Program Exited")
# # demo example
# morse hello world
# fromFile morse.txt
# makeAudio sound1
# makeAudio