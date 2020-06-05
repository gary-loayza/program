#############################
# Author: Gary Loayza       #
# Date: 2020-04-29          #
#############################
import datetime as dt
import pandas as pd
import numpy as np

import main

today = dt.date.today()
stamp =  today.strftime("%Y-%m-%d")

def init(data):
    """
    Generate a dictionary of empty DataFrames by branch to
    store later data points.
    """
    results = {}
    results['Total'] = pd.DataFrame([], columns=['Description','Total'])

    for index, row in data.iterrows():
        results[row['description']] = pd.DataFrame([], columns=['Description','Total'])

    return results

def tot_members(data, results):
    """
    Handle writing to results for membership distribution
    """
    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Members',
            'Total': ''
    }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Total Members',
        'Total': data['person_serial'].nunique()
    }, ignore_index=True)

    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Total Members',
            'Total': data[data['branch']==tab]['person_serial'].nunique()
        }, ignore_index=True)
    results['Total'].drop_duplicates(subset='Description',keep='first',inplace=True)
    return results

def ages(data, results):
    """
    Compute age breakdowns for each branch
    """
    age = ((today - data['birth_date'])/dt.timedelta(days=365.25)).dropna().astype(int)

    results['Total'] = results['Total'].append({
        'Description': 'Average Age',
        'Total': '%.2f'%(age.mean())
    }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Ages 0 to 17',
        'Total': age.apply(lambda x: np.sum(x<=17)).sum()
    }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Ages 18 to 55',
        'Total': age.apply(lambda x: np.sum(17<x<=55)).sum()
    }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Ages 56 and Up',
        'Total': age.apply(lambda x: np.sum(x>55)).sum()
    }, ignore_index=True)

    age = {}
    for tab in results:
        age[tab] = (
                today - data[data['branch'] == tab]['birth_date']
                ).apply(
                        lambda x: x/dt.timedelta(days=365.25)
                        ).dropna().astype(int)
        results[tab] = results[tab].append({
            'Description': 'Average Age',
            'Total': '%.2f'%(age[tab].mean())
        }, ignore_index=True)
        results[tab] = results[tab].append({
            'Description': 'Ages 0 to 17',
            'Total': age[tab].apply(lambda x: np.sum(x<=17)).sum()
        }, ignore_index=True)
        results[tab] = results[tab].append({
            'Description': 'Ages 18 to 55',
            'Total': age[tab].apply(lambda x: np.sum(17<x<=55)).sum()
        }, ignore_index=True)
        results[tab] = results[tab].append({
            'Description': 'Ages 56 and Up',
            'Total': age[tab].apply(lambda x: np.sum(x>55)).sum()
        }, ignore_index=True)

    results['Total'].drop_duplicates(subset='Description',keep='first',inplace=True)

    return results

def loans(data, results):
    """
    Compute loan totals and balances for each branch
    """
    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Loans',
            'Total': ''
        }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Total Loans',
        'Total': data.shape[0]
    }, ignore_index=True)

    results['Total'] = results['Total'].append({
        'Description': 'Total Balance',
        'Total': '$%.2f'%(data['balance'].sum())
    }, ignore_index=True)

    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Total Loans',
            'Total': data[data['branch']==tab].shape[0]
        }, ignore_index=True)
        results[tab] = results[tab].append({
            'Description': 'Total Balance',
            'Total': '$%.2f'%(data[data['branch']==tab]['balance'].sum())
        }, ignore_index=True)

    results['Total'].drop_duplicates(subset='Description',keep='first',inplace=True)
    return results

def products(data, results, flavor):
    """
    Compute share/loan product totals and per branch breakdown,
    depending on the flavor when run.
    """
    if flavor == 'Share':
        for tab in results:
            results[tab] = results[tab].append({
                'Description': 'Products',
                'Total': ''
            }, ignore_index=True)

    for tab in results:
        results[tab] = results[tab].append({
            'Description': flavor + ' ' + 'Products',
            'Total': ''
        }, ignore_index=True)
    products = data['description'].value_counts().reset_index()
    products.columns = ['Description','Total']
    results['Total'] = results['Total'].append(products, ignore_index=True)

    products = {}
    for tab in results:
        products[tab] = data[data['branch']==tab]['description'].value_counts().reset_index()
        products[tab].columns = ['Description', 'Total']
        results[tab] = results[tab].append(products[tab], ignore_index=True)
    return results

def safety_deposit_boxes(data, results):
    """
    Display the availability of all safety deposit boxes at each branch
    """
    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Services',
            'Total': ''
        }, ignore_index=True)
        results[tab] = results[tab].append({
            'Description': 'Safety Deposit Boxes',
            'Total': ''
        }, ignore_index=True)
    sdb = data['status'].value_counts().reset_index()
    sdb.columns = ['Description', 'Total']
    results['Total'] = results['Total'].append(sdb, ignore_index=True)

    sdb = {}
    for tab in results:
        sdb[tab] = data[data['branch']==tab]['status'].value_counts().reset_index()
        sdb[tab].columns = ['Description', 'Total']
        results[tab] = results[tab].append(sdb[tab], ignore_index=True)
    return results

def estatements(data, results):
    """
    Display the usage of eStatements
    Note that eStatements are per account, not per branch
    """
    results['Total'] = results['Total'].append({
        'Description': 'eStatements',
        'Total': ''
    }, ignore_index=True)
    estat_counts = data['e_stmt_option'].value_counts().reset_index()
    estat_counts.columns = ['Description', 'Total']
    estat_counts.index = estat_counts['Description']
    results['Total'] = results['Total'].append(estat_counts, ignore_index=True)
    results['Total'] = results['Total'].append({
        'Description': 'Total Accounts subscribed to eStatments',
        'Total': estat_counts['Total'].loc['E-statement only']
        + estat_counts['Total'].loc['E-statement and mail statement']
    }, ignore_index=True)
    return results

def insurance(data, results):
    """
    Compute the insurance products and break them down by branch
    """
    for tab in results:
        results[tab] = results[tab].append({
            'Description': 'Insurance',
            'Total': ''
        }, ignore_index=True)
    life = data['life_insurance'].value_counts().reset_index()
    life.columns = ['Description', 'Total']
    results['Total'] = results['Total'].append(life, ignore_index=True)

    other = data['other_insurance'].value_counts().reset_index()
    other.columns = ['Description', 'Total']
    results['Total'] = results['Total'].append(other, ignore_index=True)
    # Split by Branch
    life = {}
    other = {}
    for tab in results:
        life[tab] = data[data['branch']==tab]['life_insurance'].value_counts().reset_index()
        life[tab].columns = ['Description', 'Total']
        results[tab] = results[tab].append(life[tab], ignore_index=True)
        other[tab] = data[data['branch']==tab]['other_insurance'].value_counts().reset_index()
        other[tab].columns = ['Description', 'Total']
        results[tab] = results[tab].append(other[tab], ignore_index=True)
    return results

def login(data, results):
    """
    Display login methods that our users are utilizing
    Note that login data is not even attached to a member
    """
    results['Total'] = results['Total'].append({
        'Description': 'Phone Banking',
        'Total': ''
    }, ignore_index=True)
    data.columns = ['Description', 'Total']
    results['Total'] = results['Total'].append(data, ignore_index=True)
    return results

def printr(results):
    """
    Method for writing results DataFrames to spreadsheet
    """
    with pd.ExcelWriter('/opt/program/output/Monthly_Member_Analysis_' + stamp + '.xlsx') as writer:
        for tab in results:
            results[tab].to_excel(writer, sheet_name=tab, index=False)

if __name__ == "__main__":
   main.program()
