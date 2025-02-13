
class EventNotifier:
    Default_Even_Method = "event"

    def __init__(self):
        self._subscribers = set()

    def subscribe(self, subscriber):
        """Añade un suscriptor a la lista si no está ya registrado."""
        if subscriber not in self._subscribers:
            self._subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        """Elimina un suscriptor de la lista."""
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify(self, nombre_metodo, param = None):
        """Notifica un evento a todos los suscriptores."""
        for subscriber in self._subscribers:
            if hasattr(subscriber, EventNotifier.Default_Even_Method):
                getattr(subscriber, EventNotifier.Default_Even_Method)(nombre_metodo, param)
            else:
                getattr(subscriber, nombre_metodo)(param)


class Eventos(object):
    """
    Fachada de todos los métodos específicos para los distintos tipos de eventos.
    """

    def __init__(self):
        self._en_cambio_loc = EventNotifier()
        self._en_reinicia = EventNotifier()
        self._en_fin_comando = EventNotifier()

    ## No lo us, utilizo RENICIA en su lugar ####

    def sub_cambio_loc(self, subscriber):
        self._en_cambio_loc.subscribe(subscriber)

    def unsub_cambio_loc(self, subscriber):
        self._en_cambio_loc.unsubscribe(subscriber)

    def cambio_loc(self, nueva_loc):
        self._en_cambio_loc.notify("cambio_loc", nueva_loc)


    ## Cuando un comando devuelve RENICIA (se vuelev a mostrar la loc) ####

    def sub_reinicia(self, subscriber):
        self._en_reinicia.subscribe(subscriber)

    def unsub_reinicia(self, subscriber):
        self._en_reinicia.unsubscribe(subscriber)

    def reinicia(self, nueva_loc):
        self._en_reinicia.notify("reinicia", nueva_loc)

    ## Después de procesar un comando con independencia del reusltado ####

    def sub_fin_comando(self, subscriber):
        self._en_fin_comando.subscribe(subscriber)

    def unsub_fin_comando(self, subscriber):
        self._en_fin_comando.unsubscribe(subscriber)

    def fin_comando(self, comando):
        self._en_fin_comando.notify("fin_comando", comando)


class Timer:

    def __init__(self, event_name, limit, callback):
        self._event_name = event_name
        self._limit = limit
        self._callback = callback
        self._counter = 0

    def event(self, event_name, param):
        if event_name is not self._event_name:
            return
        print("Event: ", event_name)
        self._counter+=1
        if self._counter < self._limit:
            return
        print(f"Counter: {self._counter} limit: {self._limit}")
        self._callback()



# Mini test
# Llevar a una prueba automática.

class Cambio:
    def cambio_loc(self, nueva_loc):
        print("Nueva loc: ", nueva_loc)



if __name__ == '__main__':
    t = Timer("cambio_loc", 3, None)
    print (hasattr(t, EventNotifier.Default_Even_Method))
    n_loc = "nueva loc"

    ev = Eventos()
    c = Cambio()
    ev.sub_cambio_loc(c)
    ev.cambio_loc(n_loc)
    ev.unsub_cambio_loc(c)
    ev.cambio_loc(n_loc)
    ev.sub_cambio_loc(c)
    ev.sub_cambio_loc(Cambio())
    ev.sub_cambio_loc(t)
    ev.cambio_loc(n_loc)
