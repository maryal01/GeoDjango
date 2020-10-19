import os, requests, zipfile
name= "NHD_H_Alabama_State_Shape.jpg"
link = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/NHD/State/HighResolution/Shape/"

state_names = ["Alaska", "Alabama", "Arkansas", "American_Samoa", "Arizona", "California", 
"Colorado", "Connecticut", "District_of_Columbia", "Commonwealth_of_the_Northern_Mariana_Islands", 
"Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", 
"Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", 
"Mississippi", "Montana", "North_Carolina", "North_Dakota", "Nebraska", "New_Hampshire", "New_Jersey", 
"New_Mexico", "Nevada", "New_York", "Northern_Mariana_Islands","Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
"Puerto_Rico", "Rhode_Island", "South_Carolina", "South_Dakota", "Tennessee", "Texas", "Utah", "Virginia", 
"United_States_Virgin_Islands", "Vermont", "Washington", "Wisconsin", "West_Virginia", "Wyoming"]
#test_state_names = ["American_Samoa", "United_States_Virgin_Islands", "Commonwealth_of_the_Northern_Mariana_Islands", "District_of_Columbia", "Northern_Mariana_Islands"]
cwd = os.getcwd()
extension = "zip"
directory = "state-files"
path = os.path.join(cwd, directory)
if not os.path.exists(path):
    os.mkdir(path)


for state in state_names:
    url = "{}NHD_H_{}_State_Shape.{}".format(link, state, extension)
    file_path = os.path.join(path, "{}.{}".format(state, extension))
    extract_path = os.path.join(path, state)

    r = requests.get(url, allow_redirects=True)

    f = open(file_path, 'wb')
    f.write(r.content)
    f.close()

    z = zipfile.ZipFile(file_path)
    z.extractall(extract_path)
    z.close()

    os.remove(file_path)
    print("Extracted from {}".format( state))
