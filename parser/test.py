def check_array(arr):
    # Проверяем, что все элементы массива содержат цифры от 1 до 10
    is_valid = all(any(char.isdigit() and 1 <= int(char) <= 10 for char in item) for item in arr)

    # Если все условия выполняются, возвращаем True
    return is_valid

# Пример использования функции
my_array = ['Vilnius, 55 мин. назад', 'Vilnius, 1 мин. назад', 'Vilnius, 9 мин. назад']
result = check_array(my_array)

if result:
    print("Массив соответствует условиям.")
else:
    print("Массив не соответствует условиям.")
