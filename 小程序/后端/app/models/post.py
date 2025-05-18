from sqlalchemy import Column, Integer, relationship

class Post:
    # 在Post类中添加comments关系
    comments = relationship("Comment", back_populates="post")

    # 确保有comments_count字段
    comments_count = Column(Integer, default=0) 