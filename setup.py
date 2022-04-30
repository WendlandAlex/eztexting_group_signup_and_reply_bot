import sys

required_keys = ['USERNAME', 'PASSWORD']
optional_keys = ['COMPANY_NAME', 'EZTEXTING_CREDITCARD', 'EZTEXTING_ADMIN_CONTACT', 'BASE_URL']
list_of_envs = []

try:
    autoapprove = sys.argv[1]
    if autoapprove.lower() in ['autoapprove', 'silent', 'unattended', 'approve']:
        autoapprove = True
    else:
        autoapprove = None
except IndexError:
    autoapprove = None

def main():
    with open('.env', 'r') as dotenvfile:
        temp_env_dict = {}
        final_env_dict = {}

        for i in dotenvfile.readlines():
            print(i)
            if i.find('=') and i[0] != '#':
                i = i.strip('\n').rstrip('\n').split('=')
                if i[1] != '':
                    temp_env_dict[i[0]] = i[1]

        for i in required_keys:
            if temp_env_dict.get(i) is not None:
                print(f'The current setting for {i} is {temp_env_dict[i]}. Does that look right to you?')
                myinput = str(input('[y/N]: ')).lower()
                if myinput in ['n', 'no']:
                    added = str(input(f'provide a new value for the variable {i}: '))
                    if added in ['', None]:
                        exit('ERROR: required variable must not be blank')
                    final_env_dict[i] = added

                elif myinput in ['y', 'yes']:
                    final_env_dict[i] = temp_env_dict[i]

                else:
                    exit('ERROR: required variable must not be blank')

                temp_env_dict.pop(i)

            else:
                print(f'required environment variable not found! {i}')
                added = str(input('please provide a value for the required variable: '))
                if added in ['', None]:
                        exit('ERROR: required variable must not be blank')
                else:
                    final_env_dict[i] = added

        for i in optional_keys:
            if temp_env_dict.get(i) is not None:
                print(f'The current setting for {i} is {temp_env_dict[i]}. Does that look right to you?')
                myinput = str(input('[y/N]: ')).lower()
                if myinput not in ['y', 'yes']:
                    final_env_dict[i] = str(input(f'provide a new value for the variable {i}: '))
            
                temp_env_dict.pop(i)
            
            else:
                print(f'The environment variable {i} is optional. Would you like to provide it?')
                added = str(input('enter a value, or hit enter to skip: '))
                if added != '':
                    final_env_dict[i] = added

        for i in temp_env_dict:
            print(f'are you sure you would like to add new environment variable {i}={temp_env_dict[i]}?')
            confirm = str(input('confirm [y/N]: ').lower())
            if confirm in ['y', 'yes']:
                final_env_dict[i] = temp_env_dict[i]
                
        return final_env_dict

if __name__ == '__main__':
    final_env_dict = main()
    print('\n')
    for k,v in final_env_dict.items():
        print(f'{k}={v}')
    print('\n')
    decided = str(input('final chance! Are you sure want to write the above values?\nEnter [y/N]: ')).lower()
    if decided not in ['y', 'yes']:
        exit('exiting')

    with open('.env', 'w') as outfile:
        print(f'writing new .env file to {outfile.name}')
        for k, v in final_env_dict.items():
            outfile.write(f'{k}={v}\n')
