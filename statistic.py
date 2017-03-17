# _*_ coding: utf-8 _*_
import os

from file_reader import load


def load(file_name, path):
    if file_name != '':
        source = path + "/" + file_name
    else:
        source = path

    if os.path.exists(source):
        f = open(source, 'rb')
        data = []
        for i in f:
            elem = []
            try:
                elem = i.decode('utf-8')
            except:
                try:
                    elem = i.decode('big5')
                except:
                    try:
                        elem = i.decode('x-windows-950')
                    except:
                        elem = i.decode('ISO-8859-1')
            # elem = elem.encode(encoding='utf-8')
            if len(elem) > 0:
                data.append(elem.replace('\n', '').replace(':', ',').split(','))

        f.close()
        return data
    else:
        print("This file doesn't exist.")


def load_all(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            filelist = os.listdir(path)
            filelist.sort()

            for f in filelist:
                    load_all(os.path.join(path, f))

        elif os.path.isfile(path):
            buffer = []

            if path.find('.ods') != -1:
                index = path.rfind('/')
                fileName = path[index + 1:]
                siteName = fileName[:fileName.index('_')]
                month = fileName[fileName.find('m')+1:fileName.rfind('_')]
                interval = fileName[fileName.rfind('e')+1:fileName.index('.')]
                print('site name: %s, month: %s, interval: %s' % (siteName, month, interval))
                buffer = load('', path)

                if not(siteName in sites):
                    sites[siteName] = dict()
                if not(month in sites[siteName]):
                    sites[siteName][month] = dict()
                sites[siteName][month][interval] = dict()
                sites[siteName][month][interval]['accuracy'] = buffer[2][1]
                sites[siteName][month][interval]['rmse'] = buffer[0][1]
                sites[siteName][month][interval]['recall'] = float(buffer[6][2]) / (
                    float(buffer[6][4]) + float(buffer[6][2])) if int(float(buffer[6][4]) + float(buffer[6][2])) != 0 else -1
                sites[siteName][month][interval]['precision'] = float(buffer[6][2]) / (
                    float(buffer[6][3]) + float(buffer[6][2])) if int(float(buffer[6][3]) + float(buffer[6][2])) != 0 else -1
                sites[siteName][month][interval]['f1'] = (2 * sites[siteName][month][interval]['precision'] *
                                                          sites[siteName][month][interval]['recall']) / (
                                                         sites[siteName][month][interval]['precision'] +
                                                         sites[siteName][month][interval]['recall']) if (
                                                         sites[siteName][month][interval]['precision'] +
                                                         sites[siteName][month][interval]['recall']) != 0 else -1

        else:
            print("Loading error.")

    else:
        print("This path doesn't exist.")


def ave(data, sites, months, hr, pred):
    value_ave = 0.
    total_num = 0
    for site in sites:
        if site in data:
            for month in months:
                if month in data[site]:
                    value_ave += data[site][month][hr][pred]
                    total_num += 1
    if total_num:
        return value_ave/total_num
    else:
        return -1

path = '/home/clliao/workspace/python/weather_prediction/rnn_regression/result'
sites = dict()
load_all(path)
print('Finish')

site_list = ['小港']  # ['中山', '古亭', '士林', '松山', '萬華']
month_list = ['1']  # ['1', '12']
hr = '1'
pred = 'precision'  # precision, recall, f1
print 'sites: ', site_list, ', months: ', month_list, ', hr: ', hr
print 'precision: ', ave(sites, site_list, month_list, hr, 'precision')
print 'recall: ', ave(sites, site_list, month_list, hr, 'recall')
print 'f1 score: ', ave(sites, site_list, month_list, hr, 'f1')
