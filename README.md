Скрипт на pyhton для сжатия и конвертирования видео и фото. 

📚Библеотеки : <a href = "https://ffmpeg.org/">ffmpeg</a>

<h3>Что делает программа</h3>

У скрипта две функции. Первая сжимает и конвертирует видео файлы в формат webm или mp4 (это на выбор , но я советую webm для более сильного сжатия). Вторая функция сжимает и конвертирует изображения в формат webp.
Скрипт работает по принципу так: вы указываете общий путь где лажет все файлы и указываете насколько сильно сжать , затем запускаете скрипт. Скрипт обходит каждый файл и каждую папку с другими файлами. Сжатия можно добиться примерно в 3-5 раз (можно больше или меньше это зависит от того на сколько сильно хотите сжать)


Изначально я делал всё на powershell но я подумал что неплохо бы что программа которая у меня работает могла запуститься и на других ОС ведь python универсален. Поэтому в последствии весь код я перевёл на python🐍

Если закинуть программу на virus total то он будет ругаться. Видимо потому что у программы нет цифровой подписи.

Если нет доверея то :  можно взять в папке "Исходный код" сам код программы и скомпилировать через "auto-py-to-exe" (<a href = "https://pypi.org/project/auto-py-to-exe/">Ссылка</a>). Либо через pyinstaller.


<h3>Возможные проблемы</h3>

1. При запуске на linux (я тестировал на debian) может выдать ошибку что нехватает python библеотек в системе.

Их можно доустановить двумя командами:

```
sudo apt install python3-tabulate
```

```
sudo apt install python3-tqdm
```
2. Хоть и скрипт проходит каждую папку он может не тронуть вложеные папки с файлами которые лежат внутри друих папок. То есть глубина сканирование не глубокая.

3. Что при сжатии и конвериации видеофайлов так и фотографий возможно проблемы:
- При работе с фотками может зависнуть. В целом эту проблему можно решить нажав просто "Enter" и работа продолжится. Также может вылететь если <ins>очень много фотографий</ins> нужно обработать.
- При работе с видео работа может зависнуть или выдать ошибку. У меня такое было только когда файл был битым.  


Скриншоты программы🦉

![tWuOHslVGZ](https://github.com/spbkit1337/python-converter/assets/51737588/d258a59e-4801-47d9-b337-45dd757fcae3)



