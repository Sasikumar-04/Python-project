import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sasi2003@",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    # but it returns in tuple if i want in dictionary give dict as true and default is tuple
    cursor.close()
    connection.close()

# def fetch_all_records():
#     with get_db_cursor() as cursor:
#         cursor.execute("SELECT * FROM expenses")
#         expenses = cursor.fetchall()
#         return expenses

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses
def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with {expense_date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("insert into expenses (expense_date, amount, category, notes) values (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes)
        )

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("delete from expenses where expense_date=%s", (expense_date,))

# def delete_expenses_by_ids(ids):
#     if not ids:
#         return  # nothing to delete
#
#     # Build placeholders dynamically: %s,%s,%s ...
#     placeholders = ','.join(['%s'] * len(ids))
#     query = f"DELETE FROM expenses WHERE id IN ({placeholders})"
#
#     with get_db_cursor(commit=True) as cursor:
#         cursor.execute(query, tuple(ids))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with {start_date}, {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''
            select category,sum(amount) as total 
            from expenses where expense_date between %s and %s 
            group by category''',(start_date,end_date)
        )
        data = cursor.fetchall()
        return data


def fetch_month_summary():
    logger.info("fetch_month_summary called")
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT
                MONTH(expense_date) AS month_number,
                MONTHNAME(expense_date) AS month_name,
                SUM(amount) AS total
            FROM expenses
            GROUP BY
                MONTH(expense_date),
                MONTHNAME(expense_date)
            ORDER BY
                month_number ASC
        ''')

        data = cursor.fetchall()
        return data



if __name__ == "__main__":
    fetch_month_summary()
    # summary = fetch_expense_summary('2024-08-01','2024-08-05')
    # for record in summary:
    #     print(record)
    #fetch_all_records()
    #delete_expenses_by_ids([65,66])
    # expenses = fetch_expenses_for_date("2024-08-01")
    # print(expenses)
    #insert_expense("2024-08-25",40,"Food","Eat tasty samosa chat")
    #delete_expense_for_date("2024-08-25")
    #insert_expense("2024-09-20","300","Food","Panipuri")
    #fetch_expenses_for_date("2024-08-15")
    # print("Fetching")
    # fetch_expenses_for_date("2024-09-20")
    # print("deleting")
    # delete_expense_for_date("2024-09-20")
    # print("again fetching")
    # fetch_expenses_for_date("2024-09-20")

