import psycopg2
from . import logger


def update_pleroma_objects(conn, cur, tid, odate):
    query_update_objects = """
        update objects
        set data=jsonb_set(data, '{published}', %s,false),
        inserted_at=%s,
        updated_at=%s
        where data->>'content' like %s;
        """
    cur.execute(query_update_objects,
                ('"' + odate + '"', odate, odate, '%' + tid + '%'))
    conn.commit()
    count = cur.rowcount
    if count > 0:
        # Retrieve object_id of the object(s) that got updated and update data, inserted_at, updated_at
        # fields of activities table
        query_get_object_id = """select data->>'id' from objects where data->>'content' like %s;"""
        cur.execute(query_get_object_id, ('%' + tid + '%',))
        oid_list = cur.fetchall()
        for oid in oid_list:
            update_pleroma_activities(conn, cur, oid[0], odate)


def update_pleroma_activities(conn, cur, oid, odate):
    query_update_activities = """
        update activities
        set data=jsonb_set(data, '{published}', %s,false),
        inserted_at=%s,
        updated_at=%s
        where data->>'object' = %s;
        """
    cur.execute(query_update_activities,
                ('"' + odate + '"', odate, odate, oid))
    conn.commit()
    count = cur.rowcount


def update_db(twitter_id, original_date):
    # Establish database connection
    connection = cursor = None
    try:
        connection = psycopg2.connect(host="localhost", port="5432",
                                      user="pleroma", password="theadmin",
                                      database="pleroma")
        cursor = connection.cursor()
        if connection:
            update_pleroma_objects(connection, cursor, twitter_id, original_date)
        else:
            logger.info(f"Error establishing database connection.")
    except (Exception, psycopg2.Error) as error:
        logger.info(f"Error updating database:\n", error)
    finally:
        # Closing database connection
        if connection:
            cursor.close()
            connection.close()
