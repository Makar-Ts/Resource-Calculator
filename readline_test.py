import readline

class SimpleCompleter():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Создание списка соответствий.
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        # Вернуть элемент состояния из списка совпадений, 
        # если их много. 
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

def inputing():
    line = ''
    while line != 'stop':
        line = input('!("stop" to quit) Ввод текста: => ')
        print (f'Отправка: {line}')

# Регистрация класса 'SimpleCompleter'
readline.set_completer(SimpleCompleter(['start', 'stop', 'list', 'print']).complete)

# Регистрация клавиши `tab` для автодополнения
readline.parse_and_bind('tab: complete')

# Запрос текста
inputing()