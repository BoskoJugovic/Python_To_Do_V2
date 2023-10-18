# for sql server
import pyodbc

server_name = "DESKTOP-6O17EBS"
database_name = "TO_DO"

conn = pyodbc.connect(f"""
    Driver={{SQL Server Native Client 11.0}};
    Server={server_name};
    Database={database_name};
    Trusted_Connection=yes;
""")

cursor = conn.cursor()


def take_input():
    while True:
        choice = input("\nWelcome! (Type 'exit' if you want to end the app)\n"
                       "\t1) Create new item\n"
                       "\t2) List all existing items\n"
                       "\t3) Sort all existing items\n"
                       "\t4) Search for an item\n"
                       "\t5) Delete an item\n"
                       "Your choice: ")

        if choice == 'exit':
            return
        elif choice == '1':
            create()
        elif choice == '2':
            list_items()
        elif choice == '3':
            sort_by = input("\nSort by:"
                            "\n\t1) Title"
                            "\n\t2) Priority"
                            "\nYour choice: ")
            asc_desc = input("\n\t1)Ascending"
                             "\n\t2)Descending"
                             "\nYour choice: ")
            if (sort_by == '1' or sort_by == '2') and (asc_desc == '1' or asc_desc == '2'):
                sort(sort_by, asc_desc)
        elif choice == '4':
            search_by = input("\nSearch by:"
                              "\n\t1) Title"
                              "\n\t2) Priority"
                              "\nYour choice: ")
            if search_by == '1' or search_by == '2':
                search(search_by)
        elif choice == '5':
            delete()
        else:
            print("\nChoose an option from 1 - 5\n")


def create():
    while True:
        print("\nType 'go back' to return to the menu and 'exit app' to end the app\n")
        title = input("Title: ").strip()
        if title == '':
            break

        content = input("Content: ").strip()
        if content == '':
            break

        priority = input("Priority (number 1 - 5): ").strip()
        try:
            if int(priority) not in range(1, 6):
                break
        except ValueError:
            print('Priority must be a number between 1 and 5')

        item_to_create = (title, content, priority)
        insert_query = "INSERT INTO Items (Title, Content, Priority) VALUES (?, ?, ?)"
        cursor.execute(insert_query, item_to_create)
        conn.commit()

        choice = input("\nDo you want to enter another item:"
                       "\n\t1) Yes"
                       "\n\t2) No"
                       "\nYour choice: ")
        if choice == '1':
            continue
        else:
            break


def list_items():
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    for item in items:
        print(f"\nTitle: {item[1]}"
              f"\nContent: {item[2]}"
              f"\nPriority: {item[3]}")


def sort(sort_by, asc_desc):
    if sort_by == '1':
        if asc_desc == '1':
            cursor.execute("SELECT * FROM Items ORDER BY Title")
        else:
            cursor.execute("SELECT * FROM Items ORDER BY Title DESC")

    else:
        if asc_desc == '1':
            cursor.execute("SELECT * FROM Items ORDER BY Priority")
        else:
            cursor.execute("SELECT * FROM Items ORDER BY Priority DESC")
    results = cursor.fetchall()
    for result in results:
        print(f"\nTitle: {result[1]}"
              f"\nContent: {result[2]}"
              f"\nPriority: {result[3]}")


def search(search_by):
    if search_by == '1':
        search_item = input("\nTitle: ")
        cursor.execute(f"SELECT * FROM Items WHERE Title = '{search_item}'")
    else:
        search_item = input("\nPriority: ")
        try:
            if int(search_item) in range(1, 6):
                cursor.execute(f"SELECT * FROM Items WHERE Priority = '{search_item}'")
        except ValueError:
            print("Priority must be a number between 1 and 5")
            return

    results = cursor.fetchall()
    if not results:
        print("\nNo such items in database")
    else:
        for result in results:
            print(f"\nTitle: {result[1]}"
                  f"\nContent: {result[2]}"
                  f"\nPriority: {result[3]}")


def delete():
    item_to_delete = input("What item would you like to delete? ")
    delete_query = "DELETE FROM Items WHERE Title = ?"
    cursor.execute(delete_query, item_to_delete)
    items_deleted = cursor.rowcount
    conn.commit()
    if items_deleted > 0:
        print(f"\n{items_deleted} items were deleted")
    else:
        print("\nNo such item found in database")


take_input()

cursor.close()
conn.close()
