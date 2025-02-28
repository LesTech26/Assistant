import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyaudio

# Включаем движок
engine = pyttsx3.init()

# Выбор голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Функция для произношения текста
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Слушает и прспознаёт речь
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)  # Шумоподавление
        audio = recognizer.listen(source)

    try:
        print("Распознавание...")
        command = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {command}")
    except sr.UnknownValueError:
        print("Извините, я не понял, что вы сказали.")
        command = ""
    except sr.RequestError as e:
        print(f"Не могу получить доступ к сервису распознавания речи: {e}")
        command = ""
    return command.lower()


def run_assistant():
    command = take_command()
    print(command)

    if not command:
        return  # Если команда пустая, выходим из функции

    if "привет" in command:
        talk("Привет, я Настя! Чем могу помочь?")
    elif "как дела" in command:
        talk("Всё отлично, спасибо! А у вас?")
    elif "время" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        talk(f"Сейчас {time}")
    elif "найди" in command:
        search = command.replace("найди", "").strip()
        if search:  # Проверяем, что поисковый запрос не пустой
            pywhatkit.search(search)
            talk(f"Ищу {search} в Google")
        else:
            talk("Пожалуйста, уточните, что искать.")
    elif "википедия" in command:
        search = command.replace("википедия", "").strip()
        if search:  # Проверяем, что запрос не пустой
            try:
                info = wikipedia.summary(search, sentences=2)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("Найдено несколько вариантов. Уточните запрос.")
            except wikipedia.exceptions.PageError:
                talk("Ничего не найдено.")
        else:
            talk("Пожалуйста, уточните, что искать в Википедии.")
    elif "пока" in command or "стоп" in command:
        talk("До свидания!")
        exit()
    else:
        talk("Пожалуйста, повторите команду.")

# Бесконечный цикл для работы ассистента
if __name__ == "__main__":
    while True:
        run_assistant()