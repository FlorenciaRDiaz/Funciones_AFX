print("holi")
#libreria modificada
def load(filedir):
  from prediction_results import prediction_results
  Z = {}
  protein_count = 0
  extract_folder = os.path.basename(filedir[:-5])
  #os.makedirs(extract_folder, exist_ok=True)
  with ZipFile(filedir,'r') as fz:
    fz.extractall(".")

  if os.path.isdir(extract_folder):
    pass
  else:
    os.system(f"cp -R prediction_{extract_folder} {extract_folder}") #compatibility with old afxt files

  for path in os.listdir(extract_folder):
    long_path = os.path.join(extract_folder, path)
    if long_path.endswith(".txt"):
      with open(long_path,'r') as file:
        lines = file.readlines()
        file.close()
      for zipf in lines:
        zipf = zipf[:-1]
        if not "/" in zipf:
          zipf = os.path.join(extract_folder, zipf)
        if os.path.exists(zipf) == True: #Excluding linebreaks
              protein_count = protein_count + 1
              with ZipFile(zipf, 'r') as fz:
                for zip_info in fz.infolist():
                  if zip_info.filename[-1] == '/':
                    continue
                  tab = os.path.basename(zip_info.filename)
                  if tab.endswith(".txt"):
                    #zip_info.filename = os.path.basename(zip_info.filename)
                    with fz.open(zip_info.filename) as pred_info:
                      pred_lines = pred_info.readlines()
                      uncut_pred_lines = pred_info.read()
                      pred_info.close()
                    #details = pred_lines.values()
                    try:
                      ptmscore = float(re.findall(r"pTMScore=?([ \d.]+)",uncut_pred_lines)[0])
                    except:
                      ptmscore = 0
                    prediction_entry = prediction_results(pred_lines[0].strip().decode('UTF-8'),pred_lines[1].strip().decode('UTF-8'),pred_lines[2].strip().decode('UTF-8'),pred_lines[3].strip().decode('UTF-8'),ptmscore)
                    Z[f'AF_p{protein_count}'] = prediction_entry
  print("Loaded successfully.")
  #print(Z)
  predictions_AF=Z
  return predictions_AF
filedir='/content/drive/Shareddrives/PI /4.AFXT/3.AWS_FULL_AF/NIST_AWS_Full_AF_20230926.afxt'
results_AF=load(filedir)
print(results_AF)
