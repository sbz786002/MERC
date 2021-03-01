import requests
import xlsxwriter
from pandas import json_normalize
def getdrpExcel(Que):
	workbook = xlsxwriter.Workbook('List1_validate.xlsx')
	worksheet = workbook.add_worksheet()
	header_format = workbook.add_format({
    'border': 1,
    'bg_color': '#C6EFCE',
    'bold': True,
    'text_wrap': False,
    'valign': 'vcenter',
    'indent': 1,
	})
	st = requests.get("http://FS3.corp.virolaindia.com:7071//api/v1/Common/GetDynamicQuery?query="+Que+"&db=IMAGEDB")
	rs = st.json()
	cst = rs['data']
	rs1 = json_normalize(rs['data'])
	print(rs1['Product'])
	ind = rs1.keys()
	row = 0
	col = 0
	for x in ind:
	    #worksheet.set_column(row,co)
	    s = worksheet.write(row,col,x,header_format)
	    dt = []
	    lst = rs1[x]
	    for y in lst:
	        if y is not None and y not in dt:
	            dt.append(y)
	    print(len(dt))
	    if len(dt) > 0:
	        worksheet.data_validation(row+1, col,20,col,{'validate': 'list','source': dt})
	    col += 1
	workbook.close()
	full_path = abspath('List1_validate.xlsx')
	return full_path