import requests
import json

def main():
    # Ввод данных...
    cat_text = input('Подпись к картинке с котом: ')
    token = input('Введите токен для Яндекса: ')
    group_name = 'pyqa-124'

    # 1. Получение картинки с CATAAS
    print(f"Запрашиваю картинку с текстом '{cat_text}'...")
    try:
        cat_response = requests.get(f'https://cataas.com/cat/says/{cat_text}', timeout=10)
        cat_response.raise_for_status()
        image_data = cat_response.content
        file_size = len(image_data)  # Размер получаем из содержимого в памяти!
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке картинки: {e}")
        return

    # 2. Работа с Яндекс.Диском
    headers = {'Authorization': f'OAuth {token}'}
    yandex_base_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    # 2.1. Создание/проверка папки
    folder_path = {'path': f'/{group_name}'}
    try:
        check_resp = requests.get(f"{yandex_base_url}", headers=headers, params=folder_path)
        if check_resp.status_code == 404:
            print(f"Создаю папку '{group_name}' на Диске...")
            create_resp = requests.put(f"{yandex_base_url}", headers=headers, params=folder_path)
            create_resp.raise_for_status()
        else:
            print(f"Папка '{group_name}' уже существует.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при работе с папкой на Диске: {e}")
        return

    # 2.2. Получение ссылки для загрузки
    file_name_on_disk = f"{cat_text}.jpg"
    upload_path = {'path': f'/{group_name}/{file_name_on_disk}'}
    try:
        print("Получаю ссылку для загрузки...")
        link_resp = requests.get(f"{yandex_base_url}/upload", headers=headers, params=upload_path)
        link_resp.raise_for_status()
        upload_url = link_resp.json()['href']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении ссылки для загрузки: {e}")
        return

    # 2.3. Загрузка файла на Диск (ПО ВОЗДУХУ!)
    try:
        print(f"Загружаю файл '{file_name_on_disk}' на Яндекс.Диск...")
        upload_resp = requests.put(upload_url, data=image_data)  # Отправляем данные напрямую
        upload_resp.raise_for_status()
        print("Загрузка успешно завершена!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке файла на Диск: {e}")
        return

    # 3. Формирование итогового JSON
    result_data = {
        "file_name": file_name_on_disk,
        "size": file_size,
        "saved_to": f"disk:/{group_name}/{file_name_on_disk}"
    }
    result_file_name = f"result_{cat_text}.json"
    with open(result_file_name, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)
    print(f"Информация о файле сохранена в '{result_file_name}'.")

if __name__ == "__main__":
    main()
