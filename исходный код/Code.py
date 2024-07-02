import os
import platform
import subprocess
import re
import shutil
import webbrowser
from tqdm import tqdm
import tabulate
import glob




# Определить путь к папке программы
program_folder = os.path.dirname(os.path.abspath(__file__))


# # Пути Для разработки
# # Проверить наличие FFmpeg и yt-dlp в папке программы . Переменная в которой хранится путь до нужных файлов
ffmpeg_path = os.path.join(program_folder, 'ffmpeg.exe')
yt_dlp_path = os.path.join(program_folder, 'yt-dlp.exe')



# Цвет текста
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Глобальный список загрузок
download_list = []

# Определить функцию для добавления ссылки в список загрузок
def add_link(url):
    download_list.append(url)
    print(f"Ссылка добавлена: {url}")

# Определить функцию для создания папки для сохраненных файлов
def create_saves_directory():
    saves_directory = "saves"
    if not os.path.exists(saves_directory):
        os.makedirs(saves_directory)


# Загрузка в формате MP3
# def download_mp3(url):
#     try:
#         create_saves_directory()
#         print("В процессе, подождите...")

#         download_command = [yt_dlp_path, '-o', 'saves/%(title)s.%(ext)s', '--extract-audio', '--audio-format', 'mp3', url]
#         process = subprocess.Popen(download_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
#         process.wait()

#         downloaded_file = os.path.basename(url).replace('.+(?:v|e)=', '').replace('\\?.*', '')

#         print("\n----------------------------------------")
#         print("               Загружено                ")
#         print("----------------------------------------")
#         print(f"Файл сохранен как: saves/{downloaded_file}.mp3")

#         input("\nНажмите Enter для продолжения...")
#         os.system('clear' if platform.system() == 'Darwin' or platform.system() == 'Linux' else 'cls')

#     except subprocess.CalledProcessError as e:
#         print(f"Ошибка при выполнении команды: {e}")

# Загрузка видео в формате MP4
# def download_video(url):
#     try:
#         create_saves_directory()
#         print("В процессе, подождите...")

#         download_command = ['yt-dlp', '-o', 'saves/%(title)s.%(ext)s', url]
#         process = subprocess.Popen(download_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         process.wait()

#         downloaded_file = os.path.basename(url).replace('.+(?:v|e)=', '').replace('\\?.*', '')

#         print("\n----------------------------------------")
#         print("               Загружено                ")
#         print("----------------------------------------")
#         print(f"Файл сохранен как: saves/{downloaded_file}.mp4")

#         input("\nНажмите Enter для продолжения...")
#         os.system('clear' if os.name == 'posix' else 'cls')

#     except subprocess.CalledProcessError as e:
#         print(f"Ошибка при выполнении команды: {e}")

# Загрузка видео m3u8
# def download_m3u8():
#     url = input("Введите ссылку на видео формата m3u8: ")
#     saves_directory = "saves"
#     if not os.path.exists(saves_directory):
#         os.makedirs(saves_directory)
    
#     print(f"{Color.YELLOW}Скачивание в процессе...{Color.END}")
    
#     # Используем FFmpeg для скачивания и конвертации видео, скрывая вывод процесса
#     subprocess.call(['ffmpeg', '-i', url, os.path.join(saves_directory, 'video.mp4')], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
#     downloaded_file = 'video.mp4'
    
#     print(f"\n{Color.GREEN}----------------------------------------{Color.END}")
#     print(f"{Color.GREEN}               Загружено                {Color.END}")
#     print(f"{Color.GREEN}----------------------------------------{Color.END}")
#     print(f"{Color.GREEN}Файл сохранен как: saves/{downloaded_file}{Color.END}")
    
#     input("Нажмите Enter для продолжения...")
#     os.system('clear' if platform.system() == 'Darwin' or platform.system() == 'Linux' else 'cls')







# Сжатие и конвертация файлов
def compress_videos():
    print("\nВсе видеофайлы '.mkv','.webm','.m4v','.ts' при сжатии будут сконвертированы в '.mp4' или '.webm'!!!")
    print("\n- Все папки будут скопированы (будет добавлен суффикс _compressed)")
    print("\n- Все файлы которые не являются видеофайлами будут просто скопированы")
    print("\n P.S для сохранения файлов выбери любую папку кроме исходной")
    print("=====================================================================================================================")

    parent_folder_path = input("Шаг: 1(4) Введите путь до общей папки, где хранятся видеофайлами (без кавычек): ")
    output_folder_path = input("Шаг: 2(4) Введите папку для сохранения всех файлов (без кавычек): ")
    output_format = input("Шаг: 3(4) Выберите желаемый формат выходного файла (.mp4 или .webm): ")
    crf = input("Шаг: 4(4) Насколько сильно нужно сжать файлы: от 18 до 28. Где 18 - качество идентично оригиналу, а 28 - хуже качество, но размер меньше. В случае формата webm советую ставить около 20: ")

    total_size_before = 0
    total_size_after = 0
    compressed_video_count = 0

    folder_counter = 1

    for folder_name in os.listdir(parent_folder_path):
        folder_path = os.path.join(parent_folder_path, folder_name)
        if os.path.isdir(folder_path):
            output_folder = os.path.join(output_folder_path, f"{folder_name}_compressed")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            else:
                print(f"{Color.PURPLE}Папка {output_folder} уже существует.{Color.END}")

            file_counter = 1

            print(f"{Color.YELLOW}{folder_counter}) Папка в процессе: {folder_name}{Color.END}")

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    total_size_before += os.path.getsize(file_path)

                    output_file = os.path.join(output_folder, file_name)
                    if not os.path.exists(output_file) or parent_folder_path != output_folder_path:
                        print(f"{Color.YELLOW}{folder_counter}.{file_counter}) В процессе: {file_name}{Color.END}")

                        if file_name.endswith(('.mp4', '.webm', '.ts', '.m4v', '.mkv')):
                            compressed_file_name = f"{os.path.splitext(file_name)[0]}_compressed.{output_format}"
                            output_file = os.path.join(output_folder, compressed_file_name)

                            if os.path.exists(output_file):
                                print(f"{Color.PURPLE}{file_name} уже сжат.{Color.END}")
                            else:
                                if output_format == ".mp4":
                                    ffmpeg_command = ['ffmpeg', '-i', file_path, '-c:v', 'libx264', '-crf', crf, '-c:a', 'copy', output_file]
                                else:
                                    ffmpeg_command = ['ffmpeg', '-i', file_path, '-c:v', 'libvpx', '-crf', crf, output_file]

                                subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                                total_size_after += os.path.getsize(output_file)
                                compressed_video_count += 1

                                print(f"{Color.GREEN}Готово: {compressed_file_name}{Color.END}")
                        else:
                            output_file = os.path.join(output_folder, file_name)

                            if os.path.exists(output_file):
                                print(f"{Color.PURPLE}{file_name} уже скопирован.{Color.END}")
                            else:
                                shutil.copy(file_path, output_folder)
                                print(f"{Color.GREEN}Файл был скопирован: {file_name}{Color.END}")

                        file_counter += 1

            print(f"{Color.GREEN}Все файлы в папке {folder_name} сжаты и готовы.{Color.END}")
            folder_counter += 1

    # Сжатие файлов которые не в папках
    for file_name in os.listdir(parent_folder_path):
        file_path = os.path.join(parent_folder_path, file_name)
        if os.path.isfile(file_path):
            total_size_before += os.path.getsize(file_path)

            output_file = os.path.join(output_folder_path, file_name)
            if not os.path.exists(output_file) or parent_folder_path != output_folder_path:
                print(f"{Color.YELLOW}{folder_counter}) В процессе: {file_name}{Color.END}")

                if file_name.endswith(('.mp4', '.webm', '.ts', '.m4v', '.mkv')):
                    compressed_file_name = f"{os.path.splitext(file_name)[0]}_compressed.{output_format}"
                    output_file = os.path.join(output_folder_path, compressed_file_name)

                    if os.path.exists(output_file):
                        print(f"{Color.PURPLE}{file_name} уже сжат.{Color.END}")
                    else:
                        if output_format == ".mp4":
                            ffmpeg_command = ['ffmpeg', '-i', file_path, '-c:v', 'libx264', '-crf', crf, '-c:a', 'copy', output_file]
                        else:
                            ffmpeg_command = ['ffmpeg', '-i', file_path, '-c:v', 'libvpx', '-crf', crf, output_file]

                        subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                        total_size_after += os.path.getsize(output_file)
                        compressed_video_count += 1

                        print(f"{Color.GREEN}Готово: {compressed_file_name}{Color.END}")
                else:
                    output_file = os.path.join(output_folder_path, file_name)

                    if os.path.exists(output_file):
                        print(f"{Color.PURPLE}{file_name} уже скопирован.{Color.END}")
                    else:
                        shutil.copy(file_path, output_folder_path)
                        print(f"{Color.GREEN}Файл был скопирован: {file_name}{Color.END}")

            folder_counter += 1

    print("\n")
    print(f"{Color.GREEN}Все сжато! Статистика:{Color.END}")
    print(f"Количество видеофайлов: {compressed_video_count}")
    print(f"Размер всех видеофайлов до сжатия: {total_size_before / (1024 * 1024 * 1024):.2f} GB")
    print(f"Размер всех видеофайлов после сжатия: {total_size_after / (1024 * 1024 * 1024):.2f} GB")
    print("\n")
    input("\nНажмите Enter для продолжения...")





# Сжатие картинок в webp
def convert_to_webp(parent_dir, quality):
    total_files = 0
    compressed_files = 0
    total_size = 0
    compressed_size = 0

    for root, dirs, files in os.walk(parent_dir):
        print(f"Обрабатываю папку: {root}")
        for file in tqdm(files, desc="Обработано файлов", unit="файл", total=len(files)):
            if file.endswith(('.jpeg', '.jpg', '.avif', '.png', '.webp', '.tiff')):
                file_path = os.path.join(root, file)
                compressed_file = os.path.splitext(file_path)[0] + "_compressed.webp"
                command = ['ffmpeg', '-i', file_path, '-q:v', str(quality), compressed_file]
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                # Calculate sizes
                total_files += 1
                compressed_files += 1
                total_size += os.path.getsize(file_path)
                compressed_size += os.path.getsize(compressed_file)

    # Calculate sizes in MB
    total_size_mb = total_size / (1024 ** 2)
    compressed_size_mb = compressed_size / (1024 ** 2)

    print(f"Общее количество файлов: {total_files}")
    print(f"Количество сконвертированных и сжатых файлов: {compressed_files}")
    print(f"Общий размер исходных файлов: {total_size_mb:.2f} MB")
    print(f"Общий размер сжатых файлов: {compressed_size_mb:.2f} MB")

    delete_original = input(f"{Color.YELLOW}Хотите ли вы удалить исходные изображения? (y/n): {Color.END}")
    if delete_original.lower() == 'y':
        for root, dirs, files in os.walk(parent_dir):
            for file in files:
                if file.endswith(('.jpeg', '.jpg', '.avif', '.png', '.webp', '.tiff')) and not file.endswith('_compressed.webp'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

    print("\n")
    input("\nНажмите Enter для продолжения...")






# Главное меню
def main_menu():
    while True:
        os.system('clear' if platform.system() == 'Darwin' or platform.system() == 'Linux' else 'cls')
        print("Версия программы 0.4")
        print("Автор: https://github.com/spbkit1337")
        print("\n")
        # print("1) Загрузить в формате MP3")
        # print("2) Загрузить видео в формате MP4")
        print("1) Сконвертировать и сжать видео")
        # print("4) Скачать m3u8")
        print("2) Сконвертировать и сжать изображения")
        print("3) Поддерживаемые источники (?)")
        print("4) Выход")

        choice = input("Введите ваш выбор (1/2/3/4/5/6/7): ")

        # if choice == '1':
        #     url = input("Введите ссылку на видео чтобы скачать аудио: ")
        #     add_link(url)
        #     download_mp3(url)
        # elif choice == '2':
        #     url = input("Введите ссылку на видео: ")
        #     add_link(url)
        #     download_video(url)
        if choice == '1':
            compress_videos()
        # elif choice == '4':
        #     download_m3u8()
        elif choice == '2':
            print("\n")
            print("Все файлы: '.jpeg', '.jpg', '.avif', '.png', '.webp', '.tiff' будут сконвертированы и сжаты в webp и сохранены рядом с исходными файлами (будет добавлен суффикс _compressed). Также будет предложено после сжатия удалить исходные фотки")
            print("\nДругие файлы кроме фоток затронуты не будут.")
            parent_dir = input("Шаг: 1(2)Введи путь до общей папки: ")
            quality = int(input("Шаг: 2(2)Степень сжатия от 1 до 100 (рекомендую ставить 60-75): "))
            convert_to_webp(parent_dir, quality)            
        elif choice == '3':
            webbrowser.open("https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md")
        elif choice == '4':
            exit()
        else:
            print("Неверный выбор, попробуйте снова.")



if __name__ == "__main__":
    main_menu()
