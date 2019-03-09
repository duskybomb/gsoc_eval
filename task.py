import h5py, pytz, csv, numpy
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
from scipy.signal import medfilt


FILENAME = '1541962108935000000_167_838.h5'
CERN_TIMEZONE = timezone('Europe/Zurich')
UNIXTIME = FILENAME[:18]

def task_1_time():
    utc = pytz.utc
    utc_dt = utc.localize(datetime.utcfromtimestamp(int(UNIXTIME)/100000000))
    cern_dt = utc_dt.astimezone(CERN_TIMEZONE)
    print('UTC datetime: ', utc_dt, '\nCERN datetime: ', cern_dt)

def task_2_csv():
    f = h5py.File(FILENAME, 'r')

    csv_data = []
    def getData(name, obj):
        if isinstance(obj, h5py.Dataset):
            try:
                csv_data.append([name, obj.size, obj.shape, obj.dtype, 'Dataset'])
            except TypeError: # There are a few data type for which h5py does not have a type
                csv_data.append([name, obj.size, obj.shape, None, 'Dataset'])
        elif isinstance(obj, h5py.Group):
            csv_data.append([name, None, None, None, 'Group'])
    f.visititems(getData)

    with open("%s.csv" % str(UNIXTIME), "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'size', 'shape', 'dtype', 'type'])
        writer.writerows(csv_data)
    f.close()

def task_3_img():
    f = h5py.File(FILENAME, 'r')

    dataset = 'AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'
    dataset_height = 'AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'
    dataset_width = 'AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'

    dataset_2d = f[dataset][()].reshape(f[dataset_height][0], f[dataset_width][0])
    filtered_img = medfilt(dataset_2d)
    plt.imshow(filtered_img)
    plt.savefig("%s.png" % str(UNIXTIME))
    # plt.show()
    f.close()

if __name__ == "__main__":
    task_1_time()
    task_2_csv()
    task_3_img()