import xlwt

style_big = xlwt.easyxf('font: name Times New Roman, bold on')
style_norm = xlwt.easyxf('font: name Times New Roman')

class PlaceData:


	def __init__(self):
		"""Cosntructs a PlaceData instance, where a workbook is set up

		Parameters
		==========

		query
			the sequence

		"""
		self.workbook = xlwt.Workbook()

	def get_workbook(self):
		return self.workbook

	# A helper function
	# Do i need this self thing??? i removed it
	def __general_blast_write(self, sheet, query, row_start, typeblast):
		# List of organisms to be used later for checking kingdoms?
		allorgs = []

		# List of 3 organisms (at most) to be placed in file
		orgs3 = []

		# List of 3 organisms positions
		orgs3_pos = []

		print('In private method: B4 try statement')

		# print(query)

		# print(type(query))

		# print('NOW GETTING BlastOutput2')

		# data = query.get('BlastOutput2')
		# print(data)

		# print('NOW GETTING report')

		# data = query.get('BlastOutput2').get('report')
		# print(data)
		# print('NOW GETTING results')

		# data = query.get('BlastOutput2').get('report').get('results')
		# print(data)

		print('NOW GETTING hits')

		data = query.get('BlastOutput2').get('report').get('results').get('search').get('hits')
		# print(data)

		print('In private method: After try statement')

		# print(dir(data))
		# print(data)

		if(len(data) == 0):
			print(data)
			return None

		print('Going thru hits now : b4')
		print('===============')
		# Go thru all hits
		for j in range(0, len(data)):
			print('\tSetting temp')
			temp = str(data[j].get('description')[0].get('sciname'))
			print('\tDone setting temp')
			if(temp in orgs3):
				print('\t\tContinued!')
				continue

			print('\tAdding to all arrays')
			allorgs.append(temp)
			if(len(orgs3) < 3):
				orgs3.append(temp)
				orgs3_pos.append(j + 1)

			print('\tWriting to a sheet')
			row = row_start + len(orgs3) - 1
			sheet.write(row, 0, str(data[j].get('description')[0].get('accession')), style_norm)
			sheet.write(row, 1, str(data[j].get('description')[0].get('title')), style_norm)
			sheet.write(row, 2, temp, style_norm)

			print('\tWriting again to a sheet')

			qseq = str(data[j].get('hsps')[0].get('qseq'))
			sheet.write(row, 3, qseq[0] + str(data[j].get('hsps')[0].get('query_from')), style_norm)
			sheet.write(row, 4, qseq[-1] + str(data[j].get('hsps')[0].get('query_to')), style_norm)
			sheet.write(row, 5, str(data[j].get('hsps')[0].get('evalue')), style_norm)

			if(len(orgs3) >= 3):
				break

		print('=============== Success in for loop')


		if(typeblast != 2):
			print('Starting to evaluate the e value stuff')
			eval = str(data[0].get('hsps')[0].get('evalue'))
			print(eval)
			eval = eval.split('e')
			print(eval)
			if(len(eval) == 1):
				eval = -100
			else:
				eval = float(eval[1])
			print(eval)

			print('Starting if statement')
			if(eval <= -5):
				if(typeblast == 0):
					qseq = str(data[0].get('hsps')[0].get('qseq'))
					print('Starting while loop')
					while(qseq.endswith('A') or qseq.endswith('a')):
						qseq = qseq[:-1]
					print('Ended while loop! Phew...')
					if(len(qseq) <= 15):
						sheet.write(row_start, 6, 'Similar to Orgs? No')
					else:
						sheet.write(row_start, 6, 'Similar to Orgs? Yes')
				else:
					sheet.write(row_start, 6, 'Similar to Orgs? Yes')

			else:
				sheet.write(row_start, 6, 'Similar to Orgs? No')
		else:
			# something
			p = 3

		print('About to save xls')

		self.workbook.save('WaksmanOutputData.xls')

		print('Saved xls!')

		print("allorgs:")
		print(allorgs)
		print('\nOrgs3')
		print(orgs3)
		print('orgs3_pos')
		print(orgs3_pos)


	def blastn_write(self, query_nr, query_est):
		# Will write to a new blastn sheet

		print('At blastn_write of place data class')
		sheet = self.workbook.add_sheet('BLASTn')

		print('Writing to rows in blastn_write')
		# Write to rows 0 and 5 (for nr and est databases)
		for j in [0, 5]:
			sheet.write(j, 0, 'Accession #', style_big)
			sheet.write(j, 1, 'Definition', style_big)
			sheet.write(j, 2, 'Organism', style_big)
			sheet.write(j, 3, 'Query Start', style_big)
			sheet.write(j, 4, 'Query End', style_big)
			sheet.write(j, 5, 'E Value', style_big)

		sheet.write(0, 6, '<-nr', style_big)
		sheet.write(5, 6, '<-est', style_big)

		print('****************************')

		self.__general_blast_write(sheet, query_nr, 1, typeblast=0)
		self.__general_blast_write(sheet, query_est, 6, typeblast=0)

		print('finished doing private function stuff')

	def blastx_write(self, query_nr):
		# Will write to a new blastn sheet

		print('At blastx_write of place data class')
		sheet = self.workbook.add_sheet('BLASTx')

		print('Writing to rows in blastn_write')

		sheet.write(0, 0, 'Accession #', style_big)
		sheet.write(0, 1, 'Definition', style_big)
		sheet.write(0, 2, 'Organism', style_big)
		sheet.write(0, 3, 'Query Start', style_big)
		sheet.write(0, 4, 'Query End', style_big)
		sheet.write(0, 5, 'E Value', style_big)

		sheet.write(0, 6, '<-nr', style_big)

		print('****************************')

		self.__general_blast_write(sheet, query_nr, 1, typeblast=1)


