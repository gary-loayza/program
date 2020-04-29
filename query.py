#############################
# Author: Gary Loayza       #
# Date: 2020-04-29          #
#############################

def branch():
    query = '''
        SELECT
            branch.description
        FROM
            core.branch branch
        WHERE
            branch.status = 'O'
    '''
    return query

def shares():
    query = '''
        SELECT
            share.id,
            stype.description,
            person.serial AS person_serial,
            person.birth_date,
            share.balance,
            branch.description AS branch,
            share.open_date,
            share.close_date
        FROM
            core.person person
            INNER JOIN core.account account ON
                account.primary_person_serial = person.serial
            INNER JOIN core.share share ON
                share.parent_serial = account.serial
            INNER JOIN core.branch branch ON
                share.branch_serial = branch.serial
            INNER JOIN core.sh_type AS stype ON
                stype.serial = share.type_serial
        WHERE
            share.charge_off_date IS NULL
    '''
    return query

def loans():
    query = '''
        SELECT
            loan.id,
            ltype.description,
            person.serial AS person_serial,
            loan.balance,
            branch.description AS branch,
            ln_life_insurance.description AS life_insurance,
            CASE
                WHEN collateral_insurance.category = 'G' THEN 'GAP'
                WHEN collateral_insurance.category = 'M' THEN 'MBP'
                WHEN collateral_insurance.category = 'C' THEN 'Collision'
                WHEN collateral_insurance.category = 'F' THEN 'Fire'
                WHEN collateral_insurance.category = 'L' THEN 'Flood'
                WHEN collateral_insurance.category = 'P' THEN 'PMI'
                WHEN collateral_insurance.category = 'c' THEN 'CPI'
                WHEN collateral_insurance.category = 'O' THEN 'Other'
            END AS other_insurance,
            loan.open_date,
            loan.close_date
        FROM
            core.person person
            INNER JOIN core.account account ON
                account.primary_person_serial = person.serial
            INNER JOIN core.loan loan ON
                loan.parent_serial = account.serial
            INNER JOIN core.branch branch ON
                loan.branch_serial = branch.serial
            INNER JOIN core.ln_type AS ltype ON
                ltype.serial = loan.type_serial
            LEFT JOIN core.ln_life_insurance AS ln_life_insurance ON
                ln_life_insurance.serial = loan.LIFE_INSURANCE_SERIAL
            LEFT JOIN core.collateral collateral ON
                collateral.parent_serial = loan.serial
            LEFT JOIN core.collateral_insurance collateral_insurance ON
                collateral_insurance.parent_serial = collateral.serial
        WHERE
            loan.charge_off_date IS NULL
    '''
    return query

def sdb():
    query = '''
        SELECT
            rental.serial,
            rental.description AS box_number,
            rental_type.description AS box_description,
            branch.description AS branch,
            CASE
                WHEN rental.status = 'A' THEN 'Available'
                WHEN rental.status = 'R' THEN 'Rented'
                WHEN rental.status = 'H' THEN 'Held'
            END AS status,
            rental.status_date
        FROM
            core.rental rental
            INNER JOIN core.rental_type rental_type ON
                rental.type_serial = rental_type.serial
            INNER JOIN core.branch branch ON
                rental.branch_serial = branch.serial
    '''
    return query

def estatements():
    query = '''
        SELECT
            account.serial,
            CASE
                WHEN account.e_stmt_option = 'M' THEN 'Mail statement only'
                WHEN account.e_stmt_option = 'E' THEN 'E-statement only'
                WHEN account.e_stmt_option = 'B' THEN 'E-statement and mail statement'
            END AS e_stmt_option
        FROM
            core.account account
        WHERE
            account.close_date IS NULL
    '''
    return query

def login():
    query = '''
        SELECT
            login_channel.description AS login_channel,
            COUNT(login.last_login_time) AS login_count
        FROM
            core.login login
            INNER JOIN core.login_channel login_channel ON
                login.channel_serial = login_channel.serial
        WHERE
            login.last_login_time BETWEEN (CURRENT_DATE - 1 MONTH ) AND CURRENT_DATE
        GROUP BY
            login_channel.description
    '''
    return query


if __name__ == "__main__":
    print('To run this program, execute \'$ python main.py\'')
