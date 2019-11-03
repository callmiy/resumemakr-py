# -*- coding: utf-8 -*-


def add_fkey(table_name, col, related_table, related_col="id"):
    return f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT {table_name}_{col}_fkey
        FOREIGN KEY ({col})
        REFERENCES {related_table}({related_col})
        ON DELETE CASCADE;
     """


def create_index(table_name, col):
    return f"""
        CREATE INDEX {table_name}_{col}_index
        ON {table_name}({col});
    """
