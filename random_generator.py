from random import randint, uniform, choice
import datetime

class random_generator:
    def __init__(self):
        self.ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        self.ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.chars = self.ascii_lowercase + self.ascii_uppercase + ' '

    def get_integer(self, min_value, max_value):
        return randint(min_value, max_value)

    def get_float(self, min_value, max_value):
        return uniform(min_value, max_value)

    def get_string(self, min_chars, max_chars):
        return ''.join(choice(self.chars) for i in range(randint(min_chars, max_chars)))

    def get_char(self):
        return choice(self.ascii_lowercase + self.ascii_uppercase)

    def get_boolean(self):
        return choice([True, False])

    def get_complex(self, min_value, max_value):
        return complex(uniform(min_value, max_value), uniform(min_value, max_value))

    def get_date(self, min_year, max_year):
        return datetime.date(randint(min_year, max_year), randint(1, 12), randint(1, 28))

    def get_time(self):
        return datetime.time(randint(0, 23), randint(0, 59), randint(0, 59))

    def get_email(self, min_chars, max_chars):
        return self.get_string(min_chars, max_chars) + '@' + self.get_string(min_chars, max_chars) + '.com'

    def generate(self, element_type, *extra_args):
        if element_type == int:
            if len(extra_args) != 2:
                extra_args = (-100, 100)
            return self.get_integer(*extra_args)
        elif element_type == float:
            if len(extra_args) != 2:
                extra_args = (-100.0, 100.0)
            return self.get_float(*extra_args)
        elif element_type == str:
            if len(extra_args) != 2:
                extra_args = (1, 10)
            return self.get_string(*extra_args)
        elif element_type == bool:
            return self.get_boolean()
        elif element_type == complex:
            if len(extra_args) != 2:
                extra_args = (-100.0, 100.0)
            return self.get_complex(*extra_args)
        elif element_type == datetime.date:
            if len(extra_args) != 2:
                extra_args = (1900, 2020)
            return self.get_date(*extra_args)
        elif element_type == datetime.time:
            return self.get_time()
        elif element_type == datetime.datetime:
            return datetime.datetime.combine(self.get_date(*extra_args), self.get_time())
        else:
            raise Exception('Invalid type: {}'.format(element_type))

    def get_list(self, min_size, max_size, element_type, extra_args):
        return [self.generate(element_type, *extra_args) for i in range(randint(min_size, max_size))]

    def get_map(self, min_size, max_size, key_type, value_type, key_args, value_args):
        return {self.generate(key_type, *key_args): self.generate(value_type, *value_args) for i in range(randint(min_size, max_size))}

    def get_tuple(self, size, *element_types):
        return tuple(self.generate(element_type) for element_type in element_types)

    def get_set(self, min_size, max_size, element_type, extra_args):
        return {self.generate(element_type, *extra_args) for i in range(randint(min_size, max_size))}

    