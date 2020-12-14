# -*- coding: utf-8 -*-
import json
import logging
from getpass import getpass
from encAW import Encaw

print('''
    Developed by: Awiteb
    GitHub: Awiteb
    Email: Awiteb@hotmail.com
''')
pathOFlogFile = "log/usersLog.log"
#Syntax of new json file will be > {"usersData":[]}
pathOFjsonFile = "jsonFile/usersData.json"
"""لم يتم اكمال المتجر لا لان المتجر فقط توضيح لكيفية التعامل مع البيانات وتحديثها باستخدام السستم """

logging.basicConfig(filename=pathOFlogFile,level=logging.INFO,format="%(asctime)s -- %(message)s")

class UserSys: #انشاء كلاس للتعامل مع المستخدم
    def __init__(self,jsonFile): #اخذ مسار ملف الجسون لحفظ البيانات فيه
        self.login = False
        self.jsonFile = jsonFile
        with open(jsonFile,'r') as jsf: #سحب البيانات المستخدمين من ملف جسون
            self.data = json.load(jsf)
            self.usersData = self.data["usersData"] #اخذ بيانات المستخدمين فقط

        with open('key.txt','r') as f: #(اخذ مفتاح التشفير وفك التشفير (لتشفير اسم المستخدم وكلمة المرور
            self.enKey = f.read()

    def awEn(self,text):
        return Encaw(self.enKey,text).enc_encrypt()
    def awDe(self,text):
        return Encaw(self.enKey,text).enc_decrypt()

    def checkUsername(self): # (True) اذا كان اسم المستخدم موجود  (False) اذ لم يكن
        for user in self.usersData:
            try:
                if self.awDe(user['username']) == self.Nusername:
                    return True
            except:
                if self.awDe(user['username']) == self.username:
                    return True
        return False

    def delUser(self): #دالة لحذف المستخدم
        sure = input("Are you sure to delete your account? * The account cannot be recovered (y/ ): ").lower()
        if sure == 'y':
            del self.usersData[self.userIndex] #امر الحذف (يتم اخذ رقم الحقل عند تسجيل الدخول)ء
            logging.info(f'DELETE ACCOUNT: user:{self.username}')
            return True
        else:
            return False

    def updateUsername(self): #دالة لتعديل اسم المستخدم
        while True:
            cancel = input("Cancel? (y/ )").lower()
            if cancel == 'y':
                break
            else:
                self.Nusername = input("New Username: ").lower()
                if len(self.Nusername) < 3  or ' ' in self.Nusername: #شروط اسم المستخدم
                    print("False, the username must be greater than 3, and the space must not be placed")
                    continue
                if self.checkUsername(): #اذا كان الاسم موجود
                    print(f"{self.Nusername} isn't available. PuserControlse try another")
                else: # اذ لم يكن
                    sure = input(f"Are you sure to change {self.username} to {self.Nusername}? (y/ )").lower()
                    if sure == 'y':
                        self.usersData[self.userIndex]['username'] = self.awEn(self.Nusername) #تشفير اسم المستخدم قبل دخوله ملف جسون
                        self.username = self.Nusername
                        print("\nUsername has been successfully updated\n")
                        logging.info(f"UPDATE USERNAME: Last:{self.username} -- New:{self.Nusername}")
                        break
                    else:
                        break


    def updatePassword(self): #دالة لتغير كلمة المرور
        while True:
            cancel = input("Cancel? (y/ ): ").lower()
            if cancel == 'y':
                break
            else:
                oldPass = getpass("Enter the password before changing it: ")
                if oldPass != self.password: #التحقق اذا كانت كلمة المرور متطابقة
                    print("\nSorry, the password is not correct.")
                    continue
                while True:
                    self.Npassword = getpass("New password: ")
                    Repassword = getpass("Re-enter the New password: ")
                    if self.Npassword == Repassword: #اذا كانت كلمتي المرور متطابقين
                        break #الخروج من حلقة طلب كلمة المرور
                    else:
                        print("The two passwords are not identical.")
                if len(self.Npassword) < 8  or ' ' in self.Npassword: #شروط كلمة المرور
                    print("False, the password must be greater than 8, and the space must not be placed")
                    continue
                sure = input(f"Are you sure to change password? (y/ ): ").lower()
                if sure == 'y':
                    self.usersData[self.userIndex]['password'] = self.awEn(self.Npassword) #تشفير كلمة المرور قبل دخولها ملف جسون
                    self.password = self.Npassword
                    print("\npassword has been successfully updated\n")
                    logging.info(f"UPDATE PASSWORD: user:{self.username}")
                    break
                else:
                    break


    def singup(self):
        user = {}
        while True:
            cancel = input("Cancel? (y/ ): ").lower()
            if cancel == 'y':
                break
            else:
                self.username = input("User: ").lower()
                while True:
                    self.password = getpass("password: ")
                    Repassword = getpass("Re-enter the password: ")
                    if self.password == Repassword:
                        break
                    else:
                        print("The two passwords are not identical.")
                if len(self.username) < 3 or len(self.password) < 8 or ' ' in self.password or ' ' in self.username:
                    print("False, the username must be greater than 3, the password must be greater than 8,\and the space must not be placed")
                    continue
                if self.checkUsername():
                    print(f"{self.username} isn't available. PuserControlse try another")
                    continue
                else:
                    user["username"] = self.awEn(self.username) #تشفير اسم المستخدم قبل دخوله ملف جسون
                    user["password"] = self.awEn(self.password) #تشفير كلمة المرور قبل دخوله ملف جسون
                    user["coins"] = self.awEn('500') #تشفير عدد الكوينز
                    user["ammos"] = {"9×19mm":self.awEn("30"),"7.62×39mm":self.awEn("0"),"70mm shells":self.awEn("0")}
                    user["weapons"] = [{'Name':self.awEn('m9'),'Ammo':user["ammos"]["9×19mm"],'Speed':self.awEn('0.5'),\
                    'Damage':self.awEn('1.3'),'Caliber':self.awEn('9×19mm'),'Price':self.awEn('200')}] #تشفير السلاح
                    self.usersData.append(user)
                    self.upData()
                    print("Now go to login")
                    logging.info(f"SING UP: user:{self.username}")
                    break

    def logIn(self):
        while not self.login:
            cancel = input("Cancel? (y/ ): ").lower()
            if cancel == 'y':
                break
            else:
                self.username = input("User: ").lower()
                self.password = getpass("password: ")
                for user in self.usersData:
                    if self.awDe(user['username']) == self.username and self.awDe(user['password']) == self.password:
                        print("Login successfully")
                        self.login = True
                        self.userD = user
                        self.userIndex = self.usersData.index(self.userD)
                        self.userCoins = self.userD['coins']
                        self.userWeapons = self.userD['weapons']
                        self.userWeaponsName = [self.awDe(weapon['Name']) for weapon in self.userWeapons]
                        logging.info(f"LOGIN: user:{self.username}")

                if not self.login:
                    print("theis data wasn't found")
    def upData(self):
        with open(self.jsonFile,mode='w') as jf:
            json.dump(self.data,jf,indent=2)
#---نهاية كلاس التعامل مع المستخدم---#




##--مثال لركيب السستم على متجر اسلحة---
class Store():
    def __init__(self,USER): #اخذ كائن السستم للتاعمل معه
        self.USER = USER # حفظ الكائن
        self.sections = ["Weapons"] # وضع خانات المتجر
        self.weapons = [
        {"Name":self.USER.awEn("AK-47"),'Ammo':self.USER.awEn("60"),'Speed':self.USER.awEn("0.25"),'Damage':self.USER.awEn("3.2"),'Caliber':self.USER.awEn("7.62×39mm"),"Price":self.USER.awEn("1865")},
        {"Name":self.USER.awEn("UTS-15"),'Ammo':self.USER.awEn("28"),'Speed':self.USER.awEn("1,2"),'Damage':self.USER.awEn("5.6"),'Caliber':self.USER.awEn("70mm shells"),"Price":self.USER.awEn("2387")}
        ] #الاسلحة اللتي سوف يبيعها المتجر
        self.ammunition = ["9×19mm","7.62×39mm", "70mm shells"] #الذخيرة التي سوف يبيعها المتجر


    def printWeapons(self,toget): #طباعة الاسلحة (متغير toget هو المكان الذي تريد اخذ الاسلحة منه (اسلحة المستخدم او المتجر)
        for weaponIndex, weapon in enumerate(toget, start= 1): #اخذ السلاح مع الاندكس حقه
            print(f"------ID: {weaponIndex}-------")
            for key,value in weapon.items():
                print(f"{key}: {self.USER.awDe(value)}")

    def getval(self,num,keyOFval):
        return self.weapons[num].get(keyOFval)



userControl = UserSys(pathOFjsonFile) #انشاء كائنن من الكلاس
store = Store(userControl) #انشاء كائنن من الكلاس ووضع بداخله الكائن الي يتحكم بالمستخدم


##----التحكم بالكلاس----

while not userControl.login: #وايل لتسجيل الدخول ضمان عدم الدخول الى الواجهة الرئسية الا وقد تم التسجيل
    print("\nLogin[1]  Sing up[2]\n")
    choice = input(">: ").lower() #اخذ اذا كنت تريد انشاء حساب ام التسجيل
    
    if choice == '1': #اذا كان الاختيار التسجيل
        if userControl.login: # اذا كانت قيمة تسجيل الدخول ترو يطبع الرسالة
            print("You are really logged in")
        else: # اذا كانت فولس تشغبل دالة تسجيل الدخول
            userControl.logIn()
    elif choice == '2': #اذا كان الاختيار انشاء حساب
        if userControl.login: # اذا كانت قيمة تسجيل الدخول ترو يطبع الرسالة
            print("You are really logged in")
        else:# واذ كانت فولس تشغيل دالة انشاء الحساب
            userControl.singup()


#--------------------------------------#

interFace = True #القائمة الرئسية للعبة
while interFace: #طالمة الواجهة قيمتها ترو
    print(f"\nYour coins is {userControl.awDe(userControl.userCoins)}") #طباعة عدد العملات عند اللاعب #طباعة عدد العملات عند اللاعب
    print("\n  My account[1]   Store[2]   Get coins(*for test sys*)[3]  or exit\n")
    choice = input(">: ").lower()

    if choice == '1':
        if userControl.login: #اذا تم تسجيل الدخول
            while True:
                print(f"\nYour coins is {userControl.awDe(userControl.userCoins)}") #طباعة عدد العملات عند اللاعب
                print("\n  Info account[1]   My weapon[2]  Update name[3]   Update password[4]   Delete account[5] or exit")
                choice = input(">: ").lower()
                if choice == '1':
                    for key,value in userControl.userD.items():
                        if key != 'weapons' and key != 'ammos': # لاتطبع الاسلحة في بمعلومات الحساب ولاتطبع الذخيرة لان طريقة طباعتها مختلفة
                            print(f"Your {key}: {userControl.awDe(value)}")
                        if key == 'ammos':
                            for ammo,value in userControl.userD[key].items():
                                print(f"Ammo:{ammo}  quantity:{userControl.awDe(value)}")


                elif choice == '2':
                    store.printWeapons(userControl.userWeapons) #طباعة اسلحة المستخدم
                elif choice == '3':
                    userControl.updateUsername() #دالة تغير الاسم
                elif choice == '4':
                    userControl.updatePassword() #دالة تغير الباسورد
                elif choice == '5':
                    if userControl.delUser(): #دالة حذف الحساب (return True or False)
                        interFace = False #عند حذف الحساب يتم ايقاف الواحهة ورفع البيانات
                        userControl.upData() #دالة رفع البيانات
                        break
                    else:
                        pass

                elif choice == 'exit':
                    break
                else:
                    print(f"Sorry, {choice} not available") #طباعة رسالة تفيد ان الامر  الذي ادخلته ليس موجود

    elif choice == '2':
        while True: #وايل المتجر
            print(f"\nYour coins is {userControl.awDe(userControl.userCoins)}") #طباعة عدد العملات عند اللاعب
            print("\n  Weapons[1]   [exit]\n")
            choice = input(">: ").lower()
            if choice == '1':
                while True: #وايل قائمة الاسلحة
                    print(f"\nYour coins is {userControl.awDe(userControl.userCoins)}") #طباعة عدد العملات عند اللاعب
                    print("\n  Buy weapons[1]   Buy ammo[2]   Weapon upgrade[3]   Sell weapon[4]   Sell ammo[5]   [exit]\n")
                    choice = input(">: ").lower()
                    if choice == '1': #اذا الاختيار كان شرا سلاح
                        store.printWeapons(store.weapons) #طباعة الاسلحة الموجود لاشرائها
                        while True: # وايل شراء السلاح
                            try:
                                choice = int(input("\nEnter id of weapon: "))
                            except ValueError: #اذا حدثت مشكلة بقيمة المدخلات
                                print("PuserControlse, enter the id as integar..!")
                                continue #الرجوع لبداية وايل شراء السلاح

                            if choice <= len(store.weapons) and choice > 0: #اذا كان الايدي المدخل اصغر من او يساوي عدد الاسلحة او اصغر من الصفر
                                if userControl.awDe(store.getval(choice - 1,'Name')) not in userControl.userWeaponsName: #اذ لم يكن السلاح عند المستخدم
                                    if int(userControl.awDe(userControl.userCoins)) >= int(userControl.awDe(store.getval(choice - 1,'Price'))): #اذا كان عدد العملات اكبر من او يساوي سعر السلاح
                                        #رسالة تاكيد لشراء السلاح
                                        sure = input(f"Are you sure you want to buy '{userControl.awDe(store.getval(choice - 1,'Name'))}' for the price of {userControl.awDe(store.getval(choice - 1,'Price'))} It will stay with you when you buy {int(userControl.awDe(userControl.userCoins)) - int(userControl.awDe(store.getval(choice - 1,'Price')))} (y/n): ").lower()
                                        if sure == 'y': #اذا تمت الموافقة على الرسالة
                                            logging.info(f"BUY WEAPON: user:{userControl.username} -- weapon:{userControl.awDe(store.getval(choice - 1,'Name'))}")
                                            userControl.userWeapons.append(store.weapons[choice - 1]) #اضافة السلاح الى مجموعة الاسلحة
                                            userControl.userD['coins'] = userControl.userCoins = userControl.awEn(str((int(userControl.awDe(userControl.userCoins))) - (int(userControl.awDe(store.getval(choice - 1,'Price')))))) #طرح سعر السلاح من سعر العملات
                                            userControl.upData() #رفع البيانات
                                            break #الخروج من وايل شراء السلاح

                                        elif sure == 'n': #اذا لم يتم الموافقة
                                            break #الخروج من وايل شراء السلاح

                                        else: #اذا كان المدخل غير يس او نو
                                            print("choice 'y' or 'n'") #اطبع الرسالة

                                    else: #اذا العملات التي لديه لاتكفي
                                        print("Sorry, you don't have enough coins")
                                        break #الخروج من وايل شراء السلاح
                                else: #اذا السلاح كان عند المستخدم
                                    print(f"{userControl.awDe(store.getval(choice - 1,'Name'))} You already have it, you can go to sell it or upgrade it")
                                    break #الخروج من وايل شراء السلاح

                            else: #اذا كان الايدي المدخل اكبر من عدد الاسلحة
                                print("Sorry, there is no weapon ID with this number")

                    elif choice == 'exit':
                        break
            elif choice == 'exit':
                break

    elif choice == '3':
        userControl.userD['coins'] = userControl.userCoins = (userControl.awEn(str(int(userControl.awDe(userControl.userCoins)) + 500)))
        print("Done add 500 coins..")

    elif choice == 'exit':
        logging.info(f"LOGOUT: user:{userControl.username}")
        userControl.upData()
        interFace = False

    else:
        print(f"Sorry, {choice} not available") #طباعة رسالة تفيد ان الامر  الذي ادخلته ليس موجود
