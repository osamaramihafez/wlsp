"""Get lockscreen background pictures."""
import os
from shutil import copyfile, copy2
import imghdr
import getpass

DESTINATION = os.getcwd()
print(DESTINATION)
try:
    os.mkdir(os.path.join(DESTINATION, "pics_fetched"))
except FileExistsError:
    print("pics_fetched folder already exists. Good.")

DESTINATION = os.path.join(DESTINATION, "pics_fetched")

PICS_OLD_L = r"/mnt/c/Users/osama.hafez/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"
TYPE = ".jpg"

def find_path_to_pictures():
    """
    Return the path where the desktop background pictures are stored using the
    person's username.
    """
    # user = getpass.getuser()
    # path = "/mnt/c/Users/{0}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets".format(user)
    path = "/mnt/c/Users/osama.hafez/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"
    return path

def rename_files(deliver, batch, dest):
    """
    Rename file paths to delivery location and changes file extension from nothing to TYPE
    """
    file_num = 0
    for file in os.listdir(dest):
        if "." not in file and file != "Moved for Python":
            if file_num == 0:
                try:
                    os.rename(deliver + "/" + file,  deliver + "/" +"Picture (Batch {0}){1}".format(batch, TYPE))
                    file_num += 1
                except PermissionError:
                    print("Permission error on " + file)
                    pass
            else:
                try:
                    os.rename(deliver + "/" + file,  deliver + "/" + "Picture {0} (Batch {1}){2}".format(file_num, batch, TYPE))
                    file_num += 1
                except PermissionError:
                    print("Permission error on " + file)
                    pass

def get_batch_num():
    """Get's current batch number based on the batches.txt file.

    """
    batches_file = open(os.path.join(os.getcwd(), "batches.txt"), "r+")
    batches = batches_file.readlines()
    batch = int(batches[-1]) + 1
    for i in range(len(batches)):
        batches[i].strip("\n")
    if str(batch) in batches:
        batch += 1
    batches_file.write("\n" + str(batch))
    batches_file.close()
    return batch


def move_pics(src, dest):
    """Moves Pictures from one folder to another.

    No Docstrings since output depends on unrepresentable input.
    """
    deliver = DESTINATION
    batch = get_batch_num()
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        copy2(file_path, deliver)
    rename_files(deliver, batch, dest)

def check():
    d = DESTINATION
    for i in os.listdir(d):
        if i in os.listdir(d):
            n = os.stat(d+"/"+i).st_size
            for x in os.listdir(d):
                try:
                    if x != i:
                        m = os.stat(d+"/"+x).st_size
                        if m == n:
                            os.remove(d+"/"+x)
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass

    #f1 = open(image, 'r')
    #for i in dest:
        #f2 = open(i, 'r')
        #if f1.read() == f2.read():
            #f1.close()
            #f2.close()
            #os.remove(deliver + "\\" + image)
        #else:
            #f2.close()
    #f1.close()

def the_right_pics():
    deliver = DESTINATION
    for image in os.listdir(deliver):
        try:
            if not('.txt' in image or '.py' in image):
                x = imghdr.what(deliver + "/" + image)
                if x != "jpeg":
                    os.remove(deliver + "/" +image)
                else:
                    dimensions = get_image_size(deliver + "/" +image)
                    size = os.stat(deliver + "/" +image).st_size
                    if size < 100000:
                        os.remove(deliver + "/" + image)
                    elif dimensions == (1080, 1920):
                        os.remove(deliver + "/" + image)

        except PermissionError:
            pass
    check()


import struct
import imghdr

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return (width, height)





move_pics(find_path_to_pictures(), DESTINATION)
the_right_pics()
