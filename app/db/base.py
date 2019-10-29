# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from db_models.peso import Peso  # noqa
from db_models.relation import Relation  # noqa
from db_models.reporter import Reporter  # noqa
