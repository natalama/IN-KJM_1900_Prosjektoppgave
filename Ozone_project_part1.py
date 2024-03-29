import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import matplotlib.dates as mdates


def get_concentration_grouped_by_date_time(filename):
    dict_date_time_conc = {} #dictionary to group by date and time
    data_lines = np.loadtxt(filename, dtype='int,int,float,float', skiprows=1) # read file, with date and time as int, and the rest as float
    for data_line in data_lines:
        date = str(data_line[0])[6:]
        time = str(data_line[1]).rjust(2, '0')

        # extract the last 4 numbers, then multiply by 100 to add two zeroes to the right, and add time.
        # the result will be 122612 for instance. it corresponds to 26th of december, 12pm
        month_day_time = date+"."+ time
        if month_day_time not in dict_date_time_conc:
            dict_date_time_conc[month_day_time] = [] # initialize a new array if the month, day, and time isn't on the dictionary yet
        dict_date_time_conc[month_day_time].append(data_line[2]) # append concentration to dictionary
    return dict_date_time_conc #return the dictionary, of course


def find_mean(data_set):
    return  sum(data_set)/len(data_set)


# use this method if we don't have the mean yet
def find_standard_deviation(data_set):
    mean = find_mean(data_set) # just find the mean once, it will be used many times
    variance = sum((data - mean) ** 2 for data in data_set) / len(data_set)
    std_dev = np.sqrt(variance)
    return std_dev


# returns the mean and standard deviation for a set of data, based on the file name
def find_statistics(filename):
    data_set = get_concentration_grouped_by_date_time(filename)
    days_and_times = []
    means = []
    std_devs = []
    for key in data_set.keys():
        concentrations = data_set[key]
        days_and_times.append(key)
        means.append(find_mean(np.array(concentrations)))
        std_devs.append(find_standard_deviation(np.array(concentrations)))
    return days_and_times, means, std_devs


sept_date_time, sept_means, sept_std_devs = find_statistics('sept.txt')
dec_date_time, dec_means, dec_std_devs = find_statistics('dec.txt')

# plot months against average concentration with standard deviation
# I just find the color "baby poop green" funny. :)
plt.errorbar(sept_date_time, sept_means, sept_std_devs, color = 'xkcd:baby poop green', label = "September")
plt.errorbar(dec_date_time, dec_means, dec_std_devs, color = 'xkcd:eggplant purple', label = "December")
axis = plt.gca()
axis.xaxis.set_major_locator(plt.MaxNLocator(8.4))
# axis.xaxis.set_major_formatter()
#main title here
plt.suptitle("Konsentrasjon mot dato med standardavvik")
plt.legend()
plt.show()
