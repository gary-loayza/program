#############################
# Author: Gary Loayza       #
# Date: 2020-04-29          #
#############################
import pandas as pd
import numpy as np

import connection
import query
import result

live = connection.create('LIVE')


# Initiate "results" dictionary of DataFrames
# based on the query of open branches in the database
branch_query = query.branch()
results = result.init(pd.read_sql(branch_query,live))

# Generate the "shares" DataFrame from SQL
sh_query = query.shares()
shares = pd.read_sql(sh_query,live)

# Filter out closed shares and non-primary shares
# Create a new DataFrame and name it "prim_open"
is_open = shares['close_date'].isna()
sh_open = shares[is_open]
prim_open = sh_open[sh_open['id']=='0000']

# Run and store computation
# within "results" dictionary
result.tot_members(prim_open, results)

result.ages(prim_open, results)

# Generate the "loans" DataFrame from SQL
ln_query = query.loans()
loans = pd.read_sql(ln_query,live)

# Filter out closed loans to create a new DataFrame
# Name it "ln_open"
is_open = loans['close_date'].isna()
ln_open = loans[is_open]

result.loans(ln_open, results)

# products() has two flavors,
# share products and loan products
result.products(sh_open, results, 'Share')
result.products(ln_open, results, 'Loan')

sdb_query = query.sdb()
sdb = pd.read_sql(sdb_query,live)

result.safety_deposit_boxes(sdb, results)

estat_query = query.estatements()
estat = pd.read_sql(estat_query,live)

result.estatements(estat, results)

result.insurance(ln_open, results)

login_query = query.login()
login = pd.read_sql(login_query,live)

result.login(login, results)

result.printr(results)
