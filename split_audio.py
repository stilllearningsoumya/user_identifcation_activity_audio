from scipy.io import wavfile

list_of_users = ['U1','U2','U3','U4','U5']

def split_audio(user):
	parent_directory = "audio_data/"
	output_directory = "audio_splits/"
	out_file = open(user+"_splits.csv","w+")
	out_file.write("split_id,start_second,end_second\n")
	fs,signal = wavfile.read(parent_directory+user+"/speech_removed/audio.wav")

	split_count = 0
	for i in range(0,len(signal)-fs*2,fs*2):
		wavfile.write(output_directory+user+'_'+str(split_count)+".wav",fs,signal[i:i+(fs*2)])
		out_file.write(user+'_'+str(split_count)+","+str(i/fs)+","+str((i+(fs*2))/fs)+"\n")
		split_count+=1

	out_file.flush()
	out_file.close()

def main():
	for users in list_of_users:
		split_audio(users)

if __name__ == '__main__':
	main()

