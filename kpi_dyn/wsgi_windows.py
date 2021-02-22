import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
site.addsitedir("C:\Users\stg_hamidou54319\Desktop\DIGIDEX\env\Scripts")

# Add the app's directory to the PYTHONPATH 
sys.path.append('C:\Users\stg_hamidou54319\Desktop\DIGIDEX\kpi_dyn_sane') 
sys.path.append('C:\Users\stg_hamidou54319\Desktop\DIGIDEX\kpi_dyn_sane\kpi_dyn')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'kpi_dyn.settings' 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kpi_dyn.settings")  
 
application = get_wsgi_application()