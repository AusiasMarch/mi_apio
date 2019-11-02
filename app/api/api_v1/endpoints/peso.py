from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from api.utils.db import get_db
from models.peso import (
    PesoCreate,
)
from models.msg import Msg

from core import jwt
from starlette.authentication import AuthenticationError
from core import config

router = APIRouter()


@router.post("/insert", response_model=Msg, status_code=202)
def insert_peso(
    *,
    body: dict,
    db_session: Session = Depends(get_db),
):

    id_token = body['originalDetectIntentRequest']['payload']['user']['idToken']
    decoded_token = jwt.decode_google_token(id_token)
    if decoded_token['aud'] != config.GOOGLE_CLIENTID:
        raise AuthenticationError('Invalid Google Client ID.')
    if decoded_token['iss'] != config.GOOGLE_ISS:
        raise AuthenticationError('Invalid Google Token ID iss.')
    user = crud.user.get_by_email(db_session=db_session, email=decoded_token['email'])
    if not user.can_report():
        return {
            "msg": "The user is not allowed to report"
        }
    
    
    kilos = body['queryResult']['parameters']['n_kilos']
    gramos = body['queryResult']['parameters']['n_gramos']
    peso_in = PesoCreate(
        user_id = user.id,
        query_text=body['queryResult']['queryText'],
        kilos=kilos if kilos else 0,
        gramos=gramos if gramos else 0,
    )
    """
    Call the process that inserts a peso in the DB.
    """

    crud.peso.create(db_session=db_session, peso_in=peso_in)
    return {
        "msg": "The peso has been inserted."
    }


# @router.get("/info", response_model=List[FitInfoDB], status_code=200)
# def get_fit_info(
#     offset: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Paginated information about the fit history.
#     """
#     return crud.fit.read_multi(db_session=db, limit=limit, offset=offset)
#
#
# @router.get("/main", response_model=FitInfoDB, status_code=200)
# def get_main_fit(
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Returns the actual main model fit, which is used as the default model for prediction
#     """
#     return crud.fit.read_main(db_session=db)
#
#
# @router.put("/main", response_model=FitInfoDB, status_code=200)
# def update_main_fit(
#     info_in: MainFit,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Updates the main model fit given an existing model ID
#     """
#     if not crud.fit.read(db_session=db, fit_id=info_in.fit_id):
#         raise HTTPException(status_code=404)
#     return _update_main_fit(db=db, fit_id=info_in.fit_id)
#
#
# @router.get("/{fit_id}/info", response_model=List[FitInfoDB], status_code=200)
# def get_fit_info(
#     fit_id: int,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Returns paginated information about the fit history.
#     If ID is informed the result is filtered by ID.
#     """
#     return crud.fit.read(db_session=db, fit_id=fit_id)
#
#
# @router.get("/{fit_id}/download", status_code=200)
# def get_fit(
#     fit_id: int,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     fit = crud.fit.read(db, fit_id=fit_id)
#     if fit is None:
#         raise HTTPException(status_code=404)
#     models = crud.model.read_multi_by_fit(db_session=db, fit_id=fit_id)
#     filename = "fit_{}.zip".format(fit.id)
#     zip_file = generate_zip(
#         ["model_{}.pkl".format(model.id) for model in models],
#         [model.model for model in models],
#     )
#     return Response(
#         zip_file,
#         media_type="application/octet-stream",
#         headers={"Content-Disposition": 'attachment; filename="{}"'.format(filename)},
#     )
#
#
# def _update_main_fit(db: Session, fit_id: int):
#     """
#     Updates the main fit in DB
#     :param db: Database session
#     :param fit_id: New main fit fit ID
#     :return: new main fit as a DB object
#     """
#     main_fits = crud.fit.read_main(db_session=db)
#     updated = datetime.now()
#     for fit in main_fits:
#         crud.fit.update(
#             db, fit_id=fit.id, fit_in=FitInfoDBUpdate(
#                 updated=updated,
#                 is_main=False,
#             )
#         )
#     new_main = crud.fit.update(
#         db, fit_id=fit_id, fit_in=FitInfoDBUpdate(
#             updated=updated,
#             is_main=True,
#         )
#     )
#     return new_main
