from .config import *
import sys
import os
import json
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException


class TLCScrap(object):
    def __init__(self, url=SCRAP_URL):
        """
        DESC :

        IN   :
        OUT  :
        """
        self.url = url
        self.certifId = ""
        self.account = ACCOUNT_NAME
        self.password = ACCOUNT_PASSWORD
        options = Options()
        # options.add_argument("--blink-settings=imagesEnabled=false")
        # options.add_argument('headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.allQuestions = {}
        self.tryQuestions = {}
        self.completeJsonPath = ""
        self.tryJsonPath = ""

    def connectAndLaunchTest(self):
        """
        DESC : connect to the TLC with account in config.py
               and launch test in argument

        IN   :
        OUT  :
        """
        try:
            self.certifId = sys.argv[1]
        except IndexError:
            inputId = CERTIF_TEST_ID
            if not(inputId):
                inputId = input("Merci de preciser l'ID de la certif bande de chlags :\n")
            self.certifId = inputId
        self.driver.get(self.url)
        self.driver.find_element(By.NAME, "ta_username").send_keys(self.account)
        self.driver.find_element(By.NAME, "ta_password").send_keys(self.password)
        self.driver.find_element(By.NAME, "login").click()
        self.driver.find_element(By.NAME, "test_list").click()
        table = self.driver.find_elements(
            By.XPATH, '//*[@id="content"]/form/table/tbody/tr'
        )
        breakFlag = False
        for tr in table:
            datas = tr.find_elements(By.TAG_NAME, "td")
            if breakFlag:
                break
            for td in datas:
                if self.certifId in td.text:
                    datas[datas.index(td) - 1].click()
                    breakFlag = True
                    break
        if breakFlag:
            self.driver.find_element(By.NAME, "next").click()
            Alert(self.driver).accept()
            self.driver.find_element(By.NAME, "yes").click()
            self.driver.find_element(By.NAME, "ok").click()
            self.driver.find_element(By.NAME, "ok").click()
            return
        else:
            print("Aucune Certif avec cette ID")
            exit()

    def checkForExistingJson(self):
        """
        DESC : Goes to check Jsons and load them into variables

        IN   :
        OUT  :
        """
        currentCwd = os.getcwd()
        self.completeJsonPath = os.path.join(currentCwd, "CompleteJsons", self.certifId)
        tryJsonPath = os.path.join(currentCwd, "JsonTry")
        # Lire ou crée le fichier json global
        try:
            completeJsonFile = open(self.completeJsonPath, "r")
            self.allQuestions = json.loads(completeJsonFile.read())
        except FileNotFoundError:
            completeJsonFile = open(self.completeJsonPath, "w")
        # check if existant pour incrémenter et créer fichier de l'essai en cours
        tryFileList = os.listdir(tryJsonPath)
        currentCertifTrys = []
        for tryFile in tryFileList:
            if self.certifId in tryFile:
                currentCertifTrys.append(int(tryFile.split(self.certifId + "_", 1)[1]))
        if not currentCertifTrys:
            fileName = self.certifId + "_1"
            self.tryJsonPath = os.path.join(tryJsonPath, fileName)
            open(self.tryJsonPath , "w")
        else:
            fileName = self.certifId + "_" + str(max(currentCertifTrys) + 1)
            self.tryJsonPath  = os.path.join(tryJsonPath, fileName)
            open(self.tryJsonPath , "w")
        return

    def completeTest(self):
        """
        DESC : Rempli le test et attends sur la page de summary

        IN   :
        OUT  :
        """
        tempScrapCertif = {"Questions": []}
        # Loop avec click sur Next : condition de sortie : arrivée sur summary
        while True:
            try:
                if (
                    self.certifId
                    in self.driver.find_element(
                        By.XPATH, '//*[@id="pagetitle"]/h3'
                    ).text
                ):
                    break
            except NoSuchElementException:
                self.treatQuestion(tempScrapCertif)
                self.driver.find_element(
                    By.XPATH, '//*[@id="questionnav"]/input[2]'
                ).click()
        self.dictToHtml(tempScrapCertif)
        return

    def treatQuestion(self, tempScrapCertif):
        # Iteration pour une question
        currentQuestion = ''
        currentQuestionDivEles = self.driver.find_elements(
            By.XPATH, '//*[@id="questiontext"]/h3/p'
        )
        for currentQuestionDiv in currentQuestionDivEles:
            currentQuestion = currentQuestion + '\n' + currentQuestionDiv.text if currentQuestion else currentQuestionDiv.text
        responseGroup = self.driver.find_elements(
            By.XPATH, '//*[@id="answers"]/tbody/tr'
        )
        currentAnswers = []
        for item in responseGroup:
            currentAnswers.append(item.text)
        currentAnswers.pop(0)
        for ele in currentAnswers:
            currentAnswers[currentAnswers.index(ele)] = ele.split("\n", 1)[1]
        # CurrentQuestion et currentAnswer sont les variabels a utiliser
        # Balise HTML pour gras ! <strong></strong>
        indexResponse = False
        if self.allQuestions:
            for question in self.allQuestions["Questions"]:
                if currentQuestion == question["question"]:
                    try :
                        # checker les réponses et valider celle qui correspond
                        indexResponse = currentAnswers.index(question["correctResponse"])
                        self.driver.find_element(
                            By.XPATH,
                            '//*[@id="answers"]/tbody/tr['
                            + str(indexResponse + 2)
                            + "]/td[2]/input",
                        ).click()
                        origine = "102%"
                        break
                    except KeyError:
                        pass
                    try :
                        # checker les réponses et valider celle qui correspond + Flag la question
                        indexResponse = currentAnswers.index(question["response"])
                        self.driver.find_element(
                            By.XPATH,
                            '//*[@id="answers"]/tbody/tr['
                            + str(indexResponse + 2)
                            + "]/td[2]/input",
                        ).click()
                        self.driver.find_element(
                            By.XPATH, '//*[@id="questionnav"]/input[6]'
                        ).click()
                        origine = "51%"
                        break
                    except KeyError :
                        pass
            if indexResponse :
                currentAnswers[indexResponse] = (
                    "<strong>" + currentAnswers[indexResponse] + "</strong> - " + origine
                )
        tempScrapCertif["Questions"].append(
            {"question": currentQuestion, "answers": currentAnswers}
        )
        return tempScrapCertif

    def dictToHtml(self, tempScrapCertif):
        """
        DESC : Changes Dict to HTML and saves it

        IN   :
        OUT  :
        """
        currentCwd = os.getcwd()
        completeHTMLPath = os.path.join(currentCwd, "tempHTML", "PrendsTonTemps.html")
        if os.path.exists(completeHTMLPath):
            os.remove(completeHTMLPath)
        # crée le fichier html
        completeHTMLFile = open(completeHTMLPath, "w")
        # Puis f.write(str) --> f.close()
        tempHTML = ""
        iterator = 1
        for bloc in tempScrapCertif["Questions"]:
            tempHTML = tempHTML + (
                "<br><h3>" + str(iterator) + ". " + bloc["question"] + "</h3><br><ul>"
            )
            for answer in bloc["answers"]:
                tempHTML = tempHTML + ("<li>" + answer + "</li>")
            tempHTML = tempHTML + ("</ul>")
            iterator += 1
        completeHTMLFile.write(tempHTML)
        completeHTMLFile.close()
        return

    def returnToFirstQuestion(self):
        """
        DESC : Test pour savoir si on est sur une question ou sur le sommaire et retour a la premiere question

        IN   :
        OUT  :
        """
        while True:
            try:
                if ("Question" in self.driver.find_element(By.XPATH, '//*[@id="statusblock"]').text):
                    self.driver.find_element(By.XPATH, '//*[@id="questionnav"]/input[4]').click()
                    break
            except NoSuchElementException:
                break
        self.driver.find_element(By.XPATH, '//*[@id="content"]/form/table/tbody/tr[2]/td[6]/input').click()
        self.driver.find_element(By.XPATH, '//*[@id="topnav"]/p/input').click()
        return

    def finalScrapping(self):
        """
        DESC : On repasse sur toutes les questions et on crée les JSON clean et complets

        IN   :
        OUT  :
        """
        self.tryQuestions = {"Questions": [],
                              "Recap" : [] ,
                              "Results" : {}}
        # Loop avec click sur Next : condition de sortie : arrivée sur summary
        while True:
            try:
               if (
                    self.certifId
                    in self.driver.find_element(
                        By.XPATH, '//*[@id="pagetitle"]/h3'
                    ).text
                ):
                    #Valider et récup les résultats
                    recapQuestions = self.driver.find_elements(
                    By.XPATH, '//*[@id="content"]/form/table/tbody/tr'
                            )
                    recapQuestions.pop(0)
                    recapQuestionsText = []
                    for item in recapQuestions:
                        recapQuestionsText.append(item.text.split("\n", 1)[1])
                    self.tryQuestions["Recap"] = recapQuestionsText
                    break
            except NoSuchElementException:
                # Iteration pour une question
                currentQuestion = ''
                currentQuestionDivEles = self.driver.find_element(
                    By.XPATH, '//*[@id="questiontext"]/h3/p'
                )
                for currentQuestionDiv in currentQuestionDivEles : 
                    currentQuestion = currentQuestion + '\n' + currentQuestionDiv.text if currentQuestion else currentQuestionDiv.text
                responseGroup = self.driver.find_elements(
                    By.XPATH, '//*[@id="answers"]/tbody/tr'
                )
                responseGroup.pop(0)
                numberOfAnswers = len(responseGroup) + 1
                currentAnswers = []
                # On récupère toutes les questions dans une liste
                for item in responseGroup:
                    currentAnswers.append(item.text.split("\n", 1)[1])
                # On itere sur les questions qui existent deja en cherchant la notre
                questionTrouveeFlag = False
                # ce qu'on fait si on la trouve dans le maxi JSON
                posQuestionCheckee = False
                if self.allQuestions:
                    for question in self.allQuestions["Questions"]:
                        if currentQuestion == question["question"]:
                            questionTrouveeFlag = True
                            # on récupere la position de la réponse checkée dans currentAnswers
                            for i in range(2, numberOfAnswers + 1):
                                inputAnswer = self.driver.find_element(By.XPATH, '//*[@id="answers"]/tbody/tr[' + str(i) + ']/td[2]/input')
                                if inputAnswer.is_selected():
                                    posQuestionCheckee = i - 2
                            # checker si ca correspond a la réponse cochée
                            # si oui on fait rien, sinon on la remplace dans correctResponse
                            try:
                                if currentAnswers[posQuestionCheckee] == question["correctResponse"] :
                                    break
                            except KeyError :
                                question["correctResponse"] = currentAnswers[posQuestionCheckee]
                                question["response"] = currentAnswers[posQuestionCheckee]
                                break
                            # checker si la reponse est la même et modifier si non
                            try:
                                if currentAnswers[posQuestionCheckee] == question["response"] :
                                    break
                            except KeyError :
                                question["response"] = currentAnswers[posQuestionCheckee]
                                break
                if self.allQuestions == {} :
                    self.allQuestions = {"Questions" : []}
                if not posQuestionCheckee :
                    for i in range(2, numberOfAnswers + 1):
                        inputAnswer = self.driver.find_element(By.XPATH, '//*[@id="answers"]/tbody/tr[' + str(i) + ']/td[2]/input')
                        if inputAnswer.is_selected():
                            posQuestionCheckee = i - 2
                # Ce qu'on fait si on la trouve pas dans le maxi JSON
                if not questionTrouveeFlag :
                    # Ajouter la question au maxi JSON
                    self.allQuestions["Questions"].append({"question": currentQuestion, "answers": currentAnswers})
                    # on ajoute la réponse qui a été checkée
                    self.allQuestions["Questions"][len(self.allQuestions["Questions"]) - 1]["response"] = currentAnswers[posQuestionCheckee]
                    # On ajoute la date
                    self.allQuestions["Questions"][len(self.allQuestions["Questions"]) - 1]["dateAjout"] = str(date.today())
                # On ajoute la question a l'essai en cours
                self.tryQuestions["Questions"].append(
                    {"question": currentQuestion, "answers": currentAnswers}
                )
                # On ajoute la réponse checkée a l'essai en cours
                if posQuestionCheckee:
                    self.tryQuestions["Questions"][len(self.tryQuestions["Questions"]) - 1]["response"] = currentAnswers[posQuestionCheckee]
                # Passer a la question suivante
                self.driver.find_element(
                    By.XPATH, '//*[@id="questionnav"]/input[2]'
                ).click()
        # Finir test et prendre les résultats
        self.driver.find_element(By.XPATH, '//*[@id="topnav"]/input').click()
        try:
            Alert(self.driver).accept()
        except NoAlertPresentException:
            pass
        # Ajout du score dans le try et des categs
        self.tryQuestions["Results"]["score"] = self.driver.find_element(By.XPATH, '//*[@id="topnav"]/div[4]/h4').text
        allCategs = self.driver.find_elements(By.XPATH, '//*[@id="content"]/form/table/tbody/tr')
        allCategs.pop(0)
        allCategsText = []
        for row in allCategs:
            allCategsText.append(row.text)
        self.tryQuestions["Results"]["Categories"] = allCategsText
        # On met a jour les deux JSON
        completeJsonFile = open(self.completeJsonPath, "w")
        completeJsonFile.write(json.dumps(self.allQuestions))
        completeJsonFile.close()
        tryJsonFile = open(self.tryJsonPath , "w")
        tryJsonFile.write(json.dumps(self.tryQuestions))
        tryJsonFile.close()
        return