import requests
if __name__ == '__main__':
    from company import Company
    from storage import Pickle_Storage, API_Storage
else:
    from .company import Company
    from .storage import Pickle_Storage, API_Storage


def get_api_url():
    my_name = "[2504-16] Медведев"

    try:
        response = requests.get(f"http://127.0.0.1:5000/api/", timeout=1)

        if response.status_code == 200:
            data = response.json()
            for item in data.get('sts', []):
                if my_name in item[1]:
                    found_url = f"http://127.0.0.1:5000/st{item[0]}/"
                    return found_url
    except Exception as e:
        print(f"Error: {e}")

    return None


def main():
    api_url = get_api_url()
    storage = API_Storage(api_url)
    company = Company(storage)

    functions = {
        1: ('Add an element', company.add_element),
        2: ('Show all elements', company.print_elements),
        3: ('Edit an element', company.edit_element),
        4: ('Delete an element', company.delete_element),
        5: ('Delete all elements', company.delete_all_elements),
        6: ('Save to file', company.save_elements),
        7: ('Load from file', company.load_elements),
        0: ('Exit', None)
    }

    while True:
        try:
            print()
            for i, (text, func) in functions.items():
                print(f'{i}. {text}')
            request = int(input('\nChoose an option = '))
            if request in functions:
                if functions[request][1] is not None:
                    functions[request][1]()
                else:
                    break
            else:
                print('Invalid option was chosen')
                continue
        except ValueError:
            print('Please enter a valid number')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')



if __name__ == '__main__':
    main()


