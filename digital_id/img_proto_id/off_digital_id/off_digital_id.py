
from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import datetime as dt 
import pandas as pd 
from faker import Faker 
import random as rand 

start = Faker()


app = Flask(__name__)

class UserInfo:
    def __init__(self):
        self.city = "Clinton"
        self.state = "TN"
        self.zip_code = "37716"

    def get_personal_info(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        age = int(input("Enter your current age: "))
        dob = input("Enter your date of birth [mm/dd/yyyy]: ")
        address = input("Enter your current street address: ")
        weight = input("Enter your weight: ")
        height = input("Enter your height [#ft #in]: ")
        eye_color = input("Enter your eye color: ")
        return {
            "first_name": first_name,
            "last_name":last_name,
            "age": age,
            "dob": dob,
            "address": address,
            "weight": weight,
            "height": height,
            "eye_color": eye_color
        }

    def saveInfo(self):
        data = [self.first_name, self.last_name, self.age, self.dob, self.address, self.weight, self.height, self.eye_color ]
        df = pd.DataFrame(data)
        print(df)
        
class IDGenerator:
    def generate_id(self, user_info, logo_path='me.jpg'):
        logo = Image.open(logo_path)
        # Resize logo if necessary
        basewidth = 100
        wpercent = basewidth / float(logo.size[0])
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize))
        qr_code_data = '\n'.join([f"{key}: {value}" for key, value in user_info.items()])
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(qr_code_data)
        qr.make()
        qr_img = qr.make_image(fill_color='green', back_color='white').convert('RGB')
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos)
        qr_img.show()
     
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST', 'GET'])
def generate_qr():
    user_info_manager = UserInfo.get_personal_info()
    user_info = user_info_manager.get_personal_info()
    id_generator = IDGenerator.generate_id()
    qr_filename = id_generator.generate_id(UserInfo)
    return send_file(qr_filename, as_attachment=True)

@app.route('/display_qr')
def displayQR():
    pass


if __name__ == "__main__":
    print("Welcome to SID Services.\n")
    user_info_manager = UserInfo()
    user_info = user_info_manager.get_personal_info()
    #UserInfo.saveInfo()
    id_generator = IDGenerator()
    id_generator.generate_id(user_info)
    #app.run(debug=True)
    

    
    
