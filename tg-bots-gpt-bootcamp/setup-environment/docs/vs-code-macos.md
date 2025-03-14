
## 1. Установка Python

1. Открой **Терминал** (`Cmd + Пробел` → **Terminal**).
2. Проверь, установлен ли Python:

```sh
python3 --version
```

1. Если Python **не установлен** или версия ниже 3.12, установи его:
    
    - Через Homebrew:
        
        ```sh
        brew install python
        ```
        
    - Или скачай Python с [официального сайта](https://www.python.org/downloads/mac-osx/) и установи его вручную.
4. Проверь успешную установку:
    

```sh
python3 --version
```

Если видишь `Python 3.12.x` – всё ок! 🎉

---

## 2. Установка Git и клонирование репозитория

1. Проверь, установлен ли Git:

```sh
git --version
```

1. Если Git **не установлен**, установи его:
    
    - Через Homebrew:
        
        ```sh
        brew install git
        ```
        
    - Или скачай с [официального сайта](https://git-scm.com/downloads).
3. Перейди в нужную директорию:
    

```sh
cd your_dir
```

4. Склонируй репозиторий:

```sh
git clone https://github.com/MikD1/tg-bots-gpt-bootcamp.git
```

5. Перейди в папку с проектом:

```sh
cd cu-butcamp-2025
```

---

## 3. Установка VS Code

1. Скачай VS Code с [официального сайта](https://code.visualstudio.com/Download).
2. Установи его, переместив в папку **Applications**.
3. Открой VS Code и установи расширение "Python":
    - Перейди в **Extensions** (Cmd+Shift+X).
    - Найди **Python** от Microsoft.
    - Нажми "Install".


![extensions](static/extansions.png)



---

## 4. Создание виртуального окружения

1. Открой VS Code и выбери папку проекта (**File** → **Open Folder...** → выбери `cu-butcamp-2025`).
2. Открой **Терминал** (**Terminal** → **New Terminal** или `Ctrl+``).
3. Создай виртуальное окружение:

```sh
python3 -m venv venv
```

1. Активируй его:

```sh
source venv/bin/activate
```

1. Убедись, что в начале строки появился `(venv)`.


![venv_vscode](static/venv_vscode.png)


---

## 5. Установка зависимостей из `requirements.txt`

Если ты правильно склонировал репозиторий, то у тебя есть файл `requirements.txt`, установи все нужные пакеты командой:

```sh
pip3 install -r requirements.txt
```

---

## 6. Запуск `IamReadyToBootcamp.py`

Запусти свой скрипт одной из команд:

```sh
python IamReadyToBootcamp.py
```

или

```sh
python3 IamReadyToBootcamp.py
```

или через VS Code:

- Открыть `IamReadyToBootcamp.py`.
- Нажать `F5` или `Run` → `Run Without Debugging`.

![run_vscode](static/run_vscode.png)


Если программа **НЕ** вывела

`[status: OK] УРА! Все работает!`

иди к следующему пункту.

---

## 7. Ошибки

|Ошибка|Как решить|
|---|---|
|версия Python должна быть минимум 3.12|Установи нужную версию с [сайта](https://www.python.org/downloads/release/python-3120/)|
|Пропущенные библиотеки: <название>|Команда`pip3 install <название>` или`pip3 install -r requirements.txt`|
|Библиотеки с ошибкой в версии: <название>|Команда`pip3 install <название>==<версия>`|

Если у тебя другая ошибка, обратись в чат!
