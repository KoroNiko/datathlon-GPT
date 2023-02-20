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
Artwork = pd.read_csv(dataset_dir+'Artwork.csv')


def i1():# helper function for fork printing
  sys.stdout.write(' ')
  sys.stdout.flush()

def url2array(url: str):
    ''' Gets a URL and returns an image as a numpy array '''
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return np.array(img)

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
    img_url = ids_and_urls[1]
    img = url2array(img_url)
    kmeans_model = KMeans(n_clusters=NUM_COLORS, n_init='auto')

    cluster_labels, cluster_counts, rgb_colors = extract_colors(kmeans_model, img)
    # img_quant = np.reshape(rgb_colors[cluster_labels], (img.shape[0], img.shape[1], 3))

    return {
        'id':img_id,
        'cluster_labels':cluster_labels,
        'rgb_colors':rgb_colors
    }

result = []
test_bar = tqdm(total=len(Artwork['id']))
i=1
with Pool(processes=2, initializer=i1) as pool:
    iterator = pool.imap(get_img_pallete, list(Artwork[['id','image_url']].itertuples(index=False, name=None)))
    while True:
        if len(result)==1000:
            with open('/media/stratos/New Volume/'+'img_pallets_'+str(i)+'.pkl', 'wb') as handle:
                pickle.dump(result, handle)
                result = []
                i+=1
        test_bar.update()
        try:
            result.append(next(iterator))
        except StopIteration:
            break
        except Exception as e:
            print('Error at iteration', len(result))
            print(e)

# with open('/media/stratos/New Volume/'+'img_pallets_all.pkl', 'wb') as handle:
#     pickle.dump(result, handle)
