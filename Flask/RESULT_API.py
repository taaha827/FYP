import sys
import os
from flask import Flask, request, redirect, url_for     
from werkzeug.utils import secure_filename
sys.path.append('../')
import flask as f
from flask import render_template 
from flask import jsonify,request
sys.path.insert(0, '../image_processor/')


import downs_analysis
import tweeds_analysis
import wits_analysis
import ricketts_analysis
import bjork_analysis
import Image_processor as ip
app = f.Flask(__name__,static_folder='static')
app.config["DEBUG"] = True
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'image_processor/Sources'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

A = [0,0]
ANS = [0,0]
API= [0,0]
APS= [0,0]
B= [0,0]
BA= [0,0]
BO= [0,0]
GI= [0,0]
GN= [0,0]
GO= [0,0]
LI= [0,0]
LS= [0,0]
ME= [0,0]
N= [0,0]
O= [0,0]
P= [0,0]
S= [0,0]
PO= [0,0] 
PNS= [0,0]
points = [A,ANS,API,APS,B,BA,BO,GI,LI,LS,ME,N,O,P,S,PO,PNS]

@app.route('/',methods=['GET'])
def home():
    return('Hello this is just the home page')

@app.route('/upload/',methods =['POST'])
def upload_scan():
    return("I am uploading")
    if request.method == 'POST':
        # check if the post request has the file part
        if file not in request.files:
            return('Error')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return('No file is selected')
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/inital/<string:file_name>',methods =['GET'])
def cannya(file_name):
        print("I am here")
        niter= 2
        kappa= 45
        gamma= 0.25
        option= 1
        x =0

        test_object = ip.image_processing("../image_processor/Sources/"+file_name )
        test_object.load_image()
        test_object.convert_to_gray_scale()
        test_object.find_region_of_interest()
        #test_object.crop_and_save_region_of_interest()
        #test_object.show_region_of_interest()
        #test_object.show_image(test_object.background_image)
        test_object.HTV_LTV_calculation()
        test_object.perform_gaussian_blur()  
        test_object.number_of_iteration = niter
        test_object.kappa= kappa
        test_object.gamma_value=gamma
        test_object.option=1
        x = file_name
        test_object.applying_anisotropic_diffusion(x)
        test_object.perform_preliminary_canny_edge_detection(x)
        return jsonify('True')
        # niter= 2
    # kappa= 45
    # gamma= 0.25
    # option= 1
    # x =0
    
    # test_object = ip.image_processing("../image_processor/Sources/"+file_name )
    # result = test_object.load_image()
    # if result:
    #     test_object.convert_to_gray_scale()
    #     test_object.find_region_of_interest()
    #     test_object.HTV_LTV_calculation()
    #     test_object.perform_gaussian_blur()  
    #     test_object.number_of_iteration = niter
    #     test_object.kappa= kappa
    #     test_object.gamma_value=gamma
    #     test_object.option=1
        
    #     test_object.applying_anisotropic_diffusion(x)
    #     test_object.perform_preliminary_canny_edge_detection(x)
    #     return jsonify('successful')
    # else:
    #     return('No File found')

@app.route('/get_points/<string:file_name>')
def return_points(file_name):
#[A,ANS,API,APS,B,BA,BO,GI,LI,LS,ME,N,O,P,S,PO,PNS]
    pints ={'0':{'Label':'A','X':'','Y':''},'1':{'Label':'ANS','X':'','Y':''},'2':{'Label':'API','X':'','Y':''},'3':{'Label':'APS','X':'','Y':''},'4':{'Label':'B','X':'','Y':''},'5':{'Label':'BA','X':'','Y':''},'6':{'Label':'BO','X':'','Y':''},'7':{'Label':'GI','X':'','Y':''},'8':{'Label':'LI','X':'','Y':''},'9':{'Label':'LS','X':'','Y':''},'10':{'Label':'ME','X':'','Y':''},'11':{'Label':'N','X':'','Y':''},'12':{'Label':'O','X':'','Y':''},'13':{'Label':'P','X':'','Y':''},'14':{'Label':'S','X':'','Y':''},'15':{'Label':'PO','X':'','Y':''},'16':{'Label':'PNS','X':'','Y':''}}
    obj = downs_analysis.downs_analysis(file_name)
    obj.setvalues()
    i=0
    x=0
    for i in range(0,obj.points.__len__()):
        print(obj.points.__len__())
        pints[str(i)]['X'] = str(obj.points[i][0])
        pints[str(i)]['Y'] = str(obj.points[i][1])
        i+=1
        
    return jsonify(pints)

    
@app.route('/recalculate/<string:analysis_type>',methods =['POST'])
def recalculate(analysis_type):
    index = 0
    if request.method == 'POST':
            result = f.response.get_json()
            for obj in result:
                points[index][0]= obj['X']
                points[index][1]= obj['Y']
                index+=1

            if analysis_type == 'downs analysis':
                obj = downs_analysis.downs_analysis('test')
                obj.points = points
                obj.facial_angle()
                obj.angle_of_convexity()
                obj.AB_angle()
                obj.mandibular_plane_angle()
                obj.yaxis()
                obj.cant_of_oclusion()
                obj.incisor_angle()
                obj.incisor_occlusion_angle()
                obj.upper_incisor_angle()
                #call all downs analysis calculation functions here
                return jsonify(obj.result)
            elif analysis_type=='tweeds anlaysis':
                #call all the function for tweeds analysis here
                obj = tweeds_analysis.tweeds_analysis()
                obj.points[0] = points[12]
                obj.points[1] = points[13]
                obj.points[2] = points[8]
                obj.points[3] = points[9]
                obj.points[4] = points[8]
                obj.points[5] = points[7]
                obj.frankfort_mandibular_plan_angle()
                obj.incisor_mandibular_plan_angle()
                obj.frankfort_mandibular_incisor_angle()
                
                return jsonify(obj.result)
            elif analysis_type=='wits anlaysis':
                obj = wits_analysis.wits_analysis('test')
         #[A,ANS,API,APS,B,BA,BO,GI,LI,LS,ME,N,O,P,S,PO,PNS]
                #[A,B,N,O]
                obj.points[0] = points[0]
                obj.points[1] = points[4]
                obj.points[2] = points[12]
                obj.points[3] = points[11]
                obj.Functional_Occlusion_plan_angle()
                obj.ANB_angle()
                return jsonify(obj.result)
                


@app.route('/result/<string:file_name>/<string:analysis_type>')
def result1(file_name,analysis_type):
    if analysis_type == 'downs analysis':
        obj = downs_analysis.downs_analysis(file_name)
        obj.setvalues()
        obj.facial_angle()
        obj.angle_of_convexity()
        obj.AB_angle()
        obj.mandibular_plane_angle()
        obj.yaxis()
        obj.cant_of_oclusion()
        obj.incisor_angle()
        obj.incisor_occlusion_angle()
        obj.upper_incisor_angle()
        #call all downs analysis calculation functions here
        return jsonify(obj.result)
    elif analysis_type=='tweeds anlaysis':
        #call all the function for tweeds analysis here
        obj = tweeds_analysis.tweeds_analysis(file_name)
        obj.setvalues()
        obj.frankfort_mandibular_plan_angle()
        obj.incisor_mandibular_plan_angle()
        obj.frankfort_mandibular_incisor_angle()
        
        return jsonify(obj.result)
    elif analysis_type=='wits anlaysis':
        obj = wits_analysis.wits_analysis(file_name)
        obj.setvalues()
        obj.Functional_Occlusion_plan_angle()
        obj.ANB_angle()
        return jsonify(obj.result)

        

if __name__ == "__main__":
    app.run()
