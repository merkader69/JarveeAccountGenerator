import names
import random

username = ""
female_first = ""
surname = ""


def name_gen():
    global female_first
    global surname
    try:
        female_first = names.get_first_name(gender='female')
        surname = names.get_last_name()
    except Exception as e:
        print(e)
        pass


def creator():
    global username
    name_gen()  # generating first and last name

    full_name = female_first, surname
    if len(full_name) > 1:
        choice = random.choice(['Number', 'Number'])

        if choice == 'Number':
            number = '{:03d}'.format(random.randrange(1, 125))
            first_letter = full_name[0][0:3]
            three_letters_surname = full_name[-1][:3].rjust(random.randint(3, 7), 'x')
            username = '{}{}{}'.format(first_letter, three_letters_surname, number).lower()
    else:
        print('Error. Please enter first name and surname')
        # try again...
