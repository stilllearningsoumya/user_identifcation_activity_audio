import glob
import librosa
from natsort import natsorted
import numpy as np
from scipy.io import wavfile

def main():
	user_id = input("Please enter the user id: ")
	if(user_id==""):
		return
	split_files = natsorted(glob.glob("audio_splits/"+user_id+"_*.wav"))
	out_file = open(user_id+"_features.csv","w+")
	#print(split_files)	
	
	#creating the headers
	string = "split_id"
	for i in range(20):
		string+=",mfcc_"+str(i)
	for i in range(6):
		string+=",tonnetz_"+str(i)
	for i in range(20):
		string+=",specent_"+str(i)
	for i in range(7):
		string+=",specontrast_"+str(i)

	out_file.write(string+"\n")

	for files in split_files:
		filename = files.split("/")[-1].split(".")[0]
		print(filename)
		out_file.write(filename)
		string = ""
		signal, fs = librosa.load(files)

		#extract MFCC features
		m = librosa.feature.mfcc(y=signal,sr=fs)
		m = m.transpose()
		m = np.mean(m,axis=0) #Mean of all coefficients across bins

		assert len(m) == 20

		for elems in m:
			string+=","+str(elems)

		#extract tonal centroid features
		t = librosa.feature.tonnetz(y=signal,sr=fs)
		t = t.transpose()
		t = np.mean(t,axis=0)

		assert len(t) == 6

		for elems in t:
			string+=","+str(elems)

		#extract spectral cenroid will consider top-20 only
		cent = librosa.feature.spectral_centroid(y=signal,sr=fs)
		cent = cent[0][:20]

		for elems in cent:
			string+=","+str(elems)

		#extract spectral contrast features
		cont = librosa.feature.spectral_contrast(y=signal,sr=fs)
		cont = cont.transpose()
		cont = np.mean(cont,axis=0)

		assert len(cont) == 7

		for elems in cont:
			string+=","+str(elems)	

		out_file.write(string+"\n")
		out_file.flush()

	out_file.close()

if __name__ == '__main__':
	main()
