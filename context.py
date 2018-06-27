import logging
import os
import sqlite3
from collections import namedtuple


class Context:
    __instance = None

    _DATABASE_NAME = 'Comment.db'
    if os.path.exists(_DATABASE_NAME):
        __conn = sqlite3.connect(_DATABASE_NAME)
    else:
        __conn = sqlite3.connect(_DATABASE_NAME)
        __conn.cursor().executescript(open('init_database.sql', 'r', encoding="utf-8").read())
        __conn.commit()

    logging.basicConfig(filename='logs/context_errors.log', filemode='a', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Context.__instance is None:
            Context()
        return Context.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Context.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Context.__instance = self

    @classmethod
    def get_all_regions(cls):
        """Получение всех регионов"""
        cls.__conn.row_factory = sqlite3.Row
        cur = cls.__conn.cursor()
        try:
            cur.execute('SELECT * FROM Region')
            rows = cur.fetchall()
            return {row['id']: row['region'] for row in rows}
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def get_cities_by_region_id(cls, region_id):
        """Получение словоря городов по идентификатору региона"""
        cur = cls.__conn.cursor()
        try:
            cur.execute('SELECT * FROM City WHERE City.region_id = ?', (int(region_id),))
            rows = cur.fetchall()
            return {row['id']: row['city'] for row in rows}
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def add_comment(cls, surname, name, comment, city_id, patronymic='', contact_number='', e_mail=''):
        """Добавление коментария"""
        sql = '''INSERT INTO Comment (surname, name, patronymic, city_id, contact_number, e_mail, comment) 
                VALUES (?, ?, ?, ?, ? , ?, ?)
            '''
        cur = cls.__conn.cursor()
        try:
            cur.execute(sql, (surname, name, patronymic, city_id, contact_number, e_mail, comment))
            cls.__conn.commit()
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def get_all_comments(cls):
        """Получение всех коментариев"""
        Comment = namedtuple('Comment',
                             ['id', 'surname', 'name', 'patronymic', 'city_id', 'contact_number', 'e_mail', 'comment'])

        cur = cls.__conn.cursor()
        try:
            cur.execute('''SELECT co.id, co.surname, co.name, co.patronymic, ci.city, co.contact_number, co.e_mail, co.comment
                            FROM COMMENT AS co
                            INNER JOIN City AS ci ON (co.city_id = ci.id)''')
            rows = cur.fetchall()
            return [Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def delete_comment_by_id(cls, comment_id):
        """Удаление коментария"""
        cur = cls.__conn.cursor()
        try:
            cur.execute('DELETE FROM  Comment WHERE id = ?', (int(comment_id),))
            cls.__conn.commit()
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def statistics(cls):
        """  Получение регионов у которых количество комментариев больше 5"""

        Statistic = namedtuple('Statistic', ['id', 'region', 'count_comments'])

        sql = '''SELECT r.id, r.region, count( * ) AS count_comments
                  FROM Region AS r
                       INNER JOIN City AS c ON (r.id = c.region_id) 
                       INNER JOIN Comment AS cm ON (c.id = cm.city_id) 
                 GROUP BY r.region
                HAVING count_comments > 5
                '''
        cur = cls.__conn.cursor()

        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return [Statistic(row[0], row[1], row[2]) for row in rows]
        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()

    @classmethod
    def city_statistics_by_region(cls, region_id):
        sql = '''SELECT c.city, count( * ) AS count_comments
                    FROM City AS c 
                    INNER JOIN Comment AS cm ON (c.id = cm.city_id) 
                 WHERE c.region_id = ?
                 GROUP BY c.id
            '''

        cur = cls.__conn.cursor()
        try:
            cur.execute(sql, (region_id,))
            rows = cur.fetchall()

            return {row[0]: row[1] for row in rows}

        except Exception as ex:
            logging.exception(ex)
        finally:
            cur.close()
