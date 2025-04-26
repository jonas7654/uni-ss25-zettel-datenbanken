import os
import shutil
from pypdf import PdfWriter
from PIL import Image

# TODO CREATE ZIP OF SRC DIR

# returns if the file is not an image/pdf
# to just allow whole tex files in img folder.
def not_an_image(imagepath):
    extension=str(imagepath).split('.')[-1]
    return not (extension.lower() in ['pdf','jpg','jpeg','png','tiff','gif'])

# converts image to pdf and stores it to target
def convert_image(imagepath, target):
    if(str(imagepath).endswith("pdf")):
        shutil.copy(imagepath,target)
        return

    image = Image.open(imagepath)
    image.load()
    background = Image.new("RGB", image.size, (255, 255, 255))

    # skip RGBA handling if there is no Alpha channel
    if len(image.split())<4:
        image.save(target, 'PDF', resoultion=100.0)
        return
    
    # handles RGBA conversion (otherwise there would be a black background)
    background.paste(image, mask=image.split()[3]) # 3 is the alpha channel
    background.save(target, 'PDF', resoultion=100.0)

def create_pdf(dir):
    pdf_name="IAD-Zettel-" + dir+".pdf"
    print("Creating "+pdf_name)
    writer = PdfWriter()

    writer.append("./Deckblatt.pdf")

    path = "./" + directory + "/img"

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print(" - Found "+str(len(files))+" files (maybe some blacklisted files)")

    files.sort()

    for file in files:
        filepath="./"+dir+"/img/"+file
        if(not_an_image(filepath)): continue
        convert_image(filepath,"./tmp/"+file+".pdf")
        writer.append("./tmp/"+file+".pdf")
        print(" - Added "+file+".")


    writer.write("build/"+pdf_name)
    writer.close


print("Generating PDF files...")

all_directories = os.listdir(".")
directories = list(filter(lambda dir: os.path.isdir(dir) and dir != "." and dir != "." and dir != ".github" and dir != "src", all_directories))

print("Found " + str(len(directories)) + " Directories.")

for directory in directories:
    if not os.path.isdir("./" + directory + "/img"):
        print("Skipped " + directory + ", no img Folder found.")
        continue

    create_pdf(directory)
