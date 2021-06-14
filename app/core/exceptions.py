
class CoreEx(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message

    # Переопредление стандартного метода для того, чтобы в текст попадала не только ошибка, но и описание этой ошибки в унаследованных методах
    def __str__(self):
        return self.message

    def name(self):
        return self.__class__


# # # # # # # # # # UniCore # # # # # # # # # # #
class UniCoreUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения: " + message


class UniCoreDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления: " + message


class UniCoreGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения: " + message


class UniCoreGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка: " + message


class UniCoreSomeEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка некоторого действия: " + message


# # # # # # # # # # Common # # # # # # # # # # #
class ObjectNotFound(CoreEx):

    def __init__(self, message):
        self.message = message


class ObjectAlreadyExistsEx(CoreEx):

    def __init__(self, message):
        self.message = message


class WrongIDEx(CoreEx):

    def __init__(self, message):
        self.message = message


class WrongDataEx(CoreEx):

    def __init__(self, message):
        self.message = message


class OuterOperationsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления внешней операции: " + message


class OuterOperationsExecuteEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка выполнения внешней операции: " + message


class OuterOperationsUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения внешней операции: " + message


class OuterOperationsGetStateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения состояния внешней операции: " + message


class GetMethodsEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения метода: " + message


class IdempotentOperationsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления идемпотентной операции: " + message


class IdempotentOperationsUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения идемпотентной операции: " + message


# # # # # # # # # # Payment # # # # # # # # # # #
class PaymentsGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения оплаты: " + message


class PaymentsDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления оплаты: " + message


class PaymentsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления оплаты: " + message


class PaymentsUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения оплаты: " + message


class PaymentsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка оплат: " + message


# # # # # # # # # # Rate # # # # # # # # # # #
class RatesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения тарифа: " + message


class RatesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления тарифа: " + message


class RatesAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления тарифа: " + message


class RatesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения тарифа: " + message


class RatesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка тарифов: " + message


# # # # # # # # # # Notice # # # # # # # # # # #
class NoticesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения уведомления: " + message


class NoticesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления уведомления: " + message


class NoticesAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления уведомления: " + message


class NoticesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения уведомления: " + message


class NoticesReadEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка отметки уведомления прочитанным: " + message


class NoticesAddBulkEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка массового добавления уведомления: " + message


class NoticesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка уведомлений: " + message


# # # # # # # # # # NoticeType # # # # # # # # # # #
class NoticeTypesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения уведомления: " + message


class NoticeTypesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления типа уведомления: " + message


class NoticeTypesAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления типа уведомления: " + message


class NoticeTypesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения типа уведомления: " + message


class NoticeTypesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка типов уведомлений: " + message


class NoticeTypesUserEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка установки уведомлений пользователю: " + message


class NoticeTypesGroupEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка установки уведомлений группе: " + message


# # # # # # # # # # Game # # # # # # # # # # #
class GamesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения игры: " + message


class GamesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления игры: " + message


class GamesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения игры: " + message


class GamesCopyEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка копирования игры: " + message


class GamesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка игр: " + message


class GamesHistoryGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка истории игр: " + message


class GamesHistoryAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления записи об истории игры: " + message


class ProfilesPointsManualGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка ручных результатов профилей: " + message


class ProfilesPointsManualAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления записи о ручном результате профилей: " + message


class ProfilesPointsManualDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления записи о ручном результате профилей: " + message


class ProfilesPointsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка результатов профилей: " + message


class ProfilesSendToScanEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка отправки профиля на сканирование: " + message


# # # # # # # # # # Chat # # # # # # # # # # #
class ChatsGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения чата: " + message


class ChatsDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления чата: " + message


class ChatsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления чата: " + message


class ChatsUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения чата: " + message


class ChatsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка чатов: " + message


# # # # # # # # # # Message # # # # # # # # # # #
class MessagesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения сообщения: " + message


class MessagesGetEx11(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения сообщения: " + message


class MessagesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления сообщения: " + message


class MessagesAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления сообщения: " + message


class MessagesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения сообщения: " + message


class MessagesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка сообщений: " + message


class MessagesReadEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка прочтения сообщения: " + message


class ChatUsersSetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления/удаления пользователя из чата: " + message


# # # # # # # # # # Profile # # # # # # # # # # #
class ProfilesGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения профиля: " + message


class ProfilesDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления профиля: " + message


class ProfilesAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления профиля: " + message


class ProfilesUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения профиля: " + message


class ProfilesGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка профилей: " + message


# # # # # # # # # # Client # # # # # # # # # # #
class ClientsGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения клиента: " + message


class ClientsDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления клиента: " + message


class ClientsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления клиента: " + message


class ClientsUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения клиента: " + message


class ClientsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка клиентов: " + message


class ClientsLockEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка блокировки клиента: " + message


class ClientsTopUpBalanceEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка пополнения баланса клиента: " + message


# # # # # # # # # # Staff # # # # # # # # # # #
class StaffGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения работника: " + message


class StaffDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления работника: " + message


class StaffAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления работника: " + message


class StaffUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения работника: " + message


class StaffGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка работников: " + message


class StaffLockEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка блокировки работника: " + message


class StaffSetGroupEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка установки группы работнику: " + message


class StaffAuthEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка авторизации работника: " + message


class StaffChangePassEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения пароля работника: " + message


class StaffChangeMyPassEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения собственного пароля: " + message


class StaffGetGroupsEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения групп пользователя: " + message


class StaffTestAuthEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка проверки сессии пользователя: " + message


class StaffTestAuthInnerEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка внутренней проверки сессии пользователя: " + message


class StaffLogoutEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка вылогинивания пользователя: " + message


class TokenAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка создания токена: " + message


# # # # # # # # # # Command # # # # # # # # # # #
class CommandsGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения команды: " + message


class CommandsDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления команды: " + message


class CommandsAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления команды: " + message


class CommandsCheckEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка проверки данных для команды: " + message


class CommandsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка команд: " + message


# # # # # # # # # # Worker # # # # # # # # # # #
class WorkersGetEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения воркера: " + message


class WorkersDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления воркера: " + message


class WorkersAddEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка добавления воркера: " + message


class WorkersUpdateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка изменения воркера: " + message


class WorkersActivateEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка активации воркера: " + message


class WorkersGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка воркера: " + message


class TasksGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка тасков: " + message


class TasksDelEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка удаления таска: " + message


class EmailsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка писем: " + message


class LogsGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка логов действий: " + message


class LogServersGetAllEx(CoreEx):

    def __init__(self, message):
        self.message = "Ошибка получения списка логов сервера: " + message
