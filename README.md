# Audio-Steganography
Encoding files within a .wav audio file

Install the Wave Package on python before proceeding to execution of the Python Scripts

Steps to run the AudioSteg.py
	Open the Linux Terminal and run the following command
		python AudioSteg.py InputAudio.wav EncodingInputFile.txt OutputAudio.wav
	This will generate a public key to be shared with the receiver as PublicKey
	
Steps to run the AudioStegRecover.py
	Open the Linux Terminal and run the following command
		python AudioStegRecover.py OutputAudio.wav PublicKey RecoverFile.txt

The RecoverFile.txt stores all the decoded data
The OutputAudio.wav has the modified audio signal containing the encoded data from the EncodingInputFile.txt

Process - 

[1]
