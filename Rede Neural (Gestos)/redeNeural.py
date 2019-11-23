from __future__ import print_function

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import os
    # Import caso esse arquivo seja importado
    from keras.models import load_model
    import yaml
    #Setando Warnings de 'deprecation' off
    yaml.warnings({'YAMLLoadWarning': False})
    import tensorflow as tf
    #Setando Warnings de 'deprecation' off
    tf.logging.set_verbosity(tf.logging.ERROR)
    import placeholder
    import sys
    import time 
    import pickle
    import traceback
    import pandas as pd
    import numpy as np
    import scipy.misc
    import scipy.io.wavfile
    from sklearn.preprocessing import LabelEncoder
    from importlib.machinery import SourceFileLoader
    from multiprocessing import cpu_count

os.environ["MKL_NUM_THREADS"] = str(cpu_count())

def doResize(options):
    resize = None
    if options and 'Resize' in options and options['Resize'] == True:
        resize = (int(options['Width']), int(options['Height']))
    return resize


def col_pre_process(data, options):
    if len(options.keys()) == 0:
        return data
    else:
        if "pretrained" in options and options["pretrained"] != 'None':
            from keras.applications import inception_v3, vgg16, vgg19, resnet50
            if options["pretrained"] == 'InceptionV3':
                data = inception_v3.preprocess_input(data)
            elif options["pretrained"] == 'ResNet50':
                data = resnet50.preprocess_input(data)
            elif options["pretrained"] == 'VGG16':
                data = vgg16.preprocess_input(data)
            elif options["pretrained"] == 'VGG19':
                data = vgg19.preprocess_input(data)

        if "Scaling" in options and float(options["Scaling"]) != 0 and float(options["Scaling"]) != 1:
            data = data / float(options["Scaling"])

        if 'Normalization' in options and options['Normalization'] == True:
            mean = np.mean(data)
            std = np.std(data)
            data = data - mean
            data = data / std
            return data
        return data


def process_test_input(base_dir, test_raw, data_mapping):
    test_data = []
    le = None

    from keras import backend as K
    if K.backend() == 'theano' or K.backend() == 'mxnet':
        K.set_image_dim_ordering('th')
    else:
        K.set_image_dim_ordering('tf')

   
    for i in range(len(data_mapping['inputs'])):
        inp_port = data_mapping['inputs']['InputPort' + str(i)]
        if inp_port['details'][0]['type'] == 'Numpy':
            if 'options' in inp_port['details'][0]:
                options = inp_port['details'][0]['options']
            else:
                options = {}

            col_name = inp_port['details'][0]['name']
            npzFile = np.load(base_dir + "/" + test_raw[col_name][0])
            x = npzFile[npzFile.files[0]]
            input_shape = x.shape

            test_data.append(np.ndarray(
                (len(test_raw),) + x.shape, dtype=np.float32))
            for j, filename in enumerate(test_raw[col_name]):
                npzFile = np.load(base_dir + "/" + filename)
                x = npzFile[npzFile.files[0]]
                test_data[i][j] = x
            test_data[i] = col_pre_process(test_data[i], options)

        else:
            col_idx = 0
            test_data.append(np.ndarray(
                (len(test_raw), inp_port['size']), dtype=np.float32))
            for col in range(len(inp_port['details'])):
                if 'options' in inp_port['details'][col]:
                    options = inp_port['details'][col]['options']
                else:
                    options = {}

                col_name = inp_port['details'][col]['name']

                if inp_port['details'][col]['type'] == 'Categorical':
                    data_col = test_raw[col_name]
                    num_categories = len(
                        inp_port['details'][col]['categories'])

                    le_temp = LabelEncoder()
                    le_temp.fit(inp_port['details'][col]['categories'])
                    data_col = le_temp.transform(data_col)

                    one_hot_array = np.zeros(
                        (len(data_col), num_categories), dtype=np.float32)
                    one_hot_array[np.arange(len(data_col)), data_col] = 1

                    test_data[i][:, col_idx:col_idx +
                                 num_categories] = col_pre_process(one_hot_array, options)
                    col_idx += num_categories

                else:
                    data = test_raw[col_name].reshape((len(test_raw), 1))
                    test_data[i][:, col_idx:col_idx +
                                 1] = col_pre_process(data, options)
                    col_idx += 1

    
    out_port = data_mapping['outputs']['OutputPort0']
    if out_port['details'][0]['type'] == 'Categorical':
        le = LabelEncoder()
        le.fit(out_port['details'][0]['categories'])

    return test_data, le


def customPredict(test_data, config, modelFile):
    res = None
    loss_func = config['params']['loss_func']
    if 'is_custom_loss' in config['params']:
        isCustomLoss = config['params']['is_custom_loss']
    else:
        isCustomLoss = False

    if isCustomLoss:
        customLoss = SourceFileLoader(
            "customLoss", 'customLoss.py').load_module()
        loss_function = eval('customLoss.' + loss_func)
        mod = load_model(modelFile, custom_objects={loss_func: loss_function})
    else:
        mod = load_model(modelFile)
    
           
    return mod.predict(test_data)


def test_model(input_file):

    try:
        if os.path.exists('model.h5') and os.path.exists('mapping.pkl'):

            with open('mapping.pkl', 'rb') as f:
                data_mapping = pickle.load(f)

            test_raw = pd.read_csv(input_file)

            test_data, le = process_test_input(
                os.path.dirname(input_file), test_raw, data_mapping)

            currentDir = os.getcwd()

            with open('config.yaml', 'r') as f:
                config = yaml.load(f)
                models = []
                if "kfold" in config["data"] and config["data"]["kfold"] > 1:
                    kfold = config["data"]["kfold"]

                    if os.path.exists('model.h5'):
                        models.append(currentDir + '/model.h5')
                    else:
                        for sub_run in range(1, kfold + 1):
                            sub_dir = currentDir + str(sub_run)
                            if os.path.exists(sub_dir + "/model.h5"):
                                models.append(sub_dir + "/model.h5")
                else:
                    models.append(currentDir + '/model.h5')

            result = np.array([])
            for modelFile in models:
                res = customPredict(test_data, config, modelFile)
                if result.size != 0:
                    result = res + result
                else:
                    result = res

            res = result / len(models)

            out_type = data_mapping['outputs']['OutputPort0']['details'][0]['type']

            num_samples = len(test_raw)
            if num_samples != 0:
                out_dir = "./"      
                if out_type == 'Categorical' and le != None:
                    res_prob = np.round(
                        np.max(res, axis=1).astype(float), decimals=4)
                    res_id = np.argmax(res, axis=1)
                    res1 = le.inverse_transform(res_id.tolist())
                    test_raw['predicao'] = res1
                    test_raw['probabilidade'] = res_prob
                    print("Predicao: ",res1)
                    print("Probabilidade:", res_prob)
                    

                test_raw.to_csv('Resultado.csv', index=False)
                
        else:
            print('O arquivo model.h5 ou o mapping.pkl não foi encontrado!')

    except Exception as e:
        print("Ocorreu um erro... Verifique o formato da entrada inserida!")
        traceback.print_exc()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Chamada incorreta: \"python [nome_arquivo_rede] [lista_numpy].csv\"")
    else:

        from keras.models import load_model

        print("O output sera colocado em \'./output/\'\n")
        test_model(sys.argv[1])
