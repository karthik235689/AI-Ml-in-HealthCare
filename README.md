# AI-Ml-in-HeathCare
> Be **Aware** Be **Precautious** Be **Safe**

## Overview of the project
Enitre Projects is divided into three main parts :
* Admin Page for the laboratory Employees.
* DHC Page (Digital Health Card).
* Ayushman Bharat Web page.

## DHC Page
DHC - Digital Health Card is a unique health ID provided to every citizen to access halthcare services and their personal health records.This is linked with the adhar card, it is a Unique Identification numbers (UID).In this webpage 

## Ayushman Bharat Web page
Ayushman Bharat is a web page where each and every citizen can login with their DHC card and access their personal health records each and every time needed.It would be easier task than to carry health records each and everytime during the doctor appointment.The other use case is that they can book their appointment for the lab and also with the doctor and this web page helps in digitilizing the prescription by the doctor and also doctor can schedule next appointment id needed.

## Admin Page for the laboratory Employees.
This page is lab employees to update the records of the patients with their repective DHC Card number and their details.Here we us the AI for predecting the diseases and the AI prediction result will also be sent to the Ayushman Bharat Web Page and doctor can look into it and anaylse the result.NOTE:Now presently only covid detection is being implemented as a AI prediction but in the future more AI algorithims can be integrated.

## Overview of the Covid 19 
![header](https://user-images.githubusercontent.com/53186985/174720673-6fdace2d-638c-4aa4-a243-f32212c19c9a.png)

COVID-19 is five times as lethal as the flu, causing considerable morbidity and mortality. COVID-19 pulmonary infection, like other pneumonias, causes inflammation and fluid in the lungs. COVID-19 appears on chest radiographs to be highly similar to other viral and bacterial pneumonias, making diagnosis difficult. Our Deeplearning models for detecting and localising COVID-19 might aid clinicians in making an accurate and timely diagnosis. As a result, patients may be able to receive the appropriate medication before the virus's most serious effects manifest.

## 1.Installation of the Project procedure.
* HARDWARE: Basic Computer to work with deep learning models and GPU'S (optional but our code can also utilize GPU for faster training and testing).
* Python : Latest Current Stable version of python.
* Python packages are detailed separately in requirements.
* MySql 

```
Requirements Installation.
$ pip install -r requirements.txt
```
```
MySql Installation.
Link : 
``` 

## 2.DATASET
#### 2.1 SIIM COVID 19 DATASET
- download competition dataset at [link](https://www.kaggle.com/c/siim-covid19-detection/data) then extract to ./dataset/siim-covid19-detection

## 4.TRAIN MODEL
### 4.1 Classification
#### 4.1.1 Multi head classification + segmentation
- Stage1
```
$ cd src/classification_aux
$ bash train_chexpert_chest14.sh              #Pretrain backbone on chexpert + chest14
$ bash train_rsnapneu.sh                      #Pretrain rsna_pneumonia
$ bash train_siim.sh                          #Train siim covid19
```
- Stage2: Generate soft-label for classification head and mask for segmentation head.\
  Output: soft-label in ./pseudo_csv/[source].csv and public test masks in ./prediction_mask/public_test/masks
```
$ bash generate_pseudo_label.sh [checkpoints_dir]
```
- Stage3: Train model on trainset + public testset, load checkpoint from previous round
```
$ bash train_pseudo.sh [previous_checkpoints_dir] [new_checkpoints_dir]
```
Rounds of pseudo labeling (stage2) and retraining (stage3) were repeated until the score on public LB didn't improve.
- For final checkpoints
```
$ bash generate_pseudo_label.sh checkpoints_v3
$ bash train_pseudo.sh checkpoints_v3 checkpoints_v4
```
- For evaluation
```
$ CUDA_VISIBLE_DEVICES=0 python evaluate.py --cfg configs/xxx.yaml --num_tta xxx
```
mAP@0.5 4 classes: negative, typical, indeterminate, atypical
|              | [SeR152-Unet](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/classification-timm-seresnet152d_320_512_unet_aux.zip) | [EB5-Deeplab](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/classification-timm-efficientnet-b5_512_deeplabv3plus_aux.zip) | [EB6-Linknet](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/classification-timm-efficientnet-b6_448_linknet_aux.zip) | [EB7-Unet++](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/classification-timm-efficientnet-b7_512_unetplusplus_aux.zip)  | Ensemble    |
| :----------- | :---------- | :---------- | :---------- | :---------- | :---------- |
| w/o TTA/8TTA | 0.575/0.584 | 0.583/0.592 | 0.580/0.587 | 0.589/0.595 | 0.595/0.598 |

*<sub>8TTA: (orig, center-crop 80%)x(None, hflip, vflip, hflip & vflip). In [final submission](https://www.kaggle.com/nguyenbadung/siim-covid19-2021), I use 4.1.2 lung detector instead of center-crop 80%<sub>*

#### 4.1.2 [Lung Detector-YoloV5](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/detection_yolov5_lung.zip)
I annotated the train data(6334 images) using [LabelImg](https://github.com/tzutalin/labelImg) and built a lung localizer. I noticed that increasing input image size improves the modeling performance and lung detector helps the model to reduce background noise.
```
$ cd src/detection_lung_yolov5
$ cd weights && bash download_coco_weights.sh && cd ..
$ bash train.sh
```
|              | Fold0 | Fold1 | Fold2 | Fold3 | Fold4 | Average |
| :----------- | :---- | :---- | :---- | :---- | :---- | :------ |
| mAP@0.5:0.95 | 0.921 | 0.931 | 0.926 | 0.923 | 0.922 | 0.9246  |
| mAP@0.5      | 0.997 | 0.998 | 0.997 | 0.996 | 0.998 | 0.9972  |

### 4.2 Opacity Detection
Rounds of pseudo labeling (stage2) and retraining (stage3) were repeated until the score on public LB didn't improve.
#### 4.2.1 YoloV5x6 768
- Stage1:
```
$ cd src/detection_yolov5
$ cd weights && bash download_coco_weights.sh && cd ..
$ bash train_rsnapneu.sh          #pretrain with rsna_pneumonia
$ bash train_siim.sh              #train with siim covid19 dataset, load rsna_pneumonia checkpoint
```
- Stage2: Generate pseudo label (boxes)
```
$ bash generate_pseudo_label.sh
```
Jump to step 4.2.4 Ensembling + Pseudo labeling
- Stage3:
```
$ bash warmup_ext_dataset.sh      #train with pseudo labeling (public-test, padchest, pneumothorax, vin) + rsna_pneumonia
$ bash train_final.sh             #train siim covid19 boxes, load warmup checkpoint
```
#### 4.2.2 EfficientDet D7 768
- Stage1:
```
$ cd src/detection_efffdet
$ bash train_rsnapneu.sh          #pretrain with rsna_pneumonia
$ bash train_siim.sh              #train with siim covid19 dataset, load rsna_pneumonia checkpoint
```
- Stage2: Generate pseudo label (boxes)
```
$ bash generate_pseudo_label.sh
```
Jump to step 4.2.4 Ensembling + Pseudo labeling
- Stage3:
```
$ bash warmup_ext_dataset.sh      #train with pseudo labeling (public-test, padchest, pneumothorax, vin) + rsna_pneumonia
$ bash train_final.sh             #train siim covid19, load warmup checkpoint
```
#### 4.2.3 FasterRCNN FPN 768 & 1024
- Stage1: train backbone of model with chexpert + chest14 -> train model with rsna pneummonia -> train model with siim, load rsna pneumonia checkpoint
```
$ cd src/detection_fasterrcnn
$ CUDA_VISIBLE_DEVICES=0,1,2,3 python train_chexpert_chest14.py --steps 0 1 --cfg configs/resnet200d.yaml
$ CUDA_VISIBLE_DEVICES=0,1,2,3 python train_chexpert_chest14.py --steps 0 1 --cfg configs/resnet101d.yaml
$ CUDA_VISIBLE_DEVICES=0 python train_rsnapneu.py --cfg configs/resnet200d.yaml
$ CUDA_VISIBLE_DEVICES=0 python train_rsnapneu.py --cfg configs/resnet101d.yaml
$ CUDA_VISIBLE_DEVICES=0 python train_siim.py --cfg configs/resnet200d.yaml --folds 0 1 2 3 4 --SEED 123
$ CUDA_VISIBLE_DEVICES=0 python train_siim.py --cfg configs/resnet101d.yaml --folds 0 1 2 3 4 --SEED 123
```
*<sub>Note: Change SEED if training script runs into issue related to augmentation (boundingbox area=0) and comment/uncomment the following code if training script runs into issue related to resource limit<sub>*
```python
import resource
rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (8192, rlimit[1]))
```
- Stage2: Generate pseudo label (boxes)
```
$ bash generate_pseudo_label.sh
```
Jump to step 4.2.4 Ensembling + Pseudo labeling
- Stage3:
```
$ CUDA_VISIBLE_DEVICES=0 python warmup_ext_dataset.py --cfg configs/resnet200d.yaml
$ CUDA_VISIBLE_DEVICES=0 python warmup_ext_dataset.py --cfg configs/resnet101d.yaml
$ CUDA_VISIBLE_DEVICES=0 python train_final.py --cfg configs/resnet200d.yaml
$ CUDA_VISIBLE_DEVICES=0 python train_final.py --cfg configs/resnet101d.yaml
```
#### 4.2.4 Ensembling + Pseudo labeling
Keep images that meet the conditions: negative prediction < 0.3 and maximum of (typical, indeterminate, atypical) predicion > 0.7. Then choose 2 boxes with the highest confidence as pseudo labels for each image.

*<sub>Note: This step requires at least 128 GB of RAM <sub>*
```
$ cd ./src/detection_make_pseudo
$ python make_pseudo.py
$ python make_annotation.py            
```

#### 4.2.5 Detection Performance
|                  | [YoloV5x6 768](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/detection_yolov5.zip) | [EffdetD7 768](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/detection_efficientdet.zip) | [F-RCNN R200 768](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/detection_fasterrcnn_resnet200d_768.zip) | [F-RCNN R101 1024](https://github.com/dungnb1333/SIIM-COVID19-Detection/releases/download/v0.1/detection_fasterrcnn_resnet101d_1024.zip) |
| :--------------- | :----------- | :----------- | :-------------- | :--------------- |
| mAP@0.5 TTA      | 0.580        | 0.594        | 0.592           | 0.596            |

## 5.FINAL SUBMISSION
[siim-covid19-2021](https://www.kaggle.com/nguyenbadung/siim-covid19-2021?scriptVersionId=69474844) Public LB: 0.658 / Private LB: 0.635\
[demo notebook](https://github.com/dungnb1333/SIIM-COVID19-Detection/blob/main/src/demo_notebook/demo.ipynb) to visualize output of models

## 6.AWESOME RESOURCES
[Pytorch](https://github.com/pytorch/pytorch)✨\
[PyTorch Image Models](https://github.com/rwightman/pytorch-image-models)✨\
[Segmentation models](https://github.com/qubvel/segmentation_models.pytorch)✨\
[EfficientDet](https://github.com/rwightman/efficientdet-pytorch)✨\
[YoloV5](https://github.com/ultralytics/yolov5)✨\
[FasterRCNN FPN](https://github.com/pytorch/vision/tree/master/torchvision/models/detection)✨\
[Albumentations](https://github.com/albumentations-team/albumentations)✨\
[Weighted boxes fusion](https://github.com/ZFTurbo/Weighted-Boxes-Fusion)✨

