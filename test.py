import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
  #  driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')
 #  driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.maximize_window()
    yield driver
    driver.quit()


"""Явное ожидание"""


def test_show_my_pets(driver):
    wait = WebDriverWait(driver, 20)
    wait.until(expected_conditions.presence_of_element_located((By.ID, 'email')))
    driver.find_element(By.ID, 'email').send_keys('ascorbd@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('01102005')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text != ' PetFriends'

    # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
    images = driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
    names = driver.find_elements(By.XPATH, '//h5[@class="card-title"]')
    descriptions = driver.find_elements(By.XPATH, '//p[@class="card-text"]')

    # Проверяем, что на странице есть фотографии питомцев, имена, порода (вид) и возраст питомцев не пустые строки:
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
    assert wait.until(expected_conditions.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
    driver.find_element(By.CSS_SELECTOR, 'a[href="/all_pets"]').click()
    assert wait.until(expected_conditions.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "All"))

    # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
    css_locator = 'tbody>tr'
    data_my_pets = driver.find_elements(By.CSS_SELECTOR, css_locator)

    # Ожидаем, что данные всех питомцев, найденных локатором css_locator = 'tbody>tr', видны на странице:
    for i in range(len(data_my_pets)):
        assert wait.until(expected_conditions.visibility_of(data_my_pets[i]))

    # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
    image_my_pets = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(expected_conditions.visibility_of(image_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице:
    name_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(expected_conditions.visibility_of(name_my_pets[i]))

    # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице:
    type_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(expected_conditions.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице:
    age_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(expected_conditions.visibility_of(age_my_pets[i]))

    # Ищем на странице /my_pets всю статистику пользователя,
    # и вычленяем из полученных данных количество питомцев пользователя:
    all_statistics = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

    # Проверяем, что количество строк в таблице с моими питомцами равно общему количеству питомцев,
    # указанному в статистике пользователя:
    assert len(data_my_pets) == all_my_pets

    # Проверяем, что хотя бы у половины питомцев есть фото:
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
        assert m >= all_my_pets / 2

    # Проверяем, что у всех питомцев есть имя:
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть порода:
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть возраст:
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверяем, что у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
        set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
        assert len(list_name_my_pets) == len(
            set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
        set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
        assert len(list_data_my_pets) == len(
            set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть
