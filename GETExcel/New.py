import json
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import requests
from xlrd import open_workbook
from os.path import abspath
import os
import glob
import win32com.client as client
import pandas as pd
import xlwings as xw
from pandas import json_normalize
import time


def getAttribute(file_path,row_index,Sheet_index):
	book = open_workbook(file_path)
	#s = int(Sheet_index)
	sheet = book.sheet_by_name(Sheet_index)
	r = int(row_index)
	d = [sheet.cell(r-1, col_index).value for col_index in range(0,sheet.ncols)]
	dict_list = []
	for x in d:
	    dt = {"key":x}
	    if x is None or x == '':
	    	continue
	    dict_list.append(dt)
	return dict_list
	print(e)
	return str(e)

#x = getAttribute('C:\TESTAPI\DBAPI\ExcelShare\Myntra-Sku-Template-2021-02-01.xlsx', 3, 2)

def getPortalExcel(data,portal,template,sheetName,CellAddress):
	df = pd.DataFrame(data)
	path = 'C:/TESTAPI/DBAPI/Catalogue/'+portal+'/'+template+'/*'
	list_of_files = glob.glob(path)	
	print(list_of_files[0])
	loc = list_of_files[0]
	Newfile = os.path.basename(list_of_files[0])
	new_loc = 'GETExcel/'+Newfile
	wb = xw.Book(loc)
	ws = wb.sheets[sheetName]
	ws.range(CellAddress).options(index=False, header=False).value = df
	try:
		os.remove(new_loc)
	except Exception as e:
		pass
	wb.save(new_loc)
	wb.close()
	dt = [new_loc,Newfile]
	return dt

#x = getPortalExcel()

def getExcel(data):

	df = pd.DataFrame(data)
	loc = 'GETExcel/Myntra-Sku-Template-2021-02-01.xlsx'
	new_loc = 'GETExcel/MYNTRA.xlsx'
	full_path = abspath(loc)
	wb = xw.Book(loc)
	ws = wb.sheets['Casual Shoes']
	ws.range('B4').options(index=False, header=False).value = df
	wb.save(new_loc)
	wb.close()

	#writer = pd.ExcelWriter('GETExcel/New.xlsx')

	#df.to_excel(writer, sheet_name='Sheet1',index=False)
	#writer.save()
	#full_path = abspath('GETExcel/New.xlsx')
	return new_loc

def getdrpExcel(Que):
	writer = pd.ExcelWriter('Import_File.xlsx', engine='xlsxwriter')
	workbook  = writer.book
	worksheet = workbook.add_worksheet()
	header_format = workbook.add_format({
    'border': 1,
    'bg_color': '#DEB887',
    'bold': True,
    'text_wrap': False,
    'valign': 'vcenter',
    'indent': 1,
	})
	header_format1 = workbook.add_format({
    'border': True,
    'bg_color': '#C6EFCE',
    'text_wrap': True,
    'valign': 'vcenter',
    'indent': 1
	})
	st = requests.get("http://FS3.corp.virolaindia.com:7071//api/v1/Common/GetDynamicQuery?query="+Que+"&db=IMAGEDB")
	rs = st.json()
	cst = rs['data']
	st0 = requests.get("http://FS3.corp.virolaindia.com:7071//api/v1/Common/GetDynamicQuery?query=SELECT AttributeName, discption, Dailogue1, Dailogue2 FROM AttributeMaster inner join ValidationDis on AttributeMaster.Validation = ValidationDis.Validation WHERE (Dis = 0) and AID <> 26&db=IMAGEDB")
	rs0 = st0.json()
	dt1 = pd.json_normalize(rs0['data'])
	rs1 = json_normalize(rs['data'])
	rs1.to_excel(writer,sheet_name="Sheet2",index=False)
	ind = rs1.keys()
	row = 0
	col = 0
	for x in ind:
	    #worksheet.set_column(row,co)
	    sh = dt1.loc[dt1['AttributeName'] == x]
	    s = worksheet.write(row,col,x,header_format)
	    worksheet.set_column(col, col, 15)
	    if len(sh) > 0:
	        x1 = sh.iloc[0]['Dailogue1']
	        x2 = sh.iloc[0]['Dailogue2']
	        disc = sh.iloc[0]['discption']
	        s0 = worksheet.write(row+1,col,x1,header_format1)
	        worksheet.set_row(row+1,30)
	        s0 = worksheet.write(row+2,col,disc,header_format1)
	        worksheet.set_row(row+2,40)
	        s1 = worksheet.write(row+3,col,x2,header_format1)
	        worksheet.set_row(row+3,50)
	    else:
	        s0 = worksheet.write(row+1,col,'',header_format1)
	        worksheet.set_row(row+1,30)
	        s0 = worksheet.write(row+2,col,'',header_format1)
	        worksheet.set_row(row+2,40)
	        s1 = worksheet.write(row+3,col,'',header_format1)
	        worksheet.set_row(row+3,50)
	    dt = []
	    lst = rs1[x]
	    for y in lst:
	        if y is not None and y not in dt:
	            dt.append(y)
	    if len(dt) > 0:
	        frm = xl_rowcol_to_cell(1,col,row_abs=True, col_abs=True)
	        to = xl_rowcol_to_cell(len(dt),col,row_abs=True, col_abs=True)
	        worksheet.data_validation(row+4, col,2000,col,
	                                  {'validate': 'list',
	                                   'input_message': 'Please Select From Drop-Down',
	                                   'error_message': 'Value Should be Selected From Drop down',
	                                   'source': "Sheet2!%s:%s"%(frm,to)})
	        #worksheet.data_validation(row+1, col,20,col,{'validate': 'list','source': "Sheet2!$AC$2:$AC$250"})
	    col += 1
	    
	#worksheet1 = writer.sheets['Sheet2']
	#worksheet1.visible = 2
	worksheet.freeze_panes(4, 0)
	writer.save()
	workbook.close()
	full_path = abspath('pandas_simple.xlsx')
	xl = client.Dispatch("Excel.Application")
	SHEET_NAME = "Sheet2"  # The name of the sheet you want to hide
	wb = xl.Workbooks.Open(full_path)
	wb.Worksheets("Sheet2").Visible = 2 # xlSheetVeryHidden
	wb.Save()
	wb.Close()
	return full_path