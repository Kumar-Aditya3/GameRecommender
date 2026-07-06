import numpy as np
from preprocessing import tag_encoding
X = np.array(tag_encoding())
print(X.shape)
def