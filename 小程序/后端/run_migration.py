"""
运行数据库迁移的脚本
"""

import os
import importlib.util
from pathlib import Path

def run_migrations():
    """运行migrations目录下的所有迁移脚本"""
    
    migrations_dir = Path(__file__).parent / "migrations"
    print(f"正在寻找迁移文件，路径: {migrations_dir}")
    
    # 检查目录是否存在
    if not migrations_dir.exists():
        print(f"迁移目录不存在: {migrations_dir}")
        return
    
    # 获取所有Python文件
    migration_files = [f for f in migrations_dir.glob("*.py") if f.is_file()]
    print(f"找到 {len(migration_files)} 个迁移文件")
    
    # 按文件名排序
    migration_files.sort()
    
    for migration_file in migration_files:
        # 动态导入模块
        print(f"\n正在运行迁移: {migration_file.name}")
        module_name = migration_file.stem
        spec = importlib.util.spec_from_file_location(module_name, migration_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 运行升级函数
        if hasattr(module, "upgrade"):
            print(f"执行 {module_name}.upgrade()")
            module.upgrade()
        else:
            print(f"警告: {module_name} 没有 upgrade() 函数")

if __name__ == "__main__":
    run_migrations()
    print("\n所有迁移已完成") 