import csv
import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def generate(p_sRowData):
  l_sPrompt ="""Sample:
--------------------------------
Age,Height,Weight,BMI
23,72,200,27
Output:
{
\"discrepancy_flag\": \"N\"
,\"reason\": \"NA\"
}

--------------------------------

Sample:
--------------------------------
Age,Height,Weight,BMI
24,62,144,26
Output:
{
\"discrepancy_flag\": \"N\"
,\"reason\": \"NA\"
}
--------------------------------

Sample:
--------------------------------
Age,Height,Weight,BMI
45,66,120,19
Output:
{
\"discrepancy_flag\": \"N\"
,\"reason\": \"NA\"
}
--------------------------------

Sample:
--------------------------------
Age,Height,Weight,BMI
50,62,144,26
Output:
{
\"discrepancy_flag\": \"N\"
,\"reason\": \"NA\"
}
--------------------------------

Sample:
--------------------------------
Age,Height,Weight,BMI
24,62,1000,26
Output:
{
\"discrepancy_flag\": \"Y\"
,\"reason\": \"Height incorrect\"
}
--------------------------------

Sample:
--------------------------------
Age,Height,Weight,BMI
35,25,0,29
Output:
{
\"discrepancy_flag\": \"Y\"
,\"reason\": \"Weight incorrect \"
}
--------------------------------


Find discrepancy_flag and reason in JSON format:
--------------------------------
Age,Height,Weight,BMI"""
  

  
  l_supStr= """
  Output:
  ?
  --------------------------------"""


  l_sPrompt=l_sPrompt+p_sRowData+l_supStr
  #l_sPrompt=l_sPrompt.format(p_sRowData)

  model = GenerativeModel("gemini-pro-vision")
  responses = model.generate_content(
    l_sPrompt,
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 32
    },
  stream=True,
  )
  l_fullStrRes=''
  for response in responses:
      l_fullStrRes= l_fullStrRes+ response.text #+print(, end="\n\n")
  l_fullStrRes= l_fullStrRes.replace("```\n","")
  l_fullStrRes= l_fullStrRes.replace("\n```","")
  print(l_fullStrRes)
  return l_fullStrRes
      

def processFile(filepath,fileName):
  l_fBadData = open(filepath+"/"+fileName+".bad", "w")
  with open(filepath+"/"+fileName, mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
      l_sRow = ','.join(map(str, lines))
      print(l_sRow)
      l_sRetDict= generate(l_sRow)
          
      res = json.loads(l_sRetDict)
      if res.get("discrepancy_flag")=="Y":
        l_fBadData.writelines(l_sRow+','+res.get("reason")+"\n")
  l_fBadData.close()

        

             



processFile("./Data","sub_bmi_data.csv") 