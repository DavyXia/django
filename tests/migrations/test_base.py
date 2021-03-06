from django.test import TransactionTestCase
from django.db import connection


class MigrationTestBase(TransactionTestCase):
    """
    Contains an extended set of asserts for testing migrations and schema operations.
    """

    available_apps = ["migrations"]

    def assertTableExists(self, table):
        self.assertIn(table, connection.introspection.get_table_list(connection.cursor()))

    def assertTableNotExists(self, table):
        self.assertNotIn(table, connection.introspection.get_table_list(connection.cursor()))

    def assertColumnExists(self, table, column):
        self.assertIn(column, [c.name for c in connection.introspection.get_table_description(connection.cursor(), table)])

    def assertColumnNotExists(self, table, column):
        self.assertNotIn(column, [c.name for c in connection.introspection.get_table_description(connection.cursor(), table)])

    def assertColumnNull(self, table, column):
        self.assertEqual([c.null_ok for c in connection.introspection.get_table_description(connection.cursor(), table) if c.name == column][0], True)

    def assertColumnNotNull(self, table, column):
        self.assertEqual([c.null_ok for c in connection.introspection.get_table_description(connection.cursor(), table) if c.name == column][0], False)

    def assertIndexExists(self, table, columns, value=True):
        self.assertEqual(
            value,
            any(
                c["index"]
                for c in connection.introspection.get_constraints(connection.cursor(), table).values()
                if c['columns'] == list(columns)
            ),
        )

    def assertIndexNotExists(self, table, columns):
        return self.assertIndexExists(table, columns, False)
