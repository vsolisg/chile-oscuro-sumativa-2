from django.db.backends.mysql.base import DatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# Desactiva la verificación de versión de MariaDB
DatabaseWrapper.check_database_version_supported = lambda self: None

# Desactiva el uso de la cláusula RETURNING incompatible con MariaDB 10.4
DatabaseFeatures.can_return_columns_from_insert = False