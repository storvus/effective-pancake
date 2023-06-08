import inspect

import bottle
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

# PluginError is defined to bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class SQLAlchemyPlugin(object):

    name = 'sqlalchemy'
    api = 2

    def __init__(self, engine, metadata=None,
                 keyword='db', commit=True, create=False, use_kwargs=False, create_session=None):
        '''
        :param engine: SQLAlchemy engine created with `create_engine` function
        :param metadata: SQLAlchemy metadata. It is required only if `create=True`
        :param keyword: Keyword used to inject session database in a route
        :param create: If it is true, execute `metadata.create_all(engine)`
               when plugin is applied
        :param commit: If it is true, commit changes after route is executed.
        :param use_kwargs: plugin inject session database even if it is not
               explicitly defined, using **kwargs argument if defined.
        :param create_session: SQLAlchemy session maker created with the
                'sessionmaker' function. Will create its own if undefined.
        '''
        self.engine = engine
        if create_session is None:
            create_session = sessionmaker()
        self.create_session = create_session
        self.metadata = metadata
        self.keyword = keyword
        self.create = create
        self.commit = commit
        self.use_kwargs = use_kwargs

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument and check if metadata is available.'''
        for other in app.plugins:
            if not isinstance(other, SQLAlchemyPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another SQLAlchemy plugin with " \
                                         "conflicting settings (non-unique keyword).")
            elif other.name == self.name:
                self.name += '_%s' % self.keyword
        if self.create and not self.metadata:
            raise bottle.PluginError('Define metadata value to create database.')

    def apply(self, callback, route):
        # hack to support bottle v0.9.x
        config = route.config
        _callback = route.callback

        if "sqlalchemy" in config:  # support for configuration before `ConfigDict` namespaces
            g = lambda key, default: config.get('sqlalchemy', {}).get(key, default)
        else:
            g = lambda key, default: config.get('sqlalchemy.' + key, default)

        keyword = g('keyword', self.keyword)
        create = g('create', self.create)
        commit = g('commit', self.commit)
        use_kwargs = g('use_kwargs', self.use_kwargs)

        parameters = inspect.signature(_callback).parameters
        accept_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD
                            for p in parameters.values())

        if not ((use_kwargs and accept_kwargs) or keyword in parameters):
            return callback

        if create:
            self.metadata.create_all(self.engine)

        def wrapper(*args, **kwargs):
            kwargs[keyword] = session = self.create_session(bind=self.engine)
            try:
                rv = callback(*args, **kwargs)
                if commit:
                    session.commit()
            except (SQLAlchemyError, bottle.HTTPError):
                session.rollback()
                raise
            except bottle.HTTPResponse:
                if commit:
                    session.commit()
                raise
            finally:
                if isinstance(self.create_session, ScopedSession):
                    self.create_session.remove()
                else:
                    session.close()
            return rv

        return wrapper


Plugin = SQLAlchemyPlugin
