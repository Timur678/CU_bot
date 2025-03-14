
## 1. Установка Python

1. Открой [официальный сайт Python](https://www.python.org/downloads/).
2. Скачай версию 3.12 для macOS.
3. Запусти скачанный `.pkg`-файл и следуй инструкциям установки.
4. После завершения установки открой **Терминал** и проверь версию Python:

```sh
python3 --version
```

Если видишь `Python 3.12.x` – всё ок! 🎉

---

## 2. Установка Git и клонирование репозитория

1. Открой **Терминал** и введи команду:

```sh
git --version
```

2. Если Git **не установлен**, скачай его с [официального сайта](https://git-scm.com/downloads) или установи через Homebrew:

```sh
brew install git
```

3. Перейди в нужную директорию:

```sh
cd your_dir
```

4. Склонируй репозиторий:

```sh
git clone https://github.com/MikD1/tg-bots-gpt-bootcamp.git
```

5. Перейди в папку проекта:

```sh
cd cu-butcamp-2025
```


---

## 3. Установка PyCharm

1. Скачай PyCharm с [официального сайта](https://www.jetbrains.com/pycharm/download/).
2. Установи и запусти PyCharm.
3. Открой в PyCharm папку с клонированным репозиторием.

---

## 4. Добавление интерпретатора в PyCharm

1. Открой PyCharm и выбери проект.
2. Перейди в **PyCharm** → **Settings** → **Project: cu-butcamp-2025** → **Python Interpreter**.
3. Нажми **Add Interpreter** → **Add Local Interpreter**.

![settings](static/settings.png)


5. Выбери **venv** и укажи путь до установленного Python (обычно определяется автоматически).

![settings](static/create_venv.png)


6. Нажми **OK** и дождись завершения настройки. 

---

## 5. Запуск виртуального окружения

1. Открой **Терминал** в PyCharm или используй встроенный терминал macOS.
2. Активируй виртуальное окружение:

```sh
source venv/bin/activate
```

3. Убедись, что в начале строки появился `(venv)`.

![venv](static/venv.png)

---

## 6. Установка зависимостей из `requirements.txt`

Если ты правильно склонировал репозиторий, то у тебя есть файл `requirements.txt`, установи все нужные пакеты командой:

```sh
pip3 install -r requirements.txt
```

---

## 7. Запуск `IamReadyToBootcamp.py`

Запусти свой скрипт одной из команд:

```sh
python IamReadyToBootcamp.py
```

или

```sh
python3 IamReadyToBootcamp.py
```

или через PyCharm (**ПКМ по файлу `IamReadyToBootcamp.py` → Run `IamReadyToBootcamp.py`**)


![run](static/run.png)


Если программа **НЕ** вывела

`[status: OK] УРА! Все работает!`

Переходи к следующему пункту

---

## 8. Ошибки

|Ошибка|Как решить|
|---|---|
|версия Python должна быть минимум 3.12|Установи нужную версию с [сайта](https://www.python.org/downloads/release/python-3120/)|
|Пропущенные библиотеки: <название>|Команда`pip3 install <название>` или`pip3 install -r requirements.txt`|
|Библиотеки с ошибкой в версии: <название>|Команда`pip3 install <название>==<версия>`|

Если у тебя другая ошибка, обратись в чат!
