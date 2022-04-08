from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from os.path import join, dirname, realpath


class CassandraConnect:
        @staticmethod
        def conn():
                UPLOADS_PATH = join(dirname(realpath(__file__)), 'secure-connect-test.zip')
                cloud_config = {
                        'secure_connect_bundle': UPLOADS_PATH
                }
                auth_provider = PlainTextAuthProvider('jeetljCSgUyjWZoZhAhbqSrt',
                                                      't5r7I3gRs7uZBXGB7NvfcrqRKamykksyX,j,ZoZYxw6BZS8YZ03,YBpJZ_aYrBvQnjxrSL_3ECY709RoXDWD49NlxpTc4i2yU-nyKhQR3m.JC_nbI9U_hLZS,AhMa9zR')
                cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
                session = cluster.connect()
                return session

