# Оценка модели синтеза речи

## 1. О проекте
В данном проекте я оценивал качество синтезируемой речи моделью parler-tts-mini-jenny-30H. Полный отчет по работе будет прикреплен к репозиторию.

## 2. Запуск заданий
### Задание 1: 
Пример общей работы с моделью
#### Запуск
Чтобы сгенерировать аудио из обучения, выполните следующий код:
```commandline
prompt = ("Hey, how are you doing today? My name is Jenny, "
          "and I'm here to help you with any questions you have.")
description = ("Jenny speaks at an average pace with an animated delivery "
               "in a very confined sounding environment with clear audio quality.")
file_name = "simple0.wav"
speech_generation(prompt, description, file_path=file_name)
```
Далее я эксперементировал с описанием, менял только два параметра:
```commandline
description = ("Jenny speaks at a fast pace with indifferent speech "
               "in a very confined sounding environment with clear audio quality.")
file_name = "simple0_1.wav"
```

```commandline
description = ("Jenny speaks at an average pace with an animated delivery "
               "in a very confined sounding environment with clear audio quality, the voice is low, "
               "with an emphasis on every second word .")
file_name = "simple0_2.wav"
```
### Задание 2: Оценка надежности синтеза
В этом задании я проверял коэффициент ошибок
#### Запуск
Код для синтеза аудио: 
```commandline
references = get_references()
generate_group(references)
```
Для получения коэффициента:
```commandline
print(word_error_rate(references))
```

### Задание 3: Подбор описания
В этой части я изменял описание, чтобы приблизить синтезированную речь к оригиналу
#### Запуск
```commandline
prompt = ("I, Jude Duarte, high Queen of Elf haman exile, "
    "spend most mornings dozing in front of daytime television")
description = ""
file_name = "parler1.wav"
speech_generation(prompt, description, file_path=file_name)
```

Далее я снова менял только два поля:
```commandline
description = "The speaker reads slowly, with pauses"
file_name = "parler2.wav"
```

```commandline
description = ("The speaker reads slowly, measuredly, "
               "pauses at commas, and emphasizes his position")
file_name = "parler3.wav"
```

```commandline
description = ("The speaker reads slowly, measuredly, "
               "pauses at commas, and emphasizes his position", 
               "In the second part put emphasis on the word:most,  and on the word: daytime")
file_name = "parler4.wav"
```
