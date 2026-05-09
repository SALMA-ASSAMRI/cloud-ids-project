import zipfile
import os

print("Création du ZIP...")
with zipfile.ZipFile('lambda/function.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.write('lambda/lambda_function.py', 'lambda_function.py')
    z.write('lambda/ids_model.pkl', 'ids_model.pkl')
    
    packages_dir = 'lambda/packages'
    for root, dirs, files in os.walk(packages_dir):
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, packages_dir)
            z.write(filepath, arcname)
    
print("ZIP créé avec succès !")