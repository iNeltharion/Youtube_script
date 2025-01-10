import yt_dlp
import subprocess
import os


def ensure_directory_exists(directory):
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_audio(url, output_dir='temp'):
    """Загружает аудио из YouTube-видео."""
    ydl_opts = {
        'format': 'bestaudio/best',  # Загружаем лучший доступный аудиофайл
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Загружаем в указанную папку
        'extractaudio': True,  # Только аудио, без видео
        'noplaylist': True,  # Не загружать плейлисты
        'quiet': False,  # Показать вывод
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Загружаем видео
        print("Загрузка завершена")

        # Возвращаем путь к загруженному файлу
        downloaded_file = ydl.prepare_filename(ydl.extract_info(url, download=False))
        return os.path.join(output_dir, os.path.basename(downloaded_file))  # Возвращаем корректный путь

    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None


def convert_audio(input_file, output_file):
    """Конвертирует аудиофайл в формат MP3."""
    try:
        # Запускаем команду ffmpeg для конвертации
        subprocess.run(['ffmpeg', '-i', input_file, output_file], check=True)
        print(f"Конвертация прошла успешно: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка конвертации: {e}")


def main():
    # Убедимся, что папки для хранения файлов существуют
    ensure_directory_exists('sound')
    ensure_directory_exists('temp')

    # Ссылка на YouTube видео
    video_url = input("Введите ссылку на YouTube видео: ")

    # Скачиваем аудио
    downloaded_file = download_audio(video_url)

    if downloaded_file:
        # Генерация выходного пути для MP3 файла
        output_file = os.path.join('sound', os.path.splitext(os.path.basename(downloaded_file))[0] + '.mp3')

        # Конвертируем аудио в MP3
        convert_audio(downloaded_file, output_file)

        # Удаляем исходный файл после конвертации
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
            print(f"Удаление временного файла: {downloaded_file}")


if __name__ == "__main__":
    main()
