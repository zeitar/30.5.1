import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_pets(driver):
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('awgamerstone@gmail.com')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('petfriends123')

   # Настраиваем неявные ожидания:
   driver.implicitly_wait(5)

   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   # Нажимаем "Мои питомцы"
   driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
   # Проверка страницы пользователя
   assert driver.find_element(By.CSS_SELECTOR, 'html > body > div > div > div > h2').text == "zeitar"

   # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   # Проверяем, что на странице есть фотографии питомцев, имена, порода (вид) и возраст питомцев не пустые строки:
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0


def test_show_my_pets(driver):
   # Вводим email, пароль, открываем главную страницу сайта
   driver.find_element(By.ID, 'email').send_keys('awgamerstone@gmail.com')
   driver.find_element(By.ID, 'pass').send_keys('petfriends123')
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   #Настраиваем переменную явного ожидания:
   wait = WebDriverWait(driver, 5)

   # Проверяем, что мы оказались на главной странице сайта.
   # Ожидаем в течение 5с, что на странице есть тег h1 с текстом "PetFriends"
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME,'h1'), "PetFriends"))

   # Открываем страницу /my_pets.
   driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

   # Проверяем, что мы оказались на  странице пользователя.
   # Ожидаем в течение 5с, что на странице есть тег h2 с именем пользователя
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "zeitar"))

   # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
   data_my_pets = driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')

   # Ожидаем, что данные всех питомцев, видны на странице:
   for i in range(len(data_my_pets)):
      assert wait.until(EC.visibility_of(data_my_pets[i]))

   # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
   image_my_pets = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         assert wait.until(EC.visibility_of(image_my_pets[i]))

   # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице:
   name_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
   for i in range(len(name_my_pets)):
      assert wait.until(EC.visibility_of(name_my_pets[i]))

   # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице:
   type_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
   for i in range(len(type_my_pets)):
      assert wait.until(EC.visibility_of(type_my_pets[i]))

   # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице:
   age_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
   for i in range(len(age_my_pets)):
       assert wait.until(EC.visibility_of(age_my_pets[i]))


   all_my_pets = 2

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