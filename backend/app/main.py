from fastapi import FastAPI, Request, Response, HTTPException, status
from chainlit.utils import mount_chainlit
from chainlit.user import User
from chainlit.data import get_data_layer
from chainlit.auth import create_jwt

from fastapi.responses import RedirectResponse

_cookie_samesite = "none"
_auth_cookie_name = "access_token"

app = FastAPI()


@app.get("/app")
async def read_main():
    return {"message": "Hello World from main app"}


def set_auth_cookie(request: Request, response: Response, token: str):
    """
    Helper function to set the authentication cookie with secure parameters
    and remove any leftover chunks from a previously larger token.
    """

    _chunk_size = 3000

    existing_cookies = {
        k for k in request.cookies.keys() if k.startswith(_auth_cookie_name)
    }

    if len(token) > _chunk_size:
        chunks = [token[i : i + _chunk_size] for i in range(0, len(token), _chunk_size)]

        for i, chunk in enumerate(chunks):
            k = f"{_auth_cookie_name}_{i}"

            response.set_cookie(
                key=k,
                value=chunk,
                httponly=True,
                secure=True,
                samesite=_cookie_samesite,
            )

            existing_cookies.discard(k)
    else:
        # Default (shorter cookies)
        response.set_cookie(
            key=_auth_cookie_name,
            value=token,
            httponly=True,
            secure=True,
            samesite=_cookie_samesite,
        )

        existing_cookies.discard(_auth_cookie_name)

    # Delete remaining prior cookies/cookie chunks
    for k in existing_cookies:
        response.delete_cookie(key=k, path="/")


@app.get("/cc")
async def auth_user(request: Request):
    existing_cookies = {
        k for k in request.cookies.keys() 
    }

    print('existing_cookies', existing_cookies)

    user = User(
        identifier="adminer", metadata={"role": "admin", "provider": "credentials"}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credentialssignin",
        )

    # If a data layer is defined, attempt to persist user.
    if data_layer := get_data_layer():
        try:
            await data_layer.create_user(user)
        except Exception as e:
            # Catch and log exceptions during user creation.
            # TODO: Make this catch only specific errors and allow others to propagate.
            print(f"Error creating user: {e}")

    access_token = create_jwt(user)

    response =  RedirectResponse(
    
        url='/chat',
        status_code=302
    )

    set_auth_cookie(request, response, access_token)

    return response


mount_chainlit(app=app, target="app/app.py", path="/chat")
