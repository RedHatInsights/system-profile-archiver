import psycopg2

from system_profile_archiver import config

DELETE_SQL = "DELETE FROM historical_system_profiles WHERE inventory_id = %s"


def delete_by_inventory_id(logger, inventory_id):
    # TODO: re-use connection and add error handling
    db_args = {
        "host": config.DB_HOST,
        "port": config.DB_PORT,
        "database": config.DB_NAME,
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
    }
    logger.info("opening DB connection")
    conn = psycopg2.connect(**db_args)
    cur = conn.cursor()
    logger.info("deleting records for host %s" % inventory_id)
    cur.execute(DELETE_SQL, (inventory_id,))
    # TODO: (audit-log) delete
    conn.commit()
    cur.close()
    conn.close()
    logger.info("closed DB connection")
