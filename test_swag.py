from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from datetime import date
import pytest



class Test_Sauce:
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)

    def teardown_method(self):
        self.driver.quit()
    
    def waitForElementVisible(self,locator,timeout=10):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))

    def test_login(self):
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()
        self.waitForElementVisible((By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3'))
        
        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/test-empty-login.png")
        assert errorMessage.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username", ["Meryem", "standard_user", "problem_user"])
    def test_empty_password_login(self, username):
        self.waitForElementVisible((By.ID, 'user-name'))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        usernameInput.send_keys(username)
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()
        
        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/test-empty-password-{username}-login.png")
        assert errorMessage.text == "Epic sadface: Password is required"

    @pytest.mark.parametrize("username, password", [("Halil", "123"), ("Sema", "567"),("Sumeyra", "158")])
    def test_invalid_login(self,username,password):
        self.waitForElementVisible((By.ID, "user-name"))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, "password")
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, username)
        actions.send_keys_to_element(passwordInput, password)
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()
        
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-{username}-{password}-login.png")
        assert "Epic sadface: Username and password do not match any user in this service" == self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text
    def test_icon_login(self):
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()

        errorBtn = self.driver.find_element(By.CLASS_NAME, 'error-button')
        errorBtn.click()

        errorIcon = len(self.driver.find_elements(By.CLASS_NAME, 'error_icon'))
        self.driver.save_screenshot(f"{self.folderPath}/test-icon-login.png")

        assert errorIcon == 0

    def test_valid_login(self):
        self.waitForElementVisible((By.ID, "user-name"))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, "password")
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, "standard_user")
        actions.send_keys_to_element(passwordInput, "secret_sauce")
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        
        self.driver.save_screenshot(f"{self.folderPath}/test-succes-login.png")
        assert 6 == len(self.driver.find_elements(By.CLASS_NAME, "inventory_item"))


    def test_add_remove(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.waitForElementVisible((By.XPATH,"/html/body/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/a/div"))
        bikeLightAdd = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-bike-light")
        bikeLightAdd.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add1-remove.png")
        
        bikeLightRemove = self.driver.find_element(By.ID,"remove-sauce-labs-bike-light")
        bikeLightRemove.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add-remove2.png")
        addtoCart = self.driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/button")

        assert addtoCart.text == "Add to cart"

    def test_basket_lightPrice(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.waitForElementVisible((By.XPATH,"//*[@id='header_container']/div[2]/span"))
        bikeLightAdd = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-bike-light")
        bikeLightAdd.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-basket-bikelightprice1.png")

        shoppingBasket = self.driver.find_element(By.CLASS_NAME,"shopping_cart_link")
        shoppingBasket.click()

        bikeLightPrice_basket = self.driver.find_element(By.CLASS_NAME,"inventory_item_price")
        self.driver.save_screenshot(f"{self.folderPath}/test-basket-bikelightprice2.png")

        assert str("$9.99") == bikeLightPrice_basket.text

    

   

