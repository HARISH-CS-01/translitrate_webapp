import torch
from Model import model_class 
import re

class inferencemodel():
        def __init__(self):
            self.tamil_set={'-PAD-': 0, 'ஂ': 1, 'ஃ': 2, 'அ': 3, 'ஆ': 4, 'இ': 5, 'ஈ': 6, 'உ': 7, 'ஊ': 8, 'எ': 9, 'ஏ': 10, 'ஐ': 11, 'ஒ': 12, 'ஓ': 13, 'ஔ': 14, 'க': 15, 'ங': 16, 'ச': 17, 'ஜ': 18, 'ஞ': 19, 'ட': 20, 'ண': 21, 'த': 22, 'ந': 23, 'ன': 24, 'ப': 25, 'ம': 26, 'ய': 27, 'ர': 28, 'ற': 29, 'ல': 30, 'ள': 31, 'ழ': 32, 'வ': 33, 'ஷ': 34, 'ஸ': 35, 'ஹ': 36, 'ா': 37, 'ி': 38, 'ீ': 39, 'ு': 40, 'ூ': 41, 'ெ': 42, 'ே': 43, 'ை': 44, 'ொ': 45, 'ோ': 46, 'ௌ': 47, '்': 48, 'ௗ': 49}
            self.english_set={'-PAD-': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}
            self.model=model_class()
            model_path=torch.load("best_model_95.pt")
            self.model.load_state_dict(model_path)
            
        def clean_english(self,line):
            non_english=re.compile('[^a-zA-Z ]')
            line = line.replace('-', ' ').replace(',', ' ').upper()
            line = non_english.sub('', line)
            return line.split()

        def get_ohe_english(self,word):
            #english_set={'-PAD-': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}
            rep=torch.zeros(len(word)+1,1,len(self.english_set),dtype=torch.float32)
            for letter_index,letter in enumerate(word):
                pos=self.english_set[letter]
                rep[letter_index][0][pos]=1
            rep[letter_index+1][0][0]=1
            return rep

        def generate(self,text: str):
            words_list=self.clean_english(text)
            self.model.eval()
            predicted_words=[]
            for i in range(len(words_list)):
                result_string=''
                english_rep=self.get_ohe_english(words_list[i])
                output=self.model.forward_pass(english_rep)
                for i in range(len(output)):
                    index=torch.argmax(output[i]).item()
                    if index==self.tamil_set['-PAD-']:
                        break
                    for key,value in self.tamil_set.items():
                        if value==index:
                            result_string+=key
                predicted_words.append(result_string)
            return predicted_words