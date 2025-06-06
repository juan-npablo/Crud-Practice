from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from core.security import decode_access_token
from db.session import SessionLocal
from db.models.user import User

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rutas públicas que no requieren autenticación
        public_paths = [
            "/v1/auth/login",
            "/v1/auth/register",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]

        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Verificar token
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se encuentra autenticado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = token.split(" ")[1]
        try:
            payload = decode_access_token(token)
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        # Crear una sesión de DB correctamente
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            request.state.user = user
        finally:
            db.close()

        return await call_next(request)
