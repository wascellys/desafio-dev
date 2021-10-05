from django.utils import timezone


class CNABFile(object):
    """
    CNAB file object
    """

    def __init__(self, file):
        """Constructor 

        Args:
            file (InMemoryUploadedFile): file to be uploaded
        """
        self._lines = file.read().decode('utf-8').splitlines()[4:-2]
        self._stores = []
        for line in self._lines:
            transaction = self.process_line(line)
            store = transaction.pop('store')
            found = False
            for s in self._stores:
                if s.get('store') == store:
                    found = True
                    s['transactions'].append(transaction)
            if not found:
                self._stores.append({
                    'store': store,
                    'transactions': [transaction]
                })

    @classmethod
    def process_line(self, line):
        dt = timezone.datetime.strptime(
            f'{line[1:9]} {line[42:48]}',
            '%Y%m%d %H%M%S',
        )
        return {
            't_type': int(line[0]),
            'date': dt.date(),
            'amount': int(line[9:19])/100,
            'cpf': line[19:30],
            'card': line[30:42],
            'time': dt.time(),
            'store': {
                'owner': line[48:62].rstrip(),
                'name': line[62:81].rstrip(),
            },
        }

    @property
    def stores(self):
        return self._stores
