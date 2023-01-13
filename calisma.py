##############################################
###
### Author Mücahit
### This code developed under mit license
###
### Ankageo
##############################################


import subprocess,glob,os,shutil,sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import QCoreApplication
import psycopg2
from psycopg2 import OperationalError
from re import search

class Pencere(QMainWindow):
    def __init__(self):
        super(Pencere, self).__init__()      
        
                                                       
        uic.loadUi('lidar_uploader.ui', self)            
        
        
        self.select_button.clicked.connect(self.clicker)
        self.cancel_button.clicked.connect(QCoreApplication.instance().quit)
        self.run_button.clicked.connect(self.upload)
        

    def clicker(self):
        
        self.data_typ = self.data_type.currentText()
        self.selected_file.setText("")
        self.fname = QFileDialog.getExistingDirectory(self, "Select File", "/home")
        os.chdir(self.fname)
        t = glob.glob(f"*.{self.data_typ}")
        self.size = (len(t))
        self.selected_file.setText(f"{self.size} Files Selected")
                        
    
    def upload(self):

        host = self.host.text()
        port = self.port.text()
        db_name = self.db_name.text()
        user_name = self.user_name.text()
        password = self.password.text()
        table_name = self.table_name.text()
        from_epsg = self.from_epsg.text()
        to_epsg = self.to_epsg.text()
        self.progressBar.setMaximum(self.size-1)
        

        with open('C:/Users/hp/Desktop/python/lidar_uploader/continue/pipeline.json') as f:
            json1 = f.read()
                
        
        os.chdir(self.fname)
        t = glob.glob(f"*.{self.data_typ}")
        os.makedirs("atilan",exist_ok=True)

        s = 0
        list = ["label1","label2","label3","label4","label5","label6","label7","label8"]
        list1 = [host,port,db_name,user_name,password,table_name,from_epsg,to_epsg]
        m = json1
        for i in list:
            m = m.replace(i,list1[s])
            s += 1

            
        c = 0
        
        try:
            db = psycopg2.connect(host=host,
                            user=user_name,
                            password=password,
                            dbname=db_name,
                            port=port
                        )
            db.close()

            for i in t:
                self.information_text.setText("Upload Starting")
                QApplication.processEvents() 
                self.progressBar.setValue(c)
                c+=1
                k = m.replace("mfss",i)
                file = open("json.json","w")
                file.write(k)
                file.close()               

                try:
                    subprocess.run(["pdal","pipeline","json.json"],capture_output=True, text=True, check=True)
                                 
                except:
                    tyy = subprocess.run(["pdal","pipeline","json.json"], capture_output=True)
                    os.makedirs("hatali", exist_ok=True)
                    outfile1 = open("hatali.txt","a")
                    outfile1.write(f"{i} = {tyy.stderr}")
                    outfile1.write("\n")
                    outfile1.close()
                    shutil.move(i,"hatali/"+i)
                    continue
                
                shutil.move(i,"atilan/"+i)

            self.information_text.setText("Upload Finish") 

        except OperationalError as err:
            er = str(err)
            
            if search("database",er):
                self.information_text.setText("Database Name Wrong")

            elif search("password",er):
                self.information_text.setText("User Name or Password Wrong")
                
            else:
                self.information_text.setText("Host or Port Wrong")
                
        
app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())
