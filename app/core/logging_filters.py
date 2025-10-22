import logging

class EstabelecimentoContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'estabelecimento_id'):
            record.estabelecimento_id = 'N/A'
        return True