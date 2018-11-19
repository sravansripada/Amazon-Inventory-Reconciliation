import numpy as np
from sklearn import svm
import random
import json
from matplotlib.image import imread;
import matplotlib.pyplot as plt;
import skimage.transform


# HELPER
def getTransformedMatrix(image):
    num_rows = image.shape[0]
    num_columns = image.shape[1]
    num_colors = image.shape[2]
    num_pixels =  num_rows*num_columns
    # scaled = image.reshape(num_pixels, num_colors)
    resized = skimage.transform.resize(image, (224,224,3))
    resizedReshaped = resized.reshape(1, 224 * 224 * 3)
    return resizedReshaped

def printShape(image, name):
    print("BEFORE: ", name, "= " , image.shape) # (128, 128, 3)
    rgb_matrix =  getTransformedMatrix(image).shape # (16384, 3)
    print("AFTER: ", name, "= " , rgb_matrix)

# RANDOM
random.seed(229)

# PATH
local_path = ''
sage_path = '/home/ec2-user/SageMaker/efs/amazon-bin/'
env_path = local_path

train_file = env_path+'counting_train.json'
# train_file = env_path+'/input/counting_train.json'

image_path = env_path+'data/Images/'
# img_path = env_path+'/data/bin-images-resize/'


# FILE
with open(train_file) as f:
    data_list = json.loads(f.read())
print("#files_train=", len(data_list))

sample_images = "data/Images/"
sample_meta = "data/Metadata/"
sample_name = "00001"
sample_image = imread(sample_images+sample_name+".jpg")
sample_transformed = getTransformedMatrix(sample_image)

# META
file_path = sample_meta+sample_name+".json"
with open(file_path) as metadata_file:
    metadata_json = json.load(metadata_file)
    expected_quantity = metadata_json["EXPECTED_QUANTITY"]
    print("EXPECTED_QUANTITY=",expected_quantity)
    # meta_list = metadata_json["BIN_FCSKU_DATA"]
    # for meta_key in meta_list:
    #     meta_data = meta_list[meta_key]
    #     print(meta_data["quantity"])


# plt.imshow(sample_image)
# plt.show()

# CONCATENATED
A = sample_transformed
X_A = np.concatenate((A, sample_transformed))
print("X_A=", X_A.shape)

# SVM
X = [[0, 0], [1, 1]]
y = [0, 1]

clf = svm.SVC(gamma='scale')
clf.fit(X, y)

print("predict=", clf.predict([[2., 2.]]))


