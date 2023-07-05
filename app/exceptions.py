from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrectCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильная почта или пароль",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует"
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена"
)

UserNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров"
)

BookingNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Бронирование не найдено"
)

TooLongDatePeriodException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Слишком длинный период бронирования (больше 30 дней)"
)

DateFromBeforeDateToException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Дата начала бронирования больше или равна даты окончания"
)