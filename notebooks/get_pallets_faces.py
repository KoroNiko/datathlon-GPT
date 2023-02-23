# !pip install ipywidgets
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests

from collections import Counter
# from environment.settings import config
from matplotlib import colors
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from typing import Tuple

from tqdm import tqdm
from multiprocessing import Pool
import pickle

import sys
sys.path.append("/home/stratos/Documents/datathlon-GPT-main")

# dataset_dir = config['DATASET_DIR']
dataset_dir='./data/'


# Number of colors to be extracted
NUM_COLORS = 10

with open(dataset_dir+'pickle_portraits', 'rb') as handle:
    image_list = pickle.load(handle)

def extract_colors(model: KMeans, img: np.ndarray) -> Tuple[np.ndarray, Counter, np.ndarray]:
    ''' Extract the X most common colors from an image with a KMeans model '''
    if len(img.shape)==3:
        img2d = img.reshape((img.shape[0]*img.shape[1],3))
    else:
        img2d = np.stack((img,img,img),axis=2).reshape(img.shape[0]*img.shape[1],3)
    cluster_labels = model.fit_predict(img2d)
    return cluster_labels, Counter(cluster_labels), model.cluster_centers_.astype(int)

def get_img_pallete(ids_and_urls):
    img_id = ids_and_urls[0]
    img = ids_and_urls[1]
    kmeans_model = KMeans(n_clusters=NUM_COLORS, n_init='auto')

    cluster_labels, cluster_counts, rgb_colors = extract_colors(kmeans_model, img)
    # img_quant = np.reshape(rgb_colors[cluster_labels], (img.shape[0], img.shape[1], 3))

    return {
        'id':img_id,
        'cluster_counts':cluster_counts,
        'rgb_colors':rgb_colors
    }

result = []
test_bar = tqdm(total=len(image_list))

iterator = map(get_img_pallete, image_list)
while True:
    test_bar.update()
    try:
        result.append(next(iterator))
    except StopIteration:
        break
    except Exception as e:
        print('Error at iteration', len(result))
        print(e)

with open(dataset_dir+'img_pallets_faces.pkl', 'wb') as handle:
    pickle.dump(result, handle)
