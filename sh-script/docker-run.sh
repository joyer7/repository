#!/bin/bash

IMAGE=speechrec
CMD=bash

DIC_PATH=$HOME/study/aicenter_sr/volumes/dict
TRAIN_DATASET_PATH=$HOME/study/aicenter_sr/volumes/train_zeroth
TEST_DATASET_PATH=%HOME/studyaicenter_sr/volumes/rest_zeroth
LMTEXT_PATH=$/study/aicenter_sr/volumes/lm_text


nvidia-docker run -it -rm --shm-size=1g --ulimit memlock=-1 \
-v $DIC_PATH:/work/KaldiGMM/korean_script/s5/data/local/dict \s
-v $TRAIN_DATASET_PATH:/work/KaldiGMM/korean_script/s5/data/train_zeroth \
-v $TEST_DATASET_PATH:/work/KaldiGMM/korean_script/s5/data/test \
-v $LMTEXT_PATH:/work/KaldiGMM/korean_script/s5/data/lm_text \
$IMAGE $CMD

57

asdd
#====================
IMAGE=speechsyn
CMD=bash

FINANCE_DATASE_PATH=$HOME/study/aicenter_ss/volumes/finance
MODEL_PATH=$HOME/study/aicenter_ss/volumes/model

nvidia-docker run -it --rm --shm-size=1g --ulimit memlock=-1 \
-v $FINANCE_DATA_SET_PATH:/work/Tacotron2-Wavenet-Korean-TTS/datasets/finance \
-v #MODEL_PATH:/work/TKWGinfer/model \
$IMAGE $CMD
