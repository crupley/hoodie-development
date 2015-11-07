# Ingest data from sources into standardized format and store in db
import numpy as np
import pandas as pd

import psycopg2


def make_assessment():

	conn = psycopg2.connect(dbname='hoodie', user='postgres', host='/tmp')
	c = conn.cursor()

	df = pd.read_csv('../data/assessment/Secured_Property_Assessment_Roll_FY13_Q4.csv')
	n_cols = df.shape[1]
	esses = '%s, ' * (n_cols - 1) + '%s'

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
		VALUES (%s)''' % esses

	# for idx in df.index:
	# 	values = df.ix[idx].values
	# 	c.execute(q_string, values)
	conn.commit()
	conn.close()






	df.RE = df.RE.apply(lambda x: x.strip('$')).astype('float')
	df.RE_Improvements = df.RE_Improvements.apply(lambda x: x.strip('$'))
	df.RE_Improvements = df.RE_Improvements.astype('float')
	df.PP_Value = df.PP_Value.apply(lambda x: x.strip('$')).astype('float')
	# df.Taxable_Value = df.Taxable_Value.apply(lambda x: x.strip('$'))
	# df.Taxable_Value = df.astype('float')

	return df