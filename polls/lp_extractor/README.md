# License plate extractor
## Quick start
### Create new model
```
from lp_extractor.model import LPExtractorModel

extractor = LPExtractorModel()
```
### Extract plate from image
```
img_path = "data_plate/0000_00532_b.jpg"
lp = extractor.extractLP(img_path)
```
### Train recognizer
```
python train_recognizer.py
```