import pandas as pd

def dcrypt(txt):
	sts = txt
	lrn = int(sts[0])
	rrn = int(sts[-1])
	Rn = lrn + rrn
	strg = sts.split("*")
	Ubnd = int(len(strg)-1)
	DeCrypt = ""
	for x in range(len(strg)):
		if x==0:
			continue
		if x==Ubnd:
			DeCrypt = DeCrypt + chr(int(int(strg[x][:len(strg[x])-1]) / Rn))
		else:
			DeCrypt = DeCrypt + chr(int(int(strg[x]) / Rn))
	return DeCrypt

df = pd.read_excel('PasswordFile.xlsx')
col_one_list = df['pswrd'].tolist()
for x in col_one_list:
	y = dcrypt(x)
	print(y)
