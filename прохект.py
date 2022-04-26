import random

file = open('wordle.txt', 'r', encoding='utf-8') 
words = []
for i in file.readlines():
    words.append(i.rstrip())
file.close()

availible = set('ёйцукенгшщзхъфывапролджэячсмитьбю')  # Множество доступных букв, которые есть в словах или же еще не проверялись игроком. Я пока не сделала проверку, принадлежит ли каждая буква вводимого слова этому множеству.
in_place = [['_' for i in range(5)] for j in range(3)]  # Список списков букв для каждого из 3 слов, для которых известно место в слове (если неизвестно, на месте буквы стоит _)
in_word = [set() for i in range(3)]  # Список множеств букв для каждого из 3 слов, для которых известно, что оно есть в слове.

if input('Начнем игру? ') in ["Да", 'да', 'ДА']:
    win = False
    sam = random.sample(words, 3)  # Список с загаданными словами
    sam_lett = set(''.join(sam))  # Множество всех букв, которые есть в загаданных словах
    sam_lett_list = [{} for i in range(3)]  # Список со словарем для каждого загаданного слова, где ключ - буква, а значение - количество раз, которое буква встретилась в слове
    for i in range(3):
        for j in range(5):
            if sam[i][j] in sam_lett_list[i]:
                sam_lett_list[i][sam[i][j]] += 1
            else:
                sam_lett_list[i][sam[i][j]] = 1
    guessed = set()  # Множество индексов отгаданных слов
    
    print('Мы загадали 3 пятибуквенных слова! У вас есть 10 попыток, чтобы отгадать все 3 слова. За каждый ход вы можете ввести лишь одно существующее пятибуквенное слово, а мы покажем, какие буквы вы угадали, для каждого из трех слов. Если буква есть в слове, но стоит не на своем месте, оно будет обозначена нижним регистром, если на своем месте, то верхним регистром. Если введенной буквы в слове нет, на месте этой буквы будет прочерк. Также после каждого вашего хода вам будут выводиться доступные буквы алфавита, а также для каждого из 3 слов списки угаданных букв, которые есть в слове и которые стоят на своих местах.')
    
    for i in range(10):
        print('ПОПЫТКА', i + 1)
        repeat = True  # Переменная, с помощью которой при необходимости повторяем ввод.
        att = input('Введите слово: ')
        while repeat:
            if len(att) != 5:
                att = input('Длина вашего слова не равна 5. Пожалуйста, введите пятибуквенное существительное: ')
            elif att not in words:
                att = input('Такого слова не существует. Пожалуйста, введите существующее пятибуквенное существительное: ')
            else:
                repeat = False
                
        out = [['_' for i in range(5)] for j in range(3)]
        for j in range(5):  # В этом цикле для каждой буквы проверяем, есть ли она хоть в одном из слов, и, если да, для каждого из 3 слов проверяем, есть ли она в этом слове и, если да, стоит ли на нужной позиции
            if att[j] in availible and att[j] not in sam_lett:
                availible.remove(att[j])
            elif att[j] in availible:
                for k in range(3):
                    if att[j] in sam_lett_list[k]:
                        if att[j] == sam[k][j]:
                            in_place[k][j] = att[j].upper()
                            in_word[k].add(att[j])
                        else:
                            in_word[k].add(att[j])
        for j in range(5):  # В этом цикле формируем вывод для каждого слова
            if att[j] in availible and att[j] in sam_lett:
                for k in range(3):
                    if att[j] in in_word[k]:
                        if att[j] == sam[k][j]:
                            out[k][j] = att[j].upper()
                        elif sam_lett_list[k][att[j]] == 1 and att[j] not in att[:j] and att[j].upper() not in in_place[k] or att.count(att[j]) >= in_place.count(att[j].upper()) and sam_lett_list[k][att[j]] >= att.count(att[j], 0, j + 1):
                            out[k][j] = att[j]
                            
                            
        for k in range(3):
            if k not in guessed:
                print(f"Cлово {k + 1}: {''.join(out[k])}")  # Выводим наши метаслова
                
        print('\n')
        print('Доступные буквы:', ' '.join(list(availible)))
        print('\n')
        
        for k in range(3):
            if k not in guessed:
                wrd = ' '.join(list(in_word[k]))  # Переменная для красивого вывода in_word
                if wrd == '':
                    print('В слове', k + 1, 'нет угаданных букв.')
                else:
                    print(f'Угаданные буквы в слове {k + 1}: {wrd}')
                plc = ''.join(list(in_place[k]))  # Переменная для красивого вывода in_place
                if plc == '':
                    print('В слове', k + 1, 'нет букв с угаданным местом.')
                else:
                    print(f'Угаданные места букв в слове {k + 1}: {plc}')
                print('\n')
        for k in range(3):  # Цикл, в котором проверяем, угадал ли человек хоть одно слово
            if ''.join(out[k]).lower() == sam[k]:
                guessed.add(k)
                if len(guessed) < 3:
                    print(f"Поздравляю, вы угадали {k + 1}-е слово! Вам осталось {3 - len(guessed)} {'слово' if 3 - len(guessed) == 1 else 'слова'}")
        if len(guessed) == 3:  # Проверка на победу
            win = True
            print('Ура, вы угадали все слова! С победой!')
            break
if not win:
    print('Вы проиграли....')
    for i in guessed:
        print(f'Вы угадали слово {i + 1}: {sam[i]}')
    print("Оставшиеся слова:")
    for i in range(3):
        if i not in guessed:
            print(f'Слово {i}: {sam[i]}')
            
