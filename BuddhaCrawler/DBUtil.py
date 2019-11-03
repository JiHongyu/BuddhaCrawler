from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, TEXT, text
import time


# url="mysql+pymysql://[账号]:[密码]@[主机]:[端口]/[数据库]?charset=utf8"

class DBUtil:

    def __init__(self, dbUrl):
        engine = create_engine(
            dbUrl,
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        )
        self.Session = sessionmaker(bind=engine)

    def getSession(self):
        return self.Session()


dbUtil = DBUtil('mysql+pymysql://root:123456@localhost:3306/jhy?charset=utf8mb4')

Base = declarative_base()


class CollectWebInfo(Base):
    __tablename__ = 'collect_web_info_t'
    id = Column('id', BigInteger, primary_key=True)
    url = Column('url', String(256), nullable=False)
    hostUrl = Column('host_url', String(256), nullable=False)
    city = Column('city', String(256), nullable=True)
    articleTitle = Column('article_title', String(256), nullable=True)
    articleTag = Column('article_tag', String(128), nullable=True)
    articleText = Column('article_text', TEXT, nullable=True)
    publishTime = Column('publish_time', TIMESTAMP(True), nullable=True)
    coverPictureUrl = Column('cover_picture_url', String(256), nullable=True)
    articlePictureUrls = Column('article_picture_urls', TEXT, nullable=True)
    articleVideoUrls = Column('article_video_urls', TEXT, nullable=True)
    createTime = Column('create_time', TIMESTAMP(True), nullable=False)


if __name__ == '__main__':
    c = CollectWebInfo()
    c.url = '12434'
    c.hostUrl = '324234'
    c.city = '成都'
    c.articleText = '34'
    c.articleTitle = '324235'
    c.publishTime = 0
    c.coverPictureUrl = '32423'
    c.articlePictureUrls = '35424'
    c.articleVideoUrls = '324234'
    c.createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    session = dbUtil.getSession()
    session.add(c)
    session.commit()
