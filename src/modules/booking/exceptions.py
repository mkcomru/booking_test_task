class BookingNotFoundError(Exception):
    """Бронь c указанным id не найдена."""

    pass


class SlotAlreadyBookedError(Exception):
    """Слот на выбранное дату и время уже занят."""

    pass
