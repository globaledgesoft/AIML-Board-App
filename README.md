## QDN AIML Board Application

To develop a machine learning model for object detection (Pedestrians, Cars, Motorbike, Bicycle, Bus)  which is supported by Snapdragon mobile platforms with the help of Neural Processing SDK.

The Machine learning model to detect the Objects uses Single Shot Detector(SSD) algorithm trained on Mobilenet network architecture.
Why MobilenetSSD 

1. Gives realtime inference frame rates 8-13 FPS on HDK835
2. Better perfomance and accuracy comapred to other architecutres like YOLO ... Etc,

How to train the model
Installation of MobilenetSSD and Caffe 

1. Clean the caffe source code from the below git repositry using below commands.

>$ git clone https://github.com/weiliu89/caffe.git

>$ cd caffe

>$ git checkout ssd

2. Depending on the Processor used eithe CPU or GPU install the depending packages by executing repective instrctions frm http://caffe.berkeleyvision.org/install_apt.html

3. Build caffe using the below instructions

 $ cp Makefile.config.example Makefile.config
Please disable the option USE_OPENCV. USE_OPENCV := 0
( Make necessary modification  in the Makefile as per the device configuration)
 $ make -j8
 $ make test
 $ make runtest
 $ make pycaffe
 ( Make sure you add the $CAFFE_ROOT/python to your PYTHON PATH once done with the make pycaffe command)



Getting the data ready

1. Download the VOC2007 and VOC2012 dataset.
```
$ mkdir home/<username>/data
$ cd home/<username>/data
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
$ tar -xvf VOCtrainval_11-May-2012.tar
$ tar -xvf VOCtrainval_06-Nov-2007.tar
$ tar -xvf VOCtest_06-Nov-2007.tar
```
3. Creating the Lightning Memory-Mapped Database
(LMDB) file
```
$ cd $CAFFE_ROOT
$ ./data/VOC0712/create_list.sh
$ ./data/VOC0712/create_data.sh
```



Training the model with VOC

Now clone the MobileNetSSD implementation by chuanqi305 from github

```
$ git clone https://github.com/chuanqi305/MobileNet-SSD.git
$ cd MobileNet-SSD

```

1. Creating the symbolic link to training and test data sets,
```
$ ln -s $CAFFE_DIR/PATH_TO_YOUR_TRAIN_LMDB trainval_lmdb
$ ln -s $CAFFE_DIR/PATH_TO_YOUR_TEST_LMDB test_lmdb
```
2. Copy a labelmap_voc.prototxt file from ssd repo tree to MobileNetSSD Dir using below command,
```
$ cp $CAFFE_DIR/data/VOC0712/labelmap_voc.prototxt $MOBILENETSSD_DIR/labelmap.prototxt
```

Run gen_model.sh for generating the training & testing prototxt with given number of classes. Please make sure that number of classes while running gen_model.sh & number of classes mentioned in labelmap.prototxt should match.
```
$ ./gen_model.sh 21
```

Now train your model using train.sh, and keep on training unless loss is in between 1.5 to 2.5.
```
$ ./train.sh
```

Test the trained model with test.sh script.
```
$ ./test.sh
```
Run merge_bn.py to generate your own no-bn caffemodel if necessary.
```
$ python merge_bn.py --model example/MobileNetSSD_deploy.prototxt --weights snapshot/mobilenet_iter_xxxxxx.caffemodel
```
once merge_bn.py has run successfully, You’ll get two files in the root directory of MobileNetSSD.
These are our trained models,

1. no_bn.prototxt
2. no_bn.caffemodel.

Run demo.py for checking the detection.


How to Convert caffe into DLC?

Prerequisites
 Neural Processing SDK setup. Use the isntruction in from the below link to make the setup,
https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk/getting-started

Initialized environmental variables of Neural Processing SDK with caffe.
For converting the model from caffe to dlc, you need 2 files,  prototxt and caffemodel file
Once you’ve both convert it into dlc using the following command:

$ snpe-caffe-to-dlc --caffe_txt MobileNetSSD_deploy.prototxt --caffe_bin MobileNetSSD_deploy.caffemodel --dlc caffe_mobilenet_ssd.dlc