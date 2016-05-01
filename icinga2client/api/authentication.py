from ..helpers.data import dict_has_all


class AuthenticationManager:
    def authenticate_password(self, args):
        if not dict_has_all(args, ['username', 'password']):
            raise ValueError(
                'password authentication requires a username and password'
            )

        return {
            'auth': (args['username'], args['password'])
        }

    def authenticate(self, method='password', **kwargs):
        if method == 'password':
            return self.authenticate_password(kwargs)
        elif method == 'certificate':
            raise NotImplementedError('TODO')
        else:
            raise ValueError('TODO')
