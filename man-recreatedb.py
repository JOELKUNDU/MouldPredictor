"""
using this script will purge the entire database, delete the database file and recreate it.
"""

import os
from predictor import db

if __name__ == '__main__':
    os.remove('predictor/data.db')
    db.create_all()
