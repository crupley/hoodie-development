# Ingest data from sources into standardized format and store in db
import numpy as np
import pandas as pd

import psycopg2

import pdb


def db_insert(df, q_string):
	# insert raw data into db
	n_cols = df.shape[1]
	esses = '%s, ' * (n_cols - 1) + '%s'
	q_string = q_string % esses

	conn = psycopg2.connect(dbname='hoodie', user='postgres', host='/tmp')
	c = conn.cursor()

	for idx in df.index:
		values = df.ix[idx].values
		c.execute(q_string, values)
		conn.commit()
	conn.close()

# assessment data
def make_assessment():
	df = pd.read_csv('../data/assessment/Secured_Property_Assessment_Roll_FY13_Q4.csv')

	q_string = '''
		INSERT INTO assessment_raw (Situs_Address,
									Situs_Zip,
									APN,
									RE,
									RE_Improvements,
									Fixtures_Value,
									PP_Value,
									District,
									Taxable_Value,
									geom)
		VALUES (%s)'''

	# insert raw data
	db_insert(df, q_string)

	# clean data
	df.drop('Fixtures_Value', axis = 1, inplace = True)
	df.RE = df.RE.apply(lambda x: x.strip('$')).astype('float')
	df.RE_Improvements = df.RE_Improvements.apply(lambda x: x.strip('$'))
	df.RE_Improvements = df.RE_Improvements.astype('float')
	df.PP_Value = df.PP_Value.apply(lambda x: x.strip('$')).astype('float')
	df.Taxable_Value = df.Taxable_Value.apply(lambda x: x.strip('$'))
	df.Taxable_Value = df.Taxable_Value.astype('float')

	df['lat'] = df.geom.apply(lambda x: eval(x)[0])
	df['lon'] = df.geom.apply(lambda x: eval(x)[1])
	df.drop('geom', axis = 1, inplace = True)

	# insert cleaned data into db
	q_string = '''
		INSERT INTO assessment (Situs_Address,
								Situs_Zip,
								APN,
								RE,
								RE_Improvements,
								PP_Value,
								District,
								Taxable_Value,
								lat,
								lon)
		VALUES (%s)'''

	db_insert(df, q_string)

	return