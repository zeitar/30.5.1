import pytest


@pytest.fixture()
def after_test():
    yield
    print('test ended')


#def chrome_options(chrome_options):
 #   chrome_options.binary_location = '/Program Files/Google/Chrome/'
  #  chrome_options.add_extension('/path/to/extension.crx')
   # chrome_options.add_argument('--kiosk')
    #return chrome_options