from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from datetime import datetime
from backend.app.database import User

# =================== 基础CRUD操作 ===================

# 创建用户
def create_user(db: Session, username: str, password: str):
    """创建新用户"""
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 获取所有用户
def get_all_users(db: Session):
    """获取所有用户"""
    return db.query(User).all()

# 根据ID获取用户
def get_user_by_id(db: Session, user_id: int):
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()

# 根据用户名获取用户
def get_user_by_username(db: Session, username: str):
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()

# 更新用户
def update_user(db: Session, user_id: int, username: str = None, password: str = None):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if username:
            user.username = username
        if password:
            user.password = password
        db.commit()
        db.refresh(user)
    return user

# 删除用户
def delete_user(db: Session, user_id: int):
    """删除用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

# =================== 过滤操作 ===================

# 根据用户名模糊搜索
def search_users_by_username(db: Session, keyword: str):
    """根据用户名关键字搜索用户"""
    return db.query(User).filter(User.username.like(f"%{keyword}%")).all()

# 根据创建时间范围查询
def get_users_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    """根据创建时间范围获取用户"""
    return db.query(User).filter(
        and_(User.created_at >= start_date, User.created_at <= end_date)
    ).all()

# 多条件查询
def get_users_with_multiple_conditions(db: Session, username: str = None, min_id: int = None):
    """多条件查询用户"""
    query = db.query(User)
    
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    if min_id:
        query = query.filter(User.id >= min_id)
    
    return query.all()

# =================== 排序操作 ===================

# 按ID升序获取用户
def get_users_order_by_id_asc(db: Session):
    """按ID升序获取用户"""
    return db.query(User).order_by(asc(User.id)).all()

# 按ID降序获取用户
def get_users_order_by_id_desc(db: Session):
    """按ID降序获取用户"""
    return db.query(User).order_by(desc(User.id)).all()

# 按创建时间排序获取用户
def get_users_order_by_created_time(db: Session, desc_order: bool = True):
    """按创建时间排序获取用户"""
    if desc_order:
        return db.query(User).order_by(desc(User.created_at)).all()
    else:
        return db.query(User).order_by(asc(User.created_at)).all()

# =================== 分组和聚合操作 ===================

# 获取用户总数
def get_user_count(db: Session):
    """获取用户总数"""
    return db.query(User).count()

# 按用户名长度分组统计
def get_user_count_by_username_length(db: Session):
    """按用户名长度分组统计"""
    return db.query(
        func.length(User.username).label('username_length'),
        func.count(User.id).label('user_count')
    ).group_by(func.length(User.username)).all()

# 获取最早注册的用户
def get_oldest_user(db: Session):
    """获取最早注册的用户"""
    return db.query(User).order_by(asc(User.created_at)).first()

# 获取最新注册的用户
def get_newest_user(db: Session):
    """获取最新注册的用户"""
    return db.query(User).order_by(desc(User.created_at)).first()

# =================== 分页操作 ===================

# 分页获取用户
def get_users_with_pagination(db: Session, page: int = 1, page_size: int = 10):
    """分页获取用户"""
    offset = (page - 1) * page_size
    return db.query(User).offset(offset).limit(page_size).all()

# =================== 批量操作 ===================

# 批量创建用户
def create_users_bulk(db: Session, user_data_list: list):
    """批量创建用户"""
    users = []
    for data in user_data_list:
        user = User(username=data['username'], password=data['password'])
        users.append(user)
    
    db.add_all(users)
    db.commit()
    for user in users:
        db.refresh(user)
    return users

# 批量删除用户
def delete_users_bulk(db: Session, user_ids: list):
    """批量删除用户"""
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    for user in users:
        db.delete(user)
    db.commit()
    return len(users)

# =================== 复杂查询示例 ===================

# 获取指定ID范围的用户并按创建时间排序
def get_users_in_id_range_ordered(db: Session, min_id: int, max_id: int, limit: int = 10):
    """获取指定ID范围的用户并按创建时间排序"""
    return db.query(User).filter(
        and_(User.id >= min_id, User.id <= max_id)
    ).order_by(desc(User.created_at)).limit(limit).all()

# 使用或条件查询
def get_users_with_or_condition(db: Session, username: str, user_id: int):
    """使用或条件查询用户"""
    return db.query(User).filter(
        or_(User.username == username, User.id == user_id)
    ).all()

# 统计今天注册的用户数量
def get_today_user_count(db: Session):
    """统计今天注册的用户数量"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(User).filter(User.created_at >= today).count()