from analyze_labels import analyse_ubicoustics_labels

import glob
from natsort import natsorted,ns
import pandas as pd

def create_data_from_ubicoustics():
	(hammer_splits,saw_splits) = analyse_ubicoustics_labels()
	filelist = natsorted(glob.glob("*_features.csv"))
	hammer = open("hammer.csv","w+")
	hammer.write("split_id,mfcc_0,mfcc_1,mfcc_2,mfcc_3,mfcc_4,mfcc_5,mfcc_6,mfcc_7,mfcc_8,mfcc_9,mfcc_10,mfcc_11,mfcc_12,mfcc_13,mfcc_14,mfcc_15,mfcc_16,mfcc_17,mfcc_18,mfcc_19,tonnetz_0,tonnetz_1,tonnetz_2,tonnetz_3,tonnetz_4,tonnetz_5,specent_0,specent_1,specent_2,specent_3,specent_4,specent_5,specent_6,specent_7,specent_8,specent_9,specent_10,specent_11,specent_12,specent_13,specent_14,specent_15,specent_16,specent_17,specent_18,specent_19,specontrast_0,specontrast_1,specontrast_2,specontrast_3,specontrast_4,specontrast_5,specontrast_6,user\n")
	saw = open("saw.csv","w+")
	saw.write("split_id,mfcc_0,mfcc_1,mfcc_2,mfcc_3,mfcc_4,mfcc_5,mfcc_6,mfcc_7,mfcc_8,mfcc_9,mfcc_10,mfcc_11,mfcc_12,mfcc_13,mfcc_14,mfcc_15,mfcc_16,mfcc_17,mfcc_18,mfcc_19,tonnetz_0,tonnetz_1,tonnetz_2,tonnetz_3,tonnetz_4,tonnetz_5,specent_0,specent_1,specent_2,specent_3,specent_4,specent_5,specent_6,specent_7,specent_8,specent_9,specent_10,specent_11,specent_12,specent_13,specent_14,specent_15,specent_16,specent_17,specent_18,specent_19,specontrast_0,specontrast_1,specontrast_2,specontrast_3,specontrast_4,specontrast_5,specontrast_6,user\n")
	for files in filelist:
		in_file = pd.read_csv(files)
		user_id = files.split("/")[-1].split(".")[0].split("_")[0]
		print(user_id)
		for i in range(len(in_file['split_id'])):
			split_id = in_file['split_id'][i]
			print(split_id)
			if(split_id in hammer_splits):
				string=split_id+","
				for j in in_file.columns[1:]:
					string+=str(in_file[j][i])+","
				hammer.write(string+user_id.strip("U")+"\n")
			elif(split_id in saw_splits):
				string=split_id+","
				for j in in_file.columns[1:]:
					string+=str(in_file[j][i])+","
				saw.write(string+user_id.strip("U")+"\n")			

	hammer.flush()
	saw.flush()

	hammer.close()
	saw.close()

def main():
	create_data_from_ubicoustics()

if __name__ == '__main__':
	main()