# Copyright (c) 2016-present, Facebook, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

## @package lmdb_create_example
# Module caffe2.python.examples.lmdb_create_example
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import random
import numpy as np
import lmdb
from scipy.misc import imresize
import cv2
from caffe2.proto import caffe2_pb2
from caffe2.python import workspace, model_helper


def crop_center(img, new_height, new_width):
    orig_height, orig_width, _ = img.shape
    startx = (orig_width//2) - (new_width//2)
    starty = (orig_height//2) - (new_height//2)
    return img[starty:starty+new_height, startx:startx+new_width]




# handle command line arguments
parser = argparse.ArgumentParser(description='Converts a directory of images to an LMDB using a label file')
parser.add_argument('--labels', help='path to labels file', required=True)
parser.add_argument('--output', help='name of output lmdb', required=True)
parser.add_argument('--shuffle', action='store_true', help='if set, data is shuffled before going conversion', required=False)
parser.add_argument('--height', help='desired image height', required=True)
parser.add_argument('--width', help='desired image width', required=True)
parser.add_argument('--horizontal_flip', action='store_true', help='if set, add horizontally flipped images to lmdb', required=False)
parser.add_argument('--permutations', help='number of random permutations', required=False)
args = vars(parser.parse_args())


label_file = args['labels']
output = args['output']
shuffle = args['shuffle']
desired_h = args['height']
desired_w = args['width']
horizontal_flip = args['horizontal_flip']
permutations = args['permutations']


# Read labels file into list (for shuffling purposes)
with open(label_file) as f:
    content = f.readlines()
content = [x.rstrip() for x in content]
if (shuffle):
    random.shuffle(content)


print(">>> Write database...")
LMDB_MAP_SIZE = 1 << 40   # MODIFY: just a very large number
print("LMDB_MAP_SIZE", LMDB_MAP_SIZE)
env = lmdb.open(output, map_size=LMDB_MAP_SIZE)


with env.begin(write=True) as txn:

    def create_tensorprotos(img_data, label, index):
        # Create TensorProtos
        tensor_protos = caffe2_pb2.TensorProtos()
        img_tensor = tensor_protos.protos.add()
        img_tensor.dims.extend(img_data.shape)
        img_tensor.data_type = 1
        flatten_img = img_data.reshape(np.prod(img_data.shape))
        img_tensor.float_data.extend(flatten_img)
        label_tensor = tensor_protos.protos.add()
        label_tensor.data_type = 2
        label_tensor.int32_data.append(label)
        txn.put(
            '{}'.format(index).encode('ascii'),
            tensor_protos.SerializeToString()
        )
        if ((index % 100 == 0)):
            print("Inserted {} rows".format(index))
        index = index + 1
        return index


    count = 0
    for line in content:
        img_file = line.split()[0]
        label = int(line.split()[1])
        img_data = cv2.imread(img_file)

        # ensure that grayscale images get 3 dimensions
        # if (img_data.ndim < 3):
        #    img_data = np.expand_dims(img_data, axis=0)

        # resize image as desired
        h, w, _ = img_data.shape

        if (h < int(desired_h) or w < int(desired_w)):
            img_data = imresize(img_data, (int(desired_h), int(desired_w)))
        else:
            img_data = crop_center(img_data, int(desired_h), int(desired_w))

        if ((img_data[:,:,0] == img_data[:,:,1]).all() and (img_data[:,:,0] == img_data[:,:,2]).all()):
            img_data = img_data[:,:,0]
            img_data = np.expand_dims(img_data, axis=2)

        img_for_lmdb = np.transpose(img_data, (2,0,1))

        # insert correctly sized image
        count = create_tensorprotos(img_data,label,count)

        # insert horizontally flipped version if flag was set
        if (horizontal_flip):
            count = create_tensorprotos(np.fliplr(img_data), label, count)

        #if (permutations):



print("Inserted {} rows".format(count))
print("\nLMDB saved at " + output)
