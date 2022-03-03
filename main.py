import datetime
import sys, os
from PyQt5 import uic
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from datetime import date
import icons_rc


# מגישים: טל שקד 312208523 ויקטוריה חליוסטוב 320755481

# ============================================ Detect&Suggest ==============================================


# ====================if adding new icons, run this first===================================================
# os.system("C:/Users/talsh/AppData/Local/Programs/Python/Python37/Scripts/pyrcc5 icons.qrc -o icons_rc.py")


class MainProgram(qtw.QMainWindow):
    def __init__(self):
        super(MainProgram, self).__init__()
        if getattr(sys, "frozen", False):
            ui_path = os.path.dirname(sys.executable)
        elif __file__:
            ui_path = os.path.dirname(os.path.abspath(__file__))

        ui_path2 = ui_path + "/HomePage.ui"
        ui_path = ui_path + "/Detect&Suggest.ui"
        self.login_register_ui = uic.loadUi(ui_path)
        self.HomePageUI = uic.loadUi(ui_path2)

        self.login_register_ui.stackedWidget.setCurrentIndex(0)
        self.HomePageUI.stackedWidget.setCurrentIndex(0)

        # =====================connecting functions to buttons===============================
        # login buttons
        self.login_register_ui.btn_login.clicked.connect(self.Login)
        self.login_register_ui.btn_register.clicked.connect(self.RegisterPage)

        # register buttons
        self.login_register_ui.btn_cancel.clicked.connect(self.Cancel)
        self.login_register_ui.btn_register_3.clicked.connect(self.RegisterNewUser)

        # main menu buttons
        self.HomePageUI.btn_logout.clicked.connect(self.LogOut)
        self.HomePageUI.btn_newpatient.clicked.connect(self.OpenNewPatient)
        self.HomePageUI.btn_newpatient_back.clicked.connect(self.BackToMain)

        # history buttons
        self.HomePageUI.btn_patienthistory.clicked.connect(self.Open_History)
        self.HomePageUI.btn_back_to_main_history.clicked.connect(self.BackFromHistory)

        # new patient buttons
        self.HomePageUI.btn_newpatient_next.clicked.connect(self.Create_New_Patient)
        self.HomePageUI.btn_newpatient_back.clicked.connect(self.BackToMain)

        # add patient info buttons
        self.HomePageUI.btn_info_next.clicked.connect(self.Add_Patient_Info)
        self.HomePageUI.btn_info_back.clicked.connect(self.Back_To_Patient)

        # patient questions buttons
        self.HomePageUI.btn_suggest.clicked.connect(self.Suggest)
        self.HomePageUI.btn_suggest_back.clicked.connect(self.Back_To_Info)

        # suggestion buttons
        self.HomePageUI.btn_back_to_main.clicked.connect(self.BackToMain)

        # open patient history
        self.HomePageUI.btn_history_id.clicked.connect(self.OpenPatientHistory)
        # =====================showing first window of program===============================

        self.login_register_ui.show()

        # ===============================functionality===========================================

    def Back_To_Info(self):
        self.HomePageUI.stackedWidget.setCurrentIndex(2)

    #the function that gets all the info and then calculates and prints to screen the suggestions.
    def Suggest(self):

        is_fever = self.HomePageUI.buttonGroup_q1.checkedButton().text()
        is_preg = self.HomePageUI.buttonGroup_q2.checkedButton().text()
        is_dir = self.HomePageUI.buttonGroup_q3.checkedButton().text()
        is_vom = self.HomePageUI.buttonGroup_q4.checkedButton().text()
        is_smok = self.HomePageUI.buttonGroup_q5.checkedButton().text()

        anemia_counter, diet_counter, hemorrhage_counter, hyperlif_counter, blood_cells_counter, hematologic_counter \
            = 0, 0, 0, 0, 0, 0

        ironpos_counter, dehydration_counter, infection_counter, lackofvitamins_counter, viral_counter, bile_counter \
            = 0, 0, 0, 0, 0, 0

        heart_counter, blooddis_counter, liver_counter, kidney_counter, iron_counter, muscle_counter, smoke_counter, \
        lung_counter = 0, 0, 0, 0, 0, 0, 0, 0

        gland_counter, diabetes_counter, cancer_counter, overmeat_counter, diffmed_counter, malnourishment_counter \
            = 0, 0, 0, 0, 0, 0
        pregnant_counter = 0

        if is_smok == 'Yes':
            smoke_counter += 1

        try:
            file = open('Patients.txt', 'r')
        except FileNotFoundError:
            Popup_Message('Error', 'Patients file not found"', qtw.QMessageBox.Critical)
            return

        patient_age = int(file.readline())
        patient_origin = file.readline().rstrip()
        patient_id = file.readline().rstrip()
        patient_gender = file.readline().rstrip()
        file.close()
        try:
            f = open("p_measures.txt", 'r')
        except FileNotFoundError:
            Popup_Message('Error', 'patient measures file not found"', qtw.QMessageBox.Critical)
            return False

        wbc = float(f.readline())
        neut = float(f.readline())
        lymph = float(f.readline())
        rbc = float(f.readline())
        hct = float(f.readline())
        urea = float(f.readline())
        hb = float(f.readline())
        crea = float(f.readline())
        iron = float(f.readline())
        hdl = float(f.readline())
        alka = float(f.readline())
        f.close()

        # check white blood cells below
        if (patient_age >= 18 and wbc < 4500) or (4 <= patient_age <= 17 and wbc < 5500) \
                or (0 <= patient_age <= 3 and wbc < 6000):
            viral_counter += 1
            cancer_counter += 0.5
        # check white blood cells above
        if (patient_age >= 18 and wbc > 11000) or (4 <= patient_age <= 17 and wbc > 15500) \
                or (0 <= patient_age <= 3 and wbc > 17500):
            if is_fever == "Yes":
                viral_counter += 1
            cancer_counter += 0.5
            blooddis_counter += 0.5

        # check neutrophil below
        if neut < 28:
            blood_cells_counter += 1
            infection_counter += 1
            cancer_counter += 0.5
        # check neutrophil above
        if neut > 54:
            infection_counter += 1

        # check lymphocytes below
        if lymph < 36:
            blood_cells_counter += 1

        # check lymphocytes above
        if lymph > 52:
            infection_counter += 1
            cancer_counter += 1

        # check red blood cells below
        if rbc < 4.5:
            anemia_counter += 1
            hemorrhage_counter += 1

        # check red blood cells above
        if rbc > 6:
            if is_smok == "No":
                lung_counter += 1
                blood_cells_counter += 1
            if is_smok == "Yes":
                blood_cells_counter += 0.5

        # check hct male
        if patient_gender == "Male":
            if hct < 37:
                anemia_counter += 1
                hemorrhage_counter += 1
            if hct > 54 and is_smok == "No":
                dehydration_counter += 0.5

        # check hct female
        elif patient_gender == "Female":
            if hct < 33:
                anemia_counter += 1
                hemorrhage_counter += 1
            if hct > 47 and is_smok == "No":
                dehydration_counter += 0.5

        # check urea middle-east
        if patient_origin == "Middle Eastern (Oriental)":
            if urea < 18.3:
                if patient_gender == "Female" and is_preg == "No":
                    malnourishment_counter += 1
                    diet_counter += 1
                    liver_counter += 1
                if patient_gender == "Male":
                    malnourishment_counter += 1
                    diet_counter += 1
                    liver_counter += 1
            if urea > 47.3:
                kidney_counter += 1
                dehydration_counter += 1
                diet_counter += 1

        # check urea other origins
        elif patient_origin == "Other" or patient_origin == "Ethiopian":
            if urea < 17:
                if patient_gender == "Female" and is_preg == "No":
                    malnourishment_counter += 1
                    diet_counter += 1
                    liver_counter += 1
                if patient_gender == "Male":
                    malnourishment_counter += 1
                    diet_counter += 1
                    liver_counter += 1
            if urea > 43:
                kidney_counter += 1
                dehydration_counter += 1
                diet_counter += 1

        # check hemoglobin female
        if patient_age >= 18 and patient_gender == "Female":
            if hb < 12:
                anemia_counter += 1
                hematologic_counter += 0.5
                iron_counter += 0.5
                hemorrhage_counter += 0.5
            if hb > 16:
                dehydration_counter += 0.5

        # check hemoglobin male
        if patient_age >= 18 and patient_gender == "Male":
            if hb < 12:
                anemia_counter += 1
                hematologic_counter += 0.5
                iron_counter += 0.5
                hemorrhage_counter += 0.5
            if hb > 18:
                dehydration_counter += 0.5

        # check hemoglobin child
        if 0 <= patient_age <= 17:
            if hb < 11.5:
                anemia_counter += 1
                hematologic_counter += 0.5
                iron_counter += 0.5
                hemorrhage_counter += 0.5
            if hb > 15.5:
                dehydration_counter += 0.5

        # check creatinine baby
        if 0 <= patient_age <= 2:
            if crea < 0.2:
                muscle_counter += 1
                malnourishment_counter += 1
                diet_counter += 1
            if crea > 0.5:
                if is_dir == "No" and is_vom == "No":
                    kidney_counter += 1
                    overmeat_counter += 1
                    muscle_counter += 1

        # check creatinine teen
        if 3 <= patient_age <= 17:
            if crea < 0.5:
                muscle_counter += 1
                malnourishment_counter += 1
                diet_counter += 1
            if crea > 1:
                if is_dir == "No" and is_vom == "No":
                    kidney_counter += 1
                    overmeat_counter += 1
                    muscle_counter += 1

        # check creatinine adults
        if 18 <= patient_age <= 59:
            if crea < 0.6:
                muscle_counter += 1
                malnourishment_counter += 1
                diet_counter += 1
            if crea > 1:
                if is_dir == "No" and is_vom == "No":
                    kidney_counter += 1
                    overmeat_counter += 1
                    muscle_counter += 1

        # check creatinine elderly
        if patient_age >= 60:
            if crea < 0.6:
                muscle_counter += 1
                malnourishment_counter += 1
                diet_counter += 1
            if crea > 1.2:
                if is_dir == "No" and is_vom == "No":
                    kidney_counter += 1
                    overmeat_counter += 1
                    muscle_counter += 1

        # check iron male
        if patient_gender == "Male":
            if iron < 60:
                malnourishment_counter += 1
                hemorrhage_counter += 1
            if iron > 160:
                ironpos_counter += 1

        # check iron female
        if patient_gender == "Female":
            if iron < 48:
                if is_preg == "No":
                    malnourishment_counter += 1
                    hemorrhage_counter += 1
            if iron > 128:
                ironpos_counter += 1

        # check high density lipoprotein ethiopian
        if patient_origin == "Ethiopian":
            # check hdl female
            if patient_gender == "Female":
                if hdl < 40.8:
                    heart_counter += 1
                    hyperlif_counter += 1
                    diet_counter += 1

            # check hdl male
            elif patient_gender == "Male":
                if hdl < 34.8:
                    heart_counter += 1
                    hyperlif_counter += 1
                    diabetes_counter += 1

        # check hdl other origins
        if patient_origin == "Other" or patient_origin == "Middle Eastern (Oriental)":
            # check hdl female
            if patient_gender == "Female":
                if hdl < 34:
                    heart_counter += 1
                    hyperlif_counter += 1
                    diabetes_counter += 1

            # check hdl male
            if patient_gender == "Male":
                if hdl < 29:
                    heart_counter += 1
                    hyperlif_counter += 1
                    diabetes_counter += 1

        # check alkaline phosphatase Middle Eastern (Oriental)
        if patient_origin == "Middle Eastern (Oriental)":
            if alka < 60:
                malnourishment_counter = +1
                lackofvitamins_counter = +1
            if alka > 120:
                liver_counter += 1
                bile_counter += 1
                gland_counter += 1
                diffmed_counter += 1
                if patient_gender == "Female":
                    pregnant_counter += 1

        # check alkaline other origins
        if patient_origin == "Other" or patient_origin == "Ethiopian":
            if alka < 30:
                malnourishment_counter = +1
                lackofvitamins_counter = +1
            if alka > 90:
                liver_counter += 1
                bile_counter += 1
                gland_counter += 1
                diffmed_counter += 1
                if patient_gender == "Female":
                    pregnant_counter += 1

        problems = {"Anemia": anemia_counter,
                    "Diet": diet_counter,
                    "Hemorrhage": hemorrhage_counter,
                    "Hyperlifidmia": hyperlif_counter,
                    "Blood Cells": blood_cells_counter,
                    "Hematologic": hematologic_counter,
                    "Iron Poisoning": ironpos_counter,
                    "Deyhadration": dehydration_counter,
                    "Infection": infection_counter,
                    "Lack of Vitamins": lackofvitamins_counter,
                    "Viral Disease": viral_counter,
                    "Bile Disease": bile_counter,
                    "Heart Disease": heart_counter,
                    "Liver Disease": liver_counter,
                    "Kidney Disease": kidney_counter,
                    "Lack of Iron": iron_counter,
                    "Muscle Disease": muscle_counter,
                    "Smoking": smoke_counter,
                    "Lung Disease": lung_counter,
                    "Thyroid Gland": gland_counter,
                    "Adult Diabetes": diabetes_counter,
                    "Blood Disease": blooddis_counter,
                    "Cancer": cancer_counter,
                    "Over Consumption of Meat": overmeat_counter,
                    "Different use of Medicine": diffmed_counter,
                    "Malnourishment": malnourishment_counter,
                    "Pregnancy": pregnant_counter}

        treatments = {"Anemia": 'Take 2 pills of B12 (10mg) each day for a month',
                      "Diet": 'See a nutritionist',
                      "Hemorrhage": 'Immediately evacuate to the hopspital',
                      "Hyperlifidmia": 'See a nutritionist and take 1 pill of Simovil (5mg) each day for a week',
                      "Blood Cells": 'Take 1 pill of B12 (10mg) and 1 pill of Folate (5mg), both each day for a month',
                      "Hematologic": 'Injection of a hormone to encourage the creation of blood cells',
                      "Iron Poisoning": 'Evacuate to the hospital',
                      "Deyhadration": 'Rest while lying, drink a lot of water',
                      "Infection": 'Antibiotics for infection',
                      "Lack of Vitamins": 'Take a blood test to identify the lacking vitamins',
                      "Viral Disease": 'Rest at home',
                      "Bile Disease": 'Refer to surgical treatment',
                      "Heart Disease": 'See a nutritionist',
                      "Liver Disease": 'Refer to specific diagnosis to decide on treatment',
                      "Kidney Disease": 'Balance the sugar levels in the blood',
                      "Lack of Iron": 'Take 2 pills of B12 (10mg) each day for a month',
                      "Muscle Disease": 'Take 2 pills of Altman C3 turmeric (5mg) each day for a month',
                      "Smoking": 'Stop smoking',
                      "Lung Disease": 'Dont smoke and refer to X-ray on lungs',
                      "Thyroid Gland": 'Take 1 pill of Propylthiouracil (50mg) as advised by the pharmacist',
                      "Adult Diabetes": 'Insulin adjustment for the patient',
                      "Blood Disease": 'Take Cyclophosphamide and Corticosteroids as advised by the pharmacist',
                      "Cancer": 'Take Entrectinib as advised by the pharmacist',
                      "Over Consumption of Meat": 'See a nutritionist',
                      "Different use of Medicine": 'Refer to family dr to check compatibility between different meds',
                      "Malnourishment": 'See a nutritionist',
                      "Pregnancy": 'Refer to pregnancy test'}

        all_values = problems.values()
        max_value = max(all_values)
        problem_list = list(problems.keys())
        values_list = list(problems.values())
        position = values_list.index(max_value)
        critical_problem = problem_list[position]
        critical_problem_treatment = treatments[critical_problem]
        today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = str(patient_id) + '.txt'

        try:
            sugg_file = open(path, 'a')
        except FileNotFoundError:
            Popup_Message('Error', 'Suggestion file not found', qtw.QMessageBox.Critical)
            return

        suggested = str(today) + '\n' + '\n'

        suggested += ('Main Issue is: ' + critical_problem + '\n')
        suggested += ('Treatment for the issue is: ' + critical_problem_treatment + '\n' + '\n')
        suggested += ('There are other suspicions with slim chances, if the condition worsens please follow a check up '
                      'according to this list and see other treatments:\n\n\n')

        suspected_problems = []
        problems.pop(critical_problem)

        for x in list(problems.items()):
            if x[1] > 0:
                suspected_problems.append(x[0])
        for x in suspected_problems:
            if x in treatments.keys():
                suggested += (x + ": " + treatments[x] + '\n' + '\n')

        sugg_file.writelines(suggested)
        self.HomePageUI.textEdit.setPlainText(suggested)
        sugg_file.close()

        self.HomePageUI.stackedWidget.setCurrentIndex(4)

    def Add_Patient_Info(self):

        wbc = self.HomePageUI.lineEdit_wbc.text()
        neut = self.HomePageUI.lineEdit_neut.text()
        lymph = self.HomePageUI.lineEdit_lymph.text()
        rbc = self.HomePageUI.lineEdit_rbc.text()
        hct = self.HomePageUI.lineEdit_hct.text()
        urea = self.HomePageUI.lineEdit_urea.text()
        hb = self.HomePageUI.lineEdit_hb.text()
        crea = self.HomePageUI.lineEdit_creat.text()
        iron = self.HomePageUI.lineEdit_iron.text()
        hdl = self.HomePageUI.lineEdit_hdl.text()
        alka = self.HomePageUI.lineEdit_alkaline.text()

        if wbc == "" or neut == "" or lymph == "" or rbc == "" or hct == "" or urea == "" or hb == "" or crea == "" \
                or iron == "" or hdl == "" or alka == "":
            Popup_Message('Error', 'Please fill the required fields!', qtw.QMessageBox.Critical)
            return False

        minus = '-'
        if minus in wbc:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in neut:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in lymph:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in rbc:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in hct:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in urea:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in hb:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in crea:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in iron:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in hdl:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        if minus in alka:
            Popup_Message('Error', 'Measurements cannot be negative!', qtw.QMessageBox.Critical)
            return False

        for let in wbc:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in neut:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in lymph:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in rbc:
            if let != '.':
                if not let.isdigit():
                    Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                    return False

        for let in hct:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in urea:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in hb:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in crea:
            if let != '.':
                if not let.isdigit():
                    Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                    return False

        for let in iron:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in hdl:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        for let in alka:
            if not let.isdigit():
                Popup_Message('Error', 'Measurements must be digits!', qtw.QMessageBox.Critical)
                return False

        if float(lymph) > 100:
            Popup_Message("Error", 'Lymphocytes cannot be more than 100%', qtw.QMessageBox.Critical)
            return False

        if float(neut) > 100:
            Popup_Message("Error", 'Neutrophil cannot be more than 100%', qtw.QMessageBox.Critical)
            return False

        if float(hct) > 100:
            Popup_Message("Error", 'HCT cannot be more than 100%', qtw.QMessageBox.Critical)
            return False

        try:
            f = open("p_measures.txt", 'w')
        except FileNotFoundError:
            Popup_Message('Error', 'patient measures file not found"', qtw.QMessageBox.Critical)
            return False

        f.writelines(wbc + '\n')
        f.writelines(neut + '\n')
        f.writelines(lymph + '\n')
        f.writelines(rbc + '\n')
        f.writelines(hct + '\n')
        f.writelines(urea + '\n')
        f.writelines(hb + '\n')
        f.writelines(crea + '\n')
        f.writelines(iron + '\n')
        f.writelines(hdl + '\n')
        f.writelines(alka + '\n' + '\n')
        f.close()

        self.HomePageUI.lineEdit_wbc.clear()
        self.HomePageUI.lineEdit_neut.clear()
        self.HomePageUI.lineEdit_lymph.clear()
        self.HomePageUI.lineEdit_rbc.clear()
        self.HomePageUI.lineEdit_hct.clear()
        self.HomePageUI.lineEdit_urea.clear()
        self.HomePageUI.lineEdit_hb.clear()
        self.HomePageUI.lineEdit_creat.clear()
        self.HomePageUI.lineEdit_iron.clear()
        self.HomePageUI.lineEdit_hdl.clear()
        self.HomePageUI.lineEdit_alkaline.clear()

        self.HomePageUI.stackedWidget.setCurrentIndex(3)

    def Back_To_Patient(self):
        self.HomePageUI.stackedWidget.setCurrentIndex(1)

    def Create_New_Patient(self):
        p_name = self.HomePageUI.lineEdit_pname.text()
        p_id = self.HomePageUI.lineEdit_pid.text()
        p_age = self.HomePageUI.lineEdit_page.text()
        p_gender = (self.HomePageUI.comboBox_gender.currentText())
        p_origin = (self.HomePageUI.comboBox_origin.currentText())

        if p_name == "" or p_id == "" or p_age == "" or p_gender == "" or p_origin == "":
            Popup_Message('Error', 'Please fill the required fields!', qtw.QMessageBox.Critical)
            return

        if Check_ID(p_id):
            try:
                f = open('Patients.txt', 'w')
            except FileNotFoundError:
                Popup_Message('Error', 'Patients file not found"', qtw.QMessageBox.Critical)
                return

            f.writelines(p_age+'\n')
            f.writelines(p_origin+'\n')
            f.writelines(p_id+'\n')
            f.writelines(p_gender+'\n')
            f.writelines(p_name+'\n'+'\n')
            f.close()

            self.HomePageUI.lineEdit_pname.clear()
            self.HomePageUI.lineEdit_pid.clear()
            self.HomePageUI.lineEdit_page.clear()
            self.HomePageUI.stackedWidget.setCurrentIndex(2)

    def Login(self):
        user = self.login_register_ui.lineEdit_user.text()
        id = self.login_register_ui.lineEdit_id.text()
        password = self.login_register_ui.lineEdit_password.text()

        if Check_login(user, password, id):
            self.login_register_ui.lineEdit_user.clear()
            self.login_register_ui.lineEdit_id.clear()
            self.login_register_ui.lineEdit_password.clear()
            self.login_register_ui.close()
            self.HomePageUI.show()

    def RegisterPage(self):
        self.login_register_ui.stackedWidget.setCurrentIndex(1)

    def Cancel(self):
        self.login_register_ui.stackedWidget.setCurrentIndex(0)

    def RegisterNewUser(self):
        user = self.login_register_ui.lineEdit_user_register.text()
        id = self.login_register_ui.lineEdit_id_register.text()
        password = self.login_register_ui.lineEdit_password_register.text()

        if Check_register(user, password, id):
            Popup_Message('Success', 'Registered Successfully', qtw.QMessageBox.Information)
            self.login_register_ui.stackedWidget.setCurrentIndex(0)
            self.login_register_ui.lineEdit_user_register.clear()
            self.login_register_ui.lineEdit_id_register.clear()
            self.login_register_ui.lineEdit_password_register.clear()

    def LogOut(self):
        self.login_register_ui.show()
        self.HomePageUI.close()

    def OpenNewPatient(self):
        self.HomePageUI.stackedWidget.setCurrentIndex(1)

    def Open_History(self):
        self.HomePageUI.stackedWidget.setCurrentIndex(5)

    def BackToMain(self):
        self.HomePageUI.stackedWidget.setCurrentIndex(0)

    def OpenPatientHistory(self):
        p_id = self.HomePageUI.lineEdit_history_id.text()
        p_id.rstrip()

        if p_id == '':
            Popup_Message('Error', 'Please fill the required field', qtw.QMessageBox.Critical)

        if Check_ID(p_id):
            path = str(p_id) + '.txt'
            try:
                f = open(path, 'r')
            except FileNotFoundError:
                Popup_Message('Error', 'Patient file not found', qtw.QMessageBox.Critical)
                return False
            log = ''
            while (True):
                line = f.readline()
                if not line:
                    break
                log += line
            self.HomePageUI.textEdit_history_log.setPlainText(log)
        else:
            return False

    def BackFromHistory(self):
        self.HomePageUI.textEdit_history_log.clear()
        self.HomePageUI.lineEdit_history_id.clear()
        self.HomePageUI.stackedWidget.setCurrentIndex(0)

    # =====================out of class functions (for tests)===============================


def Check_login(user, password, id):
    if user == "" or password == "" or id == "":
        Popup_Message('Error', 'Please fill the required fields!', qtw.QMessageBox.Critical)
        return False

    try:
        f = open("accounts.txt", 'r')
    except FileNotFoundError:
        Popup_Message('Error', 'Users file not found"', qtw.QMessageBox.Critical)
        return False

    while True:
        line = f.readline()
        if not line:
            break
        if id == line.strip():
            line = f.readline()
            if user == line.strip():
                line = f.readline()
                if password == line.strip():
                    return True
                else:
                    Popup_Message('Error', 'Password does not match', qtw.QMessageBox.Critical)
                    return False
            else:
                Popup_Message('Error', 'Username not found', qtw.QMessageBox.Critical)
                return False
    Popup_Message('Error', 'ID not found', qtw.QMessageBox.Critical)
    return False
    f.close()


def Check_register(user, password, id):
    if user == "" or password == "" or id == "":
        Popup_Message('Error', 'Please fill the required fields!', qtw.QMessageBox.Critical)
        return False

    try:
        f = open("accounts.txt", 'a')
    except FileNotFoundError:
        Popup_Message('Error', 'Users file not found', qtw.QMessageBox.Critical)
        return False

    if Check_user_registered(user, id):
        Popup_Message('Error', 'User already exists', qtw.QMessageBox.Critical)
        return False

    if Check_Username(user) and Check_Password(password) and Check_ID(id):
        f.write(id+'\n')
        f.write(user+'\n')
        f.write(password+'\n'+'\n')
        f.close()
        return True


def Popup_Message(title, message, icon):
    p_message = qtw.QMessageBox()
    p_message.setIcon(icon)
    p_message.setWindowTitle(title)
    p_message.setText(message)
    p_message.exec_()


def Check_user_registered(user, id):
    try:
        f = open("accounts.txt", 'r')
    except FileNotFoundError:
        Popup_Message('Error', 'Users file not found', qtw.QMessageBox.Critical)
        return
    text = f.read()
    if id in text or user in text:
        f.close()
        return True
    return False


def Check_Username(user):
    if len(user) < 6 or len(user) > 8:
        Popup_Message('Error', 'Username must be between 6 to 8 letters', qtw.QMessageBox.Critical)
        return False
    count = 0
    for let in user:
        if let.isdigit():
            count += 1
        elif not let.isalpha():
            Popup_Message('Error', 'Username must use only english letters (and 2 digits)', qtw.QMessageBox.Critical)
            return False

    if count > 2:
        Popup_Message('Error', 'Username cannot contain more than 2 digits', qtw.QMessageBox.Critical)
        return False
    return True


def Check_Password(password):
    special_chars = ",@,_,,!,#,$,%,^,&,*,(,),<,>,?,/,\,|,},{,~,:,"
    special_lst = special_chars.split(",")
    if len(password) < 8 or len(password) > 10:
        Popup_Message('Error', 'Password must be between 8 to 10 letters', qtw.QMessageBox.Critical)
        return False

    count_let = 0
    count_spec = 0
    count_dig = 0
    for let in password:
        if let.isdigit():
            count_dig += 1
        elif let.isalpha():
            count_let += 1
        elif let in special_lst:
            count_spec += 1
    if count_let == 0 or count_spec == 0 or count_dig == 0:
        Popup_Message('Error', 'Password must contain at least 1 letter, 1 special character and 1 digit',
                      qtw.QMessageBox.Critical)
        return False
    return True


def Check_ID(id):
    if len(id) < 9:
        Popup_Message('Error', 'ID must contain 9 digits', qtw.QMessageBox.Critical)
        return False
    if id=='000000000':
        Popup_Message('Error', 'Please enter valid ID',qtw.QMessageBox.Critical)
        return False
    for dig in id:
        if not dig.isdigit():
            Popup_Message('Error', 'ID must contain digits only', qtw.QMessageBox.Critical)
            return False
    return True

    # =====================must have for execution===============================


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainProgram()
    app.exec_()
