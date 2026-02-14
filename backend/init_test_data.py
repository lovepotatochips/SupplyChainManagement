# -*- coding: utf-8 -*-
"""
厦门建发集团供应链管理系统测试数据初始化脚本
基于真实业务场景创建测试数据
"""
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    Menu, User, Role, Permission, UserRole, RolePermission,
    Department, Supplier, Customer,
    Product, ProductCategory, Warehouse, StockRecord,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Payment, Bill, Account, CostCenter,
    WorkflowDefinition, WorkflowInstance, WorkflowLog
)

random.seed(42)

DEPARTMENTS = [
    {"name": "厦门建发集团总部", "code": "HO", "parent_id": None, "sort_order": 1, "leader": "黄文洲", "phone": "0592-2268888", "address": "厦门市思明区环岛东路1699号建发国际大厦"},
    {"name": "供应链运营事业部", "code": "SCM", "parent_id": 1, "sort_order": 1, "leader": "王志兵", "phone": "0592-2268001", "address": "厦门市思明区环岛东路1699号建发国际大厦18层"},
    {"name": "钢铁供应链中心", "code": "STEEL", "parent_id": 2, "sort_order": 1, "leader": "张明辉", "phone": "0592-2268011", "address": "厦门市思明区环岛东路1699号建发国际大厦18层"},
    {"name": "纸业供应链中心", "code": "PAPER", "parent_id": 2, "sort_order": 2, "leader": "李建国", "phone": "0592-2268012", "address": "厦门市思明区环岛东路1699号建发国际大厦19层"},
    {"name": "汽车供应链中心", "code": "AUTO", "parent_id": 2, "sort_order": 3, "leader": "陈伟强", "phone": "0592-2268013", "address": "厦门市思明区环岛东路1699号建发国际大厦20层"},
    {"name": "农产品供应链中心", "code": "AGRI", "parent_id": 2, "sort_order": 4, "leader": "林志远", "phone": "0592-2268014", "address": "厦门市思明区环岛东路1699号建发国际大厦21层"},
    {"name": "财务部", "code": "FIN", "parent_id": 1, "sort_order": 2, "leader": "吴雅芳", "phone": "0592-2268002", "address": "厦门市思明区环岛东路1699号建发国际大厦12层"},
    {"name": "采购管理部", "code": "PUR", "parent_id": 1, "sort_order": 3, "leader": "郑国华", "phone": "0592-2268003", "address": "厦门市思明区环岛东路1699号建发国际大厦15层"},
    {"name": "仓储物流部", "code": "WMS", "parent_id": 1, "sort_order": 4, "leader": "刘德明", "phone": "0592-2268004", "address": "厦门市海沧区建发物流园"},
    {"name": "销售管理部", "code": "SALES", "parent_id": 1, "sort_order": 5, "leader": "周晓燕", "phone": "0592-2268005", "address": "厦门市思明区环岛东路1699号建发国际大厦16层"},
    {"name": "信息技术部", "code": "IT", "parent_id": 1, "sort_order": 6, "leader": "赵志强", "phone": "0592-2268006", "address": "厦门市思明区环岛东路1699号建发国际大厦8层"},
    {"name": "人力资源部", "code": "HR", "parent_id": 1, "sort_order": 7, "leader": "孙丽华", "phone": "0592-2268007", "address": "厦门市思明区环岛东路1699号建发国际大厦10层"},
    {"name": "审计合规部", "code": "AUDIT", "parent_id": 1, "sort_order": 8, "leader": "黄志刚", "phone": "0592-2268008", "address": "厦门市思明区环岛东路1699号建发国际大厦11层"},
]

ROLES = [
    {"name": "超级管理员", "code": "super_admin", "description": "系统最高权限管理员"},
    {"name": "部门经理", "code": "dept_manager", "description": "部门负责人，可审批本部门业务"},
    {"name": "采购专员", "code": "purchaser", "description": "负责采购订单创建和跟进"},
    {"name": "销售专员", "code": "sales", "description": "负责销售订单创建和跟进"},
    {"name": "仓库管理员", "code": "warehouse_keeper", "description": "负责库存管理和出入库操作"},
    {"name": "财务专员", "code": "finance", "description": "负责财务付款和账单管理"},
    {"name": "普通员工", "code": "employee", "description": "普通员工基础权限"},
]

USERS = [
    {"username": "admin", "real_name": "系统管理员", "email": "admin@cnd.com", "phone": "13800138001", "department_id": 1, "is_superuser": True},
    {"username": "huangwenzhou", "real_name": "黄文洲", "email": "huangwenzhou@cnd.com", "phone": "13906001001", "department_id": 1, "is_superuser": False},
    {"username": "wangzhibing", "real_name": "王志兵", "email": "wangzhibing@cnd.com", "phone": "13906001002", "department_id": 2, "is_superuser": False},
    {"username": "zhangminghui", "real_name": "张明辉", "email": "zhangminghui@cnd.com", "phone": "13906001003", "department_id": 3, "is_superuser": False},
    {"username": "lijianguo", "real_name": "李建国", "email": "lijianguo@cnd.com", "phone": "13906001004", "department_id": 4, "is_superuser": False},
    {"username": "chenweiqiang", "real_name": "陈伟强", "email": "chenweiqiang@cnd.com", "phone": "13906001005", "department_id": 5, "is_superuser": False},
    {"username": "linzhiyuan", "real_name": "林志远", "email": "linzhiyuan@cnd.com", "phone": "13906001006", "department_id": 6, "is_superuser": False},
    {"username": "wuyafang", "real_name": "吴雅芳", "email": "wuyafang@cnd.com", "phone": "13906001007", "department_id": 7, "is_superuser": False},
    {"username": "zhengguohua", "real_name": "郑国华", "email": "zhengguohua@cnd.com", "phone": "13906001008", "department_id": 8, "is_superuser": False},
    {"username": "liudeming", "real_name": "刘德明", "email": "liudeming@cnd.com", "phone": "13906001009", "department_id": 9, "is_superuser": False},
    {"username": "zhouxiaoyan", "real_name": "周晓燕", "email": "zhouxiaoyan@cnd.com", "phone": "13906001010", "department_id": 10, "is_superuser": False},
    {"username": "zhaoziqiang", "real_name": "赵志强", "email": "zhaoziqiang@cnd.com", "phone": "13906001011", "department_id": 11, "is_superuser": False},
    {"username": "sunlihua", "real_name": "孙丽华", "email": "sunlihua@cnd.com", "phone": "13906001012", "department_id": 12, "is_superuser": False},
    {"username": "huangzhigang", "real_name": "黄志刚", "email": "huangzhigang@cnd.com", "phone": "13906001013", "department_id": 13, "is_superuser": False},
    {"username": "caigou01", "real_name": "陈思远", "email": "chensiyuan@cnd.com", "phone": "13906002001", "department_id": 8, "is_superuser": False},
    {"username": "caigou02", "real_name": "林小燕", "email": "linxiaoyan@cnd.com", "phone": "13906002002", "department_id": 8, "is_superuser": False},
    {"username": "caigou03", "real_name": "王建华", "email": "wangjianhua@cnd.com", "phone": "13906002003", "department_id": 8, "is_superuser": False},
    {"username": "xiaoshou01", "real_name": "张晓东", "email": "zhangxiaodong@cnd.com", "phone": "13906003001", "department_id": 10, "is_superuser": False},
    {"username": "xiaoshou02", "real_name": "李美玲", "email": "limeiling@cnd.com", "phone": "13906003002", "department_id": 10, "is_superuser": False},
    {"username": "xiaoshou03", "real_name": "陈志伟", "email": "chenzhiwei@cnd.com", "phone": "13906003003", "department_id": 10, "is_superuser": False},
    {"username": "cangku01", "real_name": "吴志明", "email": "wuzhiming@cnd.com", "phone": "13906004001", "department_id": 9, "is_superuser": False},
    {"username": "cangku02", "real_name": "郑小芳", "email": "zhengxiaofang@cnd.com", "phone": "13906004002", "department_id": 9, "is_superuser": False},
    {"username": "caiwu01", "real_name": "黄晓燕", "email": "huangxiaoyan@cnd.com", "phone": "13906005001", "department_id": 7, "is_superuser": False},
    {"username": "caiwu02", "real_name": "刘建国", "email": "liujianguo@cnd.com", "phone": "13906005002", "department_id": 7, "is_superuser": False},
    {"username": "steel01", "real_name": "钢铁采购员A", "email": "steel01@cnd.com", "phone": "13906006001", "department_id": 3, "is_superuser": False},
    {"username": "steel02", "real_name": "钢铁销售员A", "email": "steel02@cnd.com", "phone": "13906006002", "department_id": 3, "is_superuser": False},
    {"username": "paper01", "real_name": "纸业采购员A", "email": "paper01@cnd.com", "phone": "13906007001", "department_id": 4, "is_superuser": False},
    {"username": "paper02", "real_name": "纸业销售员A", "email": "paper02@cnd.com", "phone": "13906007002", "department_id": 4, "is_superuser": False},
]

SUPPLIERS = [
    {"name": "宝山钢铁股份有限公司", "code": "SUP001", "type": "manufacturer", "contact_person": "王经理", "contact_phone": "021-26648000", "contact_email": "sales@baosteel.com", "address": "上海市宝山区富锦路885号", "tax_number": "913100001322030XX", "bank_name": "中国工商银行上海宝山支行", "bank_account": "1001XXXXXXXXXX0001", "credit_level": "A", "credit_limit": 50000000},
    {"name": "河钢集团有限公司", "code": "SUP002", "type": "manufacturer", "contact_person": "李经理", "contact_phone": "0311-66668888", "contact_email": "sales@hbis.com", "address": "河北省石家庄市体育南大街385号", "tax_number": "911300006746XXXXX", "bank_name": "中国银行石家庄分行", "bank_account": "1021XXXXXXXXXX0002", "credit_level": "A", "credit_limit": 30000000},
    {"name": "鞍钢集团有限公司", "code": "SUP003", "type": "manufacturer", "contact_person": "张经理", "contact_phone": "0412-6728888", "contact_email": "sales@ansteel.com", "address": "辽宁省鞍山市铁东区南胜利路46号", "tax_number": "912100001189XXXXX", "bank_name": "中国建设银行鞍山分行", "bank_account": "2100XXXXXXXXXX0003", "credit_level": "A", "credit_limit": 25000000},
    {"name": "首钢集团有限公司", "code": "SUP004", "type": "manufacturer", "contact_person": "赵经理", "contact_phone": "010-88298888", "contact_email": "sales@shougang.com", "address": "北京市石景山区石景山路68号", "tax_number": "911100001077XXXXX", "bank_name": "中国工商银行北京石景山支行", "bank_account": "0200XXXXXXXXXX0004", "credit_level": "A", "credit_limit": 20000000},
    {"name": "玖龙纸业(控股)有限公司", "code": "SUP005", "type": "manufacturer", "contact_person": "陈经理", "contact_phone": "0769-88778888", "contact_email": "sales@ndpaper.com", "address": "广东省东莞市麻涌镇新沙港工业区", "tax_number": "914419007350XXXXX", "bank_name": "中国农业银行东莞分行", "bank_account": "4428XXXXXXXXXX0005", "credit_level": "A", "credit_limit": 15000000},
    {"name": "山东晨鸣纸业集团股份有限公司", "code": "SUP006", "type": "manufacturer", "contact_person": "刘经理", "contact_phone": "0536-5228888", "contact_email": "sales@chenmingpaper.com", "address": "山东省寿光市圣城街道东环路01号", "tax_number": "913707001656XXXXX", "bank_name": "中国银行寿光支行", "bank_account": "2368XXXXXXXXXX0006", "credit_level": "A", "credit_limit": 12000000},
    {"name": "太阳纸业股份有限公司", "code": "SUP007", "type": "manufacturer", "contact_person": "孙经理", "contact_phone": "0537-3658888", "contact_email": "sales@sunpaper.com", "address": "山东省济宁市兖州区西关大街88号", "tax_number": "913708001671XXXXX", "bank_name": "中国建设银行兖州支行", "bank_account": "3700XXXXXXXXXX0007", "credit_level": "A", "credit_limit": 10000000},
    {"name": "华泰纸业股份有限公司", "code": "SUP008", "type": "manufacturer", "contact_person": "周经理", "contact_phone": "0546-6888888", "contact_email": "sales@huatai.com", "address": "山东省东营市广饶县大王镇", "tax_number": "913705001648XXXXX", "bank_name": "中国工商银行广饶支行", "bank_account": "1612XXXXXXXXXX0008", "credit_level": "B", "credit_limit": 8000000},
    {"name": "丰田汽车(中国)投资有限公司", "code": "SUP009", "type": "manufacturer", "contact_person": "田中经理", "contact_phone": "010-59568888", "contact_email": "sales@toyota.com.cn", "address": "北京市朝阳区光华路1号北京嘉里中心", "tax_number": "911100007178XXXXX", "bank_name": "中国银行北京分行", "bank_account": "3402XXXXXXXXXX0009", "credit_level": "A", "credit_limit": 80000000},
    {"name": "本田技研工业(中国)投资有限公司", "code": "SUP010", "type": "manufacturer", "contact_person": "山本经理", "contact_phone": "020-85558888", "contact_email": "sales@honda.com.cn", "address": "广州市天河区林和中路8号天誉大厦", "tax_number": "914401007221XXXXX", "bank_name": "中国工商银行广州分行", "bank_account": "3602XXXXXXXXXX0010", "credit_level": "A", "credit_limit": 60000000},
    {"name": "东风汽车集团有限公司", "code": "SUP011", "type": "manufacturer", "contact_person": "吴经理", "contact_phone": "027-84288888", "contact_email": "sales@dfmg.com.cn", "address": "湖北省武汉市武汉经济技术开发区东风大道特1号", "tax_number": "914200001776XXXXX", "bank_name": "中国建设银行武汉分行", "bank_account": "4200XXXXXXXXXX0011", "credit_level": "A", "credit_limit": 40000000},
    {"name": "中粮集团有限公司", "code": "SUP012", "type": "manufacturer", "contact_person": "郑经理", "contact_phone": "010-85008888", "contact_email": "sales@cofco.com", "address": "北京市朝阳区朝阳门南大街8号", "tax_number": "911100001011XXXXX", "bank_name": "中国农业银行北京朝阳支行", "bank_account": "1100XXXXXXXXXX0012", "credit_level": "A", "credit_limit": 50000000},
    {"name": "益海嘉里食品有限公司", "code": "SUP013", "type": "manufacturer", "contact_person": "黄经理", "contact_phone": "021-60128888", "contact_email": "sales@yihaikerry.com", "address": "上海市浦东新区银城中路168号", "tax_number": "913100006074XXXXX", "bank_name": "中国银行上海浦东分行", "bank_account": "4438XXXXXXXXXX0013", "credit_level": "A", "credit_limit": 30000000},
    {"name": "厦门国贸集团股份有限公司", "code": "SUP014", "type": "distributor", "contact_person": "林经理", "contact_phone": "0592-5888888", "contact_email": "trade@itg.com.cn", "address": "厦门市思明区湖滨南路388号国贸大厦", "tax_number": "913502001549XXXXX", "bank_name": "中国工商银行厦门分行", "bank_account": "4100XXXXXXXXXX0014", "credit_level": "A", "credit_limit": 25000000},
    {"name": "厦门象屿集团有限公司", "code": "SUP015", "type": "distributor", "contact_person": "陈经理", "contact_phone": "0592-5058888", "contact_email": "trade@xiangyu.cn", "address": "厦门市湖里区象屿路88号", "tax_number": "913502001550XXXXX", "bank_name": "中国建设银行厦门分行", "bank_account": "3510XXXXXXXXXX0015", "credit_level": "A", "credit_limit": 20000000},
]

CUSTOMERS = [
    {"name": "福建三钢(集团)有限责任公司", "code": "CUS001", "type": "vip", "contact_person": "王总", "contact_phone": "0598-8201888", "contact_email": "purchase@fjsansteel.com", "address": "福建省三明市梅列区工业中路", "tax_number": "913504001555XXXXX", "bank_name": "中国工商银行三明分行", "bank_account": "1404XXXXXXXXXX0001", "credit_limit": 20000000},
    {"name": "福建省汽车工业集团有限公司", "code": "CUS002", "type": "vip", "contact_person": "李总", "contact_phone": "0591-87808888", "contact_email": "purchase@fjmotor.com", "address": "福建省福州市仓山区城门镇樟岚村", "tax_number": "913501001581XXXXX", "bank_name": "中国银行福州分行", "bank_account": "4126XXXXXXXXXX0002", "credit_limit": 30000000},
    {"name": "金龙汽车集团股份有限公司", "code": "CUS003", "type": "vip", "contact_person": "张总", "contact_phone": "0592-2968888", "contact_email": "purchase@kinglong.com.cn", "address": "厦门市集美区金龙路9号", "tax_number": "913502001549XXXXX", "bank_name": "中国建设银行厦门分行", "bank_account": "3510XXXXXXXXXX0003", "credit_limit": 25000000},
    {"name": "福建联合石油化工有限公司", "code": "CUS004", "type": "vip", "contact_person": "赵总", "contact_phone": "0595-87688888", "contact_email": "purchase@frep.com.cn", "address": "福建省泉州市泉港区南埔镇", "tax_number": "913505001561XXXXX", "bank_name": "中国工商银行泉州分行", "bank_account": "1408XXXXXXXXXX0004", "credit_limit": 40000000},
    {"name": "紫金矿业集团股份有限公司", "code": "CUS005", "type": "vip", "contact_person": "陈总", "contact_phone": "0597-3568888", "contact_email": "purchase@zkj.com.cn", "address": "福建省龙岩市上杭县紫金大道1号", "tax_number": "913508001579XXXXX", "bank_name": "中国银行龙岩分行", "bank_account": "4136XXXXXXXXXX0005", "credit_limit": 50000000},
    {"name": "宁德时代新能源科技股份有限公司", "code": "CUS006", "type": "vip", "contact_person": "刘总", "contact_phone": "0593-8958888", "contact_email": "purchase@catl.com", "address": "福建省宁德市蕉城区漳湾镇新港路1号", "tax_number": "913509001585XXXXX", "bank_name": "中国建设银行宁德分行", "bank_account": "3500XXXXXXXXXX0006", "credit_limit": 80000000},
    {"name": "安踏体育用品集团有限公司", "code": "CUS007", "type": "wholesale", "contact_person": "孙总", "contact_phone": "0595-82688888", "contact_email": "purchase@anta.com", "address": "福建省晋江市池店镇东山工业区", "tax_number": "913505821563XXXXX", "bank_name": "中国工商银行晋江支行", "bank_account": "1408XXXXXXXXXX0007", "credit_limit": 15000000},
    {"name": "恒安国际集团有限公司", "code": "CUS008", "type": "wholesale", "contact_person": "周总", "contact_phone": "0595-85788888", "contact_email": "purchase@hengan.com", "address": "福建省晋江市安海镇恒安工业城", "tax_number": "913505821564XXXXX", "bank_name": "中国农业银行晋江支行", "bank_account": "1343XXXXXXXXXX0008", "credit_limit": 12000000},
    {"name": "达利食品集团有限公司", "code": "CUS009", "type": "wholesale", "contact_person": "吴总", "contact_phone": "0595-87388888", "contact_email": "purchase@dali-group.com", "address": "福建省泉州市惠安县紫山镇达利产业园", "tax_number": "913505211565XXXXX", "bank_name": "中国银行惠安支行", "bank_account": "4168XXXXXXXXXX0009", "credit_limit": 10000000},
    {"name": "福建永辉超市有限公司", "code": "CUS010", "type": "wholesale", "contact_person": "郑总", "contact_phone": "0591-88018888", "contact_email": "purchase@yonghui.com.cn", "address": "福建省福州市鼓楼区杨桥路永辉大厦", "tax_number": "913501001586XXXXX", "bank_name": "中国工商银行福州分行", "bank_account": "1400XXXXXXXXXX0010", "credit_limit": 8000000},
    {"name": "厦门钨业股份有限公司", "code": "CUS011", "type": "normal", "contact_person": "黄总", "contact_phone": "0592-2298888", "contact_email": "purchase@ctiam.com", "address": "厦门市海沧区柯井社", "tax_number": "913502001550XXXXX", "bank_name": "中国银行厦门分行", "bank_account": "4176XXXXXXXXXX0011", "credit_limit": 6000000},
    {"name": "福建龙净环保股份有限公司", "code": "CUS012", "type": "normal", "contact_person": "林总", "contact_phone": "0597-2298888", "contact_email": "purchase@longking.cn", "address": "福建省龙岩市新罗区工业西路68号", "tax_number": "913508001587XXXXX", "bank_name": "中国建设银行龙岩分行", "bank_account": "3500XXXXXXXXXX0012", "credit_limit": 5000000},
    {"name": "厦门宏发股份公司", "code": "CUS013", "type": "normal", "contact_person": "陈总", "contact_phone": "0592-6108888", "contact_email": "purchase@hongfa.com", "address": "厦门市集美区东林路566号", "tax_number": "913502001588XXXXX", "bank_name": "中国工商银行厦门分行", "bank_account": "4100XXXXXXXXXX0013", "credit_limit": 4000000},
    {"name": "福建南平太阳电缆股份有限公司", "code": "CUS014", "type": "normal", "contact_person": "王总", "contact_phone": "0599-8808888", "contact_email": "purchase@suncable.com", "address": "福建省南平市工业路102号", "tax_number": "913507001589XXXXX", "bank_name": "中国银行南平分行", "bank_account": "4186XXXXXXXXXX0014", "credit_limit": 3000000},
    {"name": "厦门松霖科技股份有限公司", "code": "CUS015", "type": "normal", "contact_person": "李总", "contact_phone": "0592-6368888", "contact_email": "purchase@solux.com", "address": "厦门市海沧区翁角路269号", "tax_number": "913502001590XXXXX", "bank_name": "中国建设银行厦门分行", "bank_account": "3510XXXXXXXXXX0015", "credit_limit": 2500000},
]

PRODUCT_CATEGORIES = [
    {"name": "钢铁产品", "code": "STEEL", "parent_id": None, "sort_order": 1},
    {"name": "板材", "code": "STEEL_PLATE", "parent_id": 1, "sort_order": 1},
    {"name": "型材", "code": "STEEL_SECTION", "parent_id": 1, "sort_order": 2},
    {"name": "管材", "code": "STEEL_PIPE", "parent_id": 1, "sort_order": 3},
    {"name": "线材", "code": "STEEL_WIRE", "parent_id": 1, "sort_order": 4},
    {"name": "纸业产品", "code": "PAPER", "parent_id": None, "sort_order": 2},
    {"name": "包装用纸", "code": "PAPER_PACK", "parent_id": 5, "sort_order": 1},
    {"name": "文化用纸", "code": "PAPER_CULTURE", "parent_id": 5, "sort_order": 2},
    {"name": "生活用纸", "code": "PAPER_TISSUE", "parent_id": 5, "sort_order": 3},
    {"name": "汽车产品", "code": "AUTO", "parent_id": None, "sort_order": 3},
    {"name": "整车", "code": "AUTO_VEHICLE", "parent_id": 9, "sort_order": 1},
    {"name": "零部件", "code": "AUTO_PARTS", "parent_id": 9, "sort_order": 2},
    {"name": "农产品", "code": "AGRI", "parent_id": None, "sort_order": 4},
    {"name": "粮油产品", "code": "AGRI_GRAIN", "parent_id": 12, "sort_order": 1},
    {"name": "饲料原料", "code": "AGRI_FEED", "parent_id": 12, "sort_order": 2},
]

PRODUCTS = [
    {"code": "SP001", "name": "热轧钢板Q235B", "category_id": 2, "specification": "10*2000*6000mm", "unit": "吨", "purchase_price": 4200.00, "sale_price": 4450.00, "min_stock": 500, "max_stock": 2000},
    {"code": "SP002", "name": "冷轧钢板DC01", "category_id": 2, "specification": "1.5*1250*2500mm", "unit": "吨", "purchase_price": 5200.00, "sale_price": 5500.00, "min_stock": 300, "max_stock": 1500},
    {"code": "SP003", "name": "镀锌钢板DX51D", "category_id": 2, "specification": "0.8*1250*C", "unit": "吨", "purchase_price": 5800.00, "sale_price": 6150.00, "min_stock": 200, "max_stock": 1000},
    {"code": "SP004", "name": "工字钢Q235", "category_id": 3, "specification": "25#", "unit": "吨", "purchase_price": 4150.00, "sale_price": 4400.00, "min_stock": 200, "max_stock": 800},
    {"code": "SP005", "name": "角钢Q235", "category_id": 3, "specification": "50*50*5mm", "unit": "吨", "purchase_price": 4050.00, "sale_price": 4300.00, "min_stock": 150, "max_stock": 600},
    {"code": "SP006", "name": "槽钢Q235", "category_id": 3, "specification": "20#", "unit": "吨", "purchase_price": 4100.00, "sale_price": 4350.00, "min_stock": 150, "max_stock": 600},
    {"code": "SP007", "name": "无缝钢管20#", "category_id": 4, "specification": "108*4.5mm", "unit": "吨", "purchase_price": 4800.00, "sale_price": 5100.00, "min_stock": 100, "max_stock": 500},
    {"code": "SP008", "name": "焊接钢管Q235", "category_id": 4, "specification": "219*6mm", "unit": "吨", "purchase_price": 4300.00, "sale_price": 4580.00, "min_stock": 100, "max_stock": 500},
    {"code": "SP009", "name": "螺纹钢HRB400", "category_id": 5, "specification": "Φ20mm", "unit": "吨", "purchase_price": 3950.00, "sale_price": 4200.00, "min_stock": 500, "max_stock": 2000},
    {"code": "SP010", "name": "线材Q235", "category_id": 5, "specification": "Φ6.5mm", "unit": "吨", "purchase_price": 3900.00, "sale_price": 4150.00, "min_stock": 300, "max_stock": 1200},
    {"code": "PP001", "name": "牛卡纸", "category_id": 6, "specification": "200g/m2*1600mm", "unit": "吨", "purchase_price": 4500.00, "sale_price": 4800.00, "min_stock": 200, "max_stock": 800},
    {"code": "PP002", "name": "瓦楞原纸", "category_id": 6, "specification": "120g/m2*1800mm", "unit": "吨", "purchase_price": 3200.00, "sale_price": 3450.00, "min_stock": 300, "max_stock": 1200},
    {"code": "PP003", "name": "箱板纸", "category_id": 6, "specification": "150g/m2*1700mm", "unit": "吨", "purchase_price": 3800.00, "sale_price": 4080.00, "min_stock": 250, "max_stock": 1000},
    {"code": "PP004", "name": "铜版纸", "category_id": 7, "specification": "128g/m2*889mm", "unit": "吨", "purchase_price": 5800.00, "sale_price": 6200.00, "min_stock": 100, "max_stock": 500},
    {"code": "PP005", "name": "双胶纸", "category_id": 7, "specification": "80g/m2*889mm", "unit": "吨", "purchase_price": 5200.00, "sale_price": 5550.00, "min_stock": 150, "max_stock": 600},
    {"code": "PP006", "name": "复印纸A4", "category_id": 7, "specification": "70g/包(500张)", "unit": "包", "purchase_price": 22.00, "sale_price": 28.00, "min_stock": 500, "max_stock": 2000},
    {"code": "PP007", "name": "卫生纸原纸", "category_id": 8, "specification": "17g/m2*2100mm", "unit": "吨", "purchase_price": 6500.00, "sale_price": 6950.00, "min_stock": 50, "max_stock": 200},
    {"code": "PP008", "name": "餐巾纸", "category_id": 8, "specification": "200抽/包", "unit": "包", "purchase_price": 3.50, "sale_price": 5.00, "min_stock": 1000, "max_stock": 5000},
    {"code": "AP001", "name": "丰田凯美瑞", "category_id": 10, "specification": "2.5S 锋尚版", "unit": "辆", "purchase_price": 195000.00, "sale_price": 215000.00, "min_stock": 5, "max_stock": 30},
    {"code": "AP002", "name": "丰田汉兰达", "category_id": 10, "specification": "2.0T 四驱精英版", "unit": "辆", "purchase_price": 248000.00, "sale_price": 275000.00, "min_stock": 3, "max_stock": 20},
    {"code": "AP003", "name": "本田雅阁", "category_id": 10, "specification": "260TURBO 精致版", "unit": "辆", "purchase_price": 175000.00, "sale_price": 195000.00, "min_stock": 5, "max_stock": 25},
    {"code": "AP004", "name": "本田CR-V", "category_id": 10, "specification": "240TURBO 两驱都市版", "unit": "辆", "purchase_price": 185000.00, "sale_price": 205000.00, "min_stock": 5, "max_stock": 25},
    {"code": "AP005", "name": "东风日产轩逸", "category_id": 10, "specification": "1.6L XL 豪华版", "unit": "辆", "purchase_price": 125000.00, "sale_price": 142000.00, "min_stock": 10, "max_stock": 50},
    {"code": "AP006", "name": "发动机总成", "category_id": 11, "specification": "丰田2.5L A25A-FKS", "unit": "台", "purchase_price": 35000.00, "sale_price": 42000.00, "min_stock": 2, "max_stock": 10},
    {"code": "AP007", "name": "变速箱总成", "category_id": 11, "specification": "丰田8AT", "unit": "台", "purchase_price": 28000.00, "sale_price": 35000.00, "min_stock": 2, "max_stock": 10},
    {"code": "AP008", "name": "轮胎", "category_id": 11, "specification": "米其林225/65R17", "unit": "条", "purchase_price": 850.00, "sale_price": 1100.00, "min_stock": 50, "max_stock": 200},
    {"code": "AG001", "name": "大豆", "category_id": 13, "specification": "转基因,蛋白≥38%", "unit": "吨", "purchase_price": 4800.00, "sale_price": 5100.00, "min_stock": 500, "max_stock": 3000},
    {"code": "AG002", "name": "玉米", "category_id": 13, "specification": "二等,水分≤14%", "unit": "吨", "purchase_price": 2800.00, "sale_price": 3000.00, "min_stock": 800, "max_stock": 5000},
    {"code": "AG003", "name": "小麦", "category_id": 13, "specification": "三等,容重≥750g/L", "unit": "吨", "purchase_price": 2900.00, "sale_price": 3150.00, "min_stock": 600, "max_stock": 4000},
    {"code": "AG004", "name": "豆粕", "category_id": 14, "specification": "蛋白≥43%", "unit": "吨", "purchase_price": 3500.00, "sale_price": 3750.00, "min_stock": 300, "max_stock": 2000},
    {"code": "AG005", "name": "菜籽粕", "category_id": 14, "specification": "蛋白≥35%", "unit": "吨", "purchase_price": 2800.00, "sale_price": 3000.00, "min_stock": 200, "max_stock": 1500},
    {"code": "AG006", "name": "棕榈油", "category_id": 13, "specification": "24度精炼", "unit": "吨", "purchase_price": 8500.00, "sale_price": 9200.00, "min_stock": 100, "max_stock": 800},
]

WAREHOUSES = [
    {"code": "WH001", "name": "厦门海沧钢材仓库", "type": "raw", "address": "厦门市海沧区建发物流园A区", "manager": "吴志明", "phone": "0592-6888001", "capacity": 50000},
    {"code": "WH002", "name": "厦门同安纸业仓库", "type": "normal", "address": "厦门市同安区工业集中区", "manager": "郑小芳", "phone": "0592-7108002", "capacity": 30000},
    {"code": "WH003", "name": "厦门翔安汽车仓库", "type": "finished", "address": "厦门市翔安区巷北工业区", "manager": "张志强", "phone": "0592-7888003", "capacity": 20000},
    {"code": "WH004", "name": "厦门集美农产品仓库", "type": "normal", "address": "厦门市集美区灌口镇", "manager": "李明华", "phone": "0592-6268004", "capacity": 40000},
    {"code": "WH005", "name": "泉州晋江钢材仓库", "type": "raw", "address": "泉州市晋江市安海镇工业区", "manager": "王建国", "phone": "0595-8578005", "capacity": 35000},
    {"code": "WH006", "name": "福州马尾综合仓库", "type": "normal", "address": "福州市马尾区青洲路", "manager": "陈志远", "phone": "0591-8368006", "capacity": 45000},
    {"code": "WH007", "name": "厦门湖里退货仓库", "type": "return", "address": "厦门市湖里区高崎北二路", "manager": "林晓燕", "phone": "0592-5788007", "capacity": 10000},
]

ACCOUNTS = [
    {"name": "中国工商银行厦门分行基本户", "code": "ACC001", "type": "bank", "bank_name": "中国工商银行厦门分行", "account_number": "410002920920XXXXXXX", "balance": 50000000.00},
    {"name": "中国建设银行厦门分行一般户", "code": "ACC002", "type": "bank", "bank_name": "中国建设银行厦门分行", "account_number": "351015580010XXXXXXX", "balance": 30000000.00},
    {"name": "中国银行厦门分行外汇户", "code": "ACC003", "type": "bank", "bank_name": "中国银行厦门分行", "account_number": "417662360010XXXXXXX", "balance": 20000000.00},
    {"name": "现金账户", "code": "ACC004", "type": "cash", "bank_name": None, "account_number": None, "balance": 500000.00},
    {"name": "支付宝账户", "code": "ACC005", "type": "online", "bank_name": "支付宝", "account_number": "cnd@alipay.com", "balance": 1000000.00},
    {"name": "微信支付账户", "code": "ACC006", "type": "online", "bank_name": "微信支付", "account_number": "cnd@wechat.com", "balance": 800000.00},
]

COST_CENTERS = [
    {"name": "钢铁供应链成本中心", "code": "CC001", "parent_id": None},
    {"name": "纸业供应链成本中心", "code": "CC002", "parent_id": None},
    {"name": "汽车供应链成本中心", "code": "CC003", "parent_id": None},
    {"name": "农产品供应链成本中心", "code": "CC004", "parent_id": None},
    {"name": "仓储物流成本中心", "code": "CC005", "parent_id": None},
    {"name": "管理费用成本中心", "code": "CC006", "parent_id": None},
]

WORKFLOW_DEFINITIONS = [
    {"name": "采购订单审批流程", "code": "WF_PURCHASE", "type": "purchase", "description": "采购订单标准审批流程", "config": {"steps": [{"name": "部门经理审批", "approver_role": "dept_manager"}, {"name": "财务审核", "approver_role": "finance"}, {"name": "总经理审批", "approver_role": "super_admin"}]}},
    {"name": "销售订单审批流程", "code": "WF_SALES", "type": "sale", "description": "销售订单标准审批流程", "config": {"steps": [{"name": "部门经理审批", "approver_role": "dept_manager"}, {"name": "财务审核", "approver_role": "finance"}]}},
    {"name": "付款审批流程", "code": "WF_PAYMENT", "type": "payment", "description": "付款申请标准审批流程", "config": {"steps": [{"name": "部门经理审批", "approver_role": "dept_manager"}, {"name": "财务审核", "approver_role": "finance"}, {"name": "财务总监审批", "approver_role": "finance"}, {"name": "总经理审批", "approver_role": "super_admin"}]}},
]

def generate_code(prefix: str, seq: int) -> str:
    return f"{prefix}{datetime.now().strftime('%Y%m%d')}{seq:04d}"

def random_date(start_days_ago: int = 365, end_days_ago: int = 0) -> datetime:
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def create_departments(db: Session):
    print("创建部门数据...")
    dept_map = {}
    created_count = 0
    for dept_data in DEPARTMENTS:
        existing = db.query(Department).filter(Department.code == dept_data["code"]).first()
        if existing:
            dept_map[dept_data["code"]] = existing.id
            continue
        dept = Department(**dept_data, status=1, description=f"{dept_data['name']}负责公司相关业务")
        db.add(dept)
        db.flush()
        dept_map[dept.code] = dept.id
        created_count += 1
    for i, dept_data in enumerate(DEPARTMENTS):
        if dept_data["parent_id"] is not None and isinstance(dept_data["parent_id"], int):
            dept = db.query(Department).filter(Department.code == dept_data["code"]).first()
            parent_code = DEPARTMENTS[dept_data["parent_id"] - 1]["code"]
            dept.parent_id = dept_map.get(parent_code)
    db.commit()
    print(f"成功创建 {created_count} 个部门（已存在 {len(DEPARTMENTS) - created_count} 个）")
    return dept_map

def create_roles(db: Session):
    print("创建角色数据...")
    role_map = {}
    created_count = 0
    for role_data in ROLES:
        existing = db.query(Role).filter(Role.code == role_data["code"]).first()
        if existing:
            role_map[role_data["code"]] = existing.id
            continue
        role = Role(**role_data, status=True)
        db.add(role)
        db.flush()
        role_map[role.code] = role.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个角色（已存在 {len(ROLES) - created_count} 个）")
    return role_map

def create_permissions(db: Session):
    print("创建权限数据...")
    permissions = [
        {"name": "菜单-首页", "code": "menu:dashboard", "type": "menu", "description": "首页菜单访问权限"},
        {"name": "菜单-采购管理", "code": "menu:purchase", "type": "menu", "description": "采购管理菜单访问权限"},
        {"name": "菜单-销售管理", "code": "menu:sales", "type": "menu", "description": "销售管理菜单访问权限"},
        {"name": "菜单-库存管理", "code": "menu:inventory", "type": "menu", "description": "库存管理菜单访问权限"},
        {"name": "菜单-财务管理", "code": "menu:finance", "type": "menu", "description": "财务管理菜单访问权限"},
        {"name": "菜单-供应商管理", "code": "menu:supplier", "type": "menu", "description": "供应商管理菜单访问权限"},
        {"name": "菜单-客户管理", "code": "menu:customer", "type": "menu", "description": "客户管理菜单访问权限"},
        {"name": "菜单-系统管理", "code": "menu:system", "type": "menu", "description": "系统管理菜单访问权限"},
        {"name": "菜单-数据分析", "code": "menu:analysis", "type": "menu", "description": "数据分析菜单访问权限"},
        {"name": "菜单-供应商分析", "code": "menu:analysis:supplier", "type": "menu", "description": "供应商分析菜单访问权限"},
        {"name": "菜单-采购分析", "code": "menu:analysis:purchase", "type": "menu", "description": "采购分析菜单访问权限"},
        {"name": "菜单-库存分析", "code": "menu:analysis:inventory", "type": "menu", "description": "库存分析菜单访问权限"},
        {"name": "菜单-销售分析", "code": "menu:analysis:sales", "type": "menu", "description": "销售分析菜单访问权限"},
        {"name": "菜单-付款分析", "code": "menu:analysis:payment", "type": "menu", "description": "付款分析菜单访问权限"},
        {"name": "菜单-账单分析", "code": "menu:analysis:bill", "type": "menu", "description": "账单分析菜单访问权限"},
        {"name": "菜单-账户分析", "code": "menu:analysis:account", "type": "menu", "description": "账户分析菜单访问权限"},
        {"name": "按钮-新增采购订单", "code": "btn:purchase:create", "type": "button", "description": "创建采购订单权限"},
        {"name": "按钮-审批采购订单", "code": "btn:purchase:approve", "type": "button", "description": "审批采购订单权限"},
        {"name": "按钮-新增销售订单", "code": "btn:sales:create", "type": "button", "description": "创建销售订单权限"},
        {"name": "按钮-审批销售订单", "code": "btn:sales:approve", "type": "button", "description": "审批销售订单权限"},
        {"name": "按钮-付款操作", "code": "btn:finance:payment", "type": "button", "description": "付款操作权限"},
        {"name": "按钮-库存操作", "code": "btn:inventory:operate", "type": "button", "description": "库存出入库操作权限"},
    ]
    perm_map = {}
    created_count = 0
    for perm_data in permissions:
        existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
        if existing:
            perm_map[perm_data["code"]] = existing.id
            continue
        perm = Permission(**perm_data)
        db.add(perm)
        db.flush()
        perm_map[perm.code] = perm.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个权限（已存在 {len(permissions) - created_count} 个）")
    return perm_map

def create_users(db: Session, dept_map: dict, role_map: dict):
    print("创建用户数据...")
    user_map = {}
    default_password = get_password_hash("123456")
    created_count = 0
    for user_data in USERS:
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            user_map[user_data["username"]] = existing_user.id
            continue
        user = User(
            username=user_data["username"],
            password=default_password,
            real_name=user_data["real_name"],
            email=user_data["email"],
            phone=user_data["phone"],
            department_id=user_data["department_id"],
            is_superuser=user_data["is_superuser"],
            status=True
        )
        db.add(user)
        db.flush()
        user_map[user.username] = user.id
        created_count += 1
        if user_data["is_superuser"]:
            user_role = UserRole(user_id=user.id, role_id=role_map["super_admin"])
        elif "caigou" in user_data["username"]:
            user_role = UserRole(user_id=user.id, role_id=role_map["purchaser"])
        elif "xiaoshou" in user_data["username"]:
            user_role = UserRole(user_id=user.id, role_id=role_map["sales"])
        elif "cangku" in user_data["username"]:
            user_role = UserRole(user_id=user.id, role_id=role_map["warehouse_keeper"])
        elif "caiwu" in user_data["username"]:
            user_role = UserRole(user_id=user.id, role_id=role_map["finance"])
        elif user_data["department_id"] and user_data["department_id"] <= 13:
            user_role = UserRole(user_id=user.id, role_id=role_map["dept_manager"])
        else:
            user_role = UserRole(user_id=user.id, role_id=role_map["employee"])
        db.add(user_role)
    db.commit()
    print(f"成功创建 {created_count} 个用户（已存在 {len(USERS) - created_count} 个）")
    return user_map

def create_suppliers(db: Session):
    print("创建供应商数据...")
    supplier_map = {}
    created_count = 0
    for sup_data in SUPPLIERS:
        existing = db.query(Supplier).filter(Supplier.code == sup_data["code"]).first()
        if existing:
            supplier_map[sup_data["code"]] = existing.id
            continue
        supplier = Supplier(**sup_data, status=True, balance=0.0)
        db.add(supplier)
        db.flush()
        supplier_map[sup_data["code"]] = supplier.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个供应商（已存在 {len(SUPPLIERS) - created_count} 个）")
    return supplier_map

def create_customers(db: Session):
    print("创建客户数据...")
    customer_map = {}
    created_count = 0
    for cust_data in CUSTOMERS:
        existing = db.query(Customer).filter(Customer.code == cust_data["code"]).first()
        if existing:
            customer_map[cust_data["code"]] = existing.id
            continue
        customer = Customer(**cust_data, status=True, balance=0.0)
        db.add(customer)
        db.flush()
        customer_map[cust_data["code"]] = customer.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个客户（已存在 {len(CUSTOMERS) - created_count} 个）")
    return customer_map

def create_product_categories(db: Session):
    print("创建产品分类数据...")
    cat_map = {}
    created_count = 0
    for cat_data in PRODUCT_CATEGORIES:
        existing = db.query(ProductCategory).filter(ProductCategory.code == cat_data["code"]).first()
        if existing:
            cat_map[cat_data["code"]] = existing.id
            continue
        cat = ProductCategory(**cat_data, status=1, description=f"{cat_data['name']}分类")
        db.add(cat)
        db.flush()
        cat_map[cat_data["code"]] = cat.id
        created_count += 1
    for i, cat_data in enumerate(PRODUCT_CATEGORIES):
        if cat_data["parent_id"] is not None:
            cat = db.query(ProductCategory).filter(ProductCategory.code == cat_data["code"]).first()
            parent_code = PRODUCT_CATEGORIES[cat_data["parent_id"] - 1]["code"]
            cat.parent_id = cat_map.get(parent_code)
    db.commit()
    print(f"成功创建 {created_count} 个产品分类（已存在 {len(PRODUCT_CATEGORIES) - created_count} 个）")
    return cat_map

def create_products(db: Session, cat_map: dict):
    print("创建产品数据...")
    product_map = {}
    created_count = 0
    for prod_data in PRODUCTS:
        existing = db.query(Product).filter(Product.code == prod_data["code"]).first()
        if existing:
            product_map[prod_data["code"]] = existing.id
            continue
        product = Product(
            code=prod_data["code"],
            name=prod_data["name"],
            category_id=prod_data["category_id"],
            specification=prod_data["specification"],
            unit=prod_data["unit"],
            purchase_price=prod_data["purchase_price"],
            sale_price=prod_data["sale_price"],
            min_stock=prod_data["min_stock"],
            max_stock=prod_data["max_stock"],
            current_stock=random.uniform(prod_data["min_stock"], prod_data["max_stock"]),
            status="active"
        )
        db.add(product)
        db.flush()
        product_map[prod_data["code"]] = product.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个产品（已存在 {len(PRODUCTS) - created_count} 个）")
    return product_map

def create_warehouses(db: Session):
    print("创建仓库数据...")
    warehouse_map = {}
    created_count = 0
    for wh_data in WAREHOUSES:
        existing = db.query(Warehouse).filter(Warehouse.code == wh_data["code"]).first()
        if existing:
            warehouse_map[wh_data["code"]] = existing.id
            continue
        warehouse = Warehouse(**wh_data, status=1, remark=f"{wh_data['name']}，主要存储相关产品")
        db.add(warehouse)
        db.flush()
        warehouse_map[wh_data["code"]] = warehouse.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个仓库（已存在 {len(WAREHOUSES) - created_count} 个）")
    return warehouse_map

def create_accounts(db: Session):
    print("创建账户数据...")
    account_map = {}
    created_count = 0
    for acc_data in ACCOUNTS:
        existing = db.query(Account).filter(Account.code == acc_data["code"]).first()
        if existing:
            account_map[acc_data["code"]] = existing.id
            continue
        account = Account(**acc_data, status=1, remark=f"{acc_data['name']}")
        db.add(account)
        db.flush()
        account_map[acc_data["code"]] = account.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个账户（已存在 {len(ACCOUNTS) - created_count} 个）")
    return account_map

def create_cost_centers(db: Session):
    print("创建成本中心数据...")
    cc_map = {}
    created_count = 0
    for cc_data in COST_CENTERS:
        existing = db.query(CostCenter).filter(CostCenter.code == cc_data["code"]).first()
        if existing:
            cc_map[cc_data["code"]] = existing.id
            continue
        cc = CostCenter(**cc_data, status=1, description=f"{cc_data['name']}")
        db.add(cc)
        db.flush()
        cc_map[cc_data["code"]] = cc.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个成本中心（已存在 {len(COST_CENTERS) - created_count} 个）")
    return cc_map

def create_workflow_definitions(db: Session):
    print("创建工作流定义数据...")
    wf_map = {}
    created_count = 0
    for wf_data in WORKFLOW_DEFINITIONS:
        existing = db.query(WorkflowDefinition).filter(WorkflowDefinition.code == wf_data["code"]).first()
        if existing:
            wf_map[wf_data["code"]] = existing.id
            continue
        wf = WorkflowDefinition(**wf_data, status=1)
        db.add(wf)
        db.flush()
        wf_map[wf_data["code"]] = wf.id
        created_count += 1
    db.commit()
    print(f"成功创建 {created_count} 个工作流定义（已存在 {len(WORKFLOW_DEFINITIONS) - created_count} 个）")
    return wf_map

def create_purchase_orders(db: Session, supplier_map: dict, product_map: dict, user_map: dict, warehouse_map: dict):
    print("创建采购订单数据...")
    po_count = 0
    po_item_count = 0
    stock_record_count = 0
    purchasers = [u for u in USERS if "caigou" in u["username"] or u["username"] in ["zhangminghui", "lijianguo", "steel01", "paper01"]]
    for i in range(50):
        supplier_code = random.choice(list(supplier_map.keys()))
        purchaser = random.choice(purchasers)
        purchase_date = random_date(180, 10)
        expected_date = purchase_date + timedelta(days=random.randint(7, 30))
        status = random.choice(["pending", "approved", "shipped", "completed", "completed", "completed"])
        approval_status = "approved" if status in ["approved", "shipped", "completed"] else "pending"
        po = PurchaseOrder(
            code=generate_code("PO", i + 1),
            supplier_id=supplier_map[supplier_code],
            purchase_date=purchase_date,
            expected_date=expected_date,
            total_amount=0,
            paid_amount=0,
            status=status,
            approval_status=approval_status,
            approved_by=user_map.get("zhengguohua") if approval_status == "approved" else None,
            approved_at=purchase_date + timedelta(hours=random.randint(1, 24)) if approval_status == "approved" else None,
            remark=f"采购订单，供应商：{supplier_code}"
        )
        db.add(po)
        db.flush()
        po_count += 1
        total_amount = 0
        items_count = random.randint(2, 5)
        selected_products = random.sample(list(product_map.keys()), items_count)
        for prod_code in selected_products:
            prod = db.query(Product).filter(Product.code == prod_code).first()
            quantity = random.uniform(10, 100)
            unit_price = prod.purchase_price * random.uniform(0.98, 1.02)
            amount = round(quantity * unit_price, 2)
            total_amount += amount
            received_qty = quantity if status == "completed" else (quantity * random.uniform(0.5, 1.0) if status == "shipped" else 0)
            item = PurchaseOrderItem(
                purchase_order_id=po.id,
                product_code=prod_code,
                product_name=prod.name,
                specification=prod.specification,
                unit=prod.unit,
                quantity=round(quantity, 2),
                unit_price=round(unit_price, 2),
                amount=amount,
                received_quantity=round(received_qty, 2)
            )
            db.add(item)
            po_item_count += 1
            if status in ["shipped", "completed"] and received_qty > 0:
                wh_code = random.choice(list(warehouse_map.keys()))
                stock_record = StockRecord(
                    code=generate_code("SR", stock_record_count + 1),
                    type="in",
                    warehouse_id=warehouse_map[wh_code],
                    product_id=product_map[prod_code],
                    quantity=round(received_qty, 2),
                    unit_price=round(unit_price, 2),
                    amount=round(received_qty * unit_price, 2),
                    reference_code=po.code,
                    reference_type="purchase",
                    operator_id=user_map.get(purchaser["username"]),
                    remark=f"采购入库，采购单号：{po.code}"
                )
                db.add(stock_record)
                stock_record_count += 1
        po.total_amount = round(total_amount, 2)
        if status == "completed":
            po.paid_amount = round(total_amount * random.uniform(0.3, 1.0), 2)
    db.commit()
    print(f"成功创建 {po_count} 个采购订单，{po_item_count} 个采购订单明细，{stock_record_count} 条库存记录")

def create_sales_orders(db: Session, customer_map: dict, product_map: dict, user_map: dict, warehouse_map: dict):
    print("创建销售订单数据...")
    so_count = 0
    so_item_count = 0
    stock_record_count = 0
    salespersons = [u for u in USERS if "xiaoshou" in u["username"] or u["username"] in ["zhouxiaoyan", "steel02", "paper02"]]
    for i in range(60):
        customer_code = random.choice(list(customer_map.keys()))
        salesperson = random.choice(salespersons)
        sale_date = random_date(150, 5)
        delivery_date = sale_date + timedelta(days=random.randint(3, 15))
        status = random.choice(["pending", "shipped", "delivered", "completed", "completed", "completed"])
        approval_status = "approved" if status in ["shipped", "delivered", "completed"] else "pending"
        so = SalesOrder(
            code=generate_code("SO", i + 1),
            customer_id=customer_map[customer_code],
            sale_date=sale_date,
            delivery_date=delivery_date,
            total_amount=0,
            paid_amount=0,
            status=status,
            approval_status=approval_status,
            approved_by=user_map.get("zhouxiaoyan") if approval_status == "approved" else None,
            approved_at=sale_date + timedelta(hours=random.randint(1, 24)) if approval_status == "approved" else None,
            remark=f"销售订单，客户：{customer_code}"
        )
        db.add(so)
        db.flush()
        so_count += 1
        total_amount = 0
        items_count = random.randint(1, 4)
        selected_products = random.sample(list(product_map.keys()), items_count)
        for prod_code in selected_products:
            prod = db.query(Product).filter(Product.code == prod_code).first()
            quantity = random.uniform(5, 50)
            unit_price = prod.sale_price * random.uniform(0.95, 1.05)
            amount = round(quantity * unit_price, 2)
            total_amount += amount
            shipped_qty = quantity if status in ["delivered", "completed"] else (quantity * random.uniform(0.3, 0.8) if status == "shipped" else 0)
            item = SalesOrderItem(
                sales_order_id=so.id,
                product_code=prod_code,
                product_name=prod.name,
                specification=prod.specification,
                unit=prod.unit,
                quantity=round(quantity, 2),
                unit_price=round(unit_price, 2),
                amount=amount,
                shipped_quantity=round(shipped_qty, 2)
            )
            db.add(item)
            so_item_count += 1
            if status in ["shipped", "delivered", "completed"] and shipped_qty > 0:
                wh_code = random.choice(list(warehouse_map.keys()))
                stock_record = StockRecord(
                    code=generate_code("SR", 1000 + stock_record_count + 1),
                    type="out",
                    warehouse_id=warehouse_map[wh_code],
                    product_id=product_map[prod_code],
                    quantity=round(shipped_qty, 2),
                    unit_price=round(unit_price, 2),
                    amount=round(shipped_qty * unit_price, 2),
                    reference_code=so.code,
                    reference_type="sale",
                    operator_id=user_map.get(salesperson["username"]),
                    remark=f"销售出库，销售单号：{so.code}"
                )
                db.add(stock_record)
                stock_record_count += 1
        so.total_amount = round(total_amount, 2)
        if status == "completed":
            so.paid_amount = round(total_amount * random.uniform(0.5, 1.0), 2)
    db.commit()
    print(f"成功创建 {so_count} 个销售订单，{so_item_count} 个销售订单明细，{stock_record_count} 条库存记录")

def create_payments_and_bills(db: Session, supplier_map: dict, customer_map: dict, user_map: dict, account_map: dict):
    print("创建付款和账单数据...")
    payment_count = 0
    bill_count = 0
    finance_users = [u for u in USERS if "caiwu" in u["username"] or u["username"] == "wuyafang"]
    for i in range(30):
        supplier_code = random.choice(list(supplier_map.keys()))
        amount = random.uniform(50000, 2000000)
        payment_date = random_date(120, 5)
        status = random.choice(["pending", "completed", "completed", "completed"])
        approval_status = "approved" if status == "completed" else "pending"
        finance_user = random.choice(finance_users)
        payment = Payment(
            code=generate_code("PAY", i + 1),
            type="pay",
            amount=round(amount, 2),
            payment_method=random.choice(["transfer", "transfer", "check"]),
            payment_date=payment_date if status == "completed" else None,
            reference_type="purchase",
            supplier_id=supplier_map[supplier_code],
            bank_account=account_map["ACC001"],
            status=status,
            approval_status=approval_status,
            approved_by=user_map.get("wuyafang") if approval_status == "approved" else None,
            approved_at=payment_date - timedelta(hours=random.randint(1, 48)) if approval_status == "approved" else None,
            operator_id=user_map.get(finance_user["username"]),
            remark=f"采购付款，供应商：{supplier_code}"
        )
        db.add(payment)
        payment_count += 1
    for i in range(25):
        customer_code = random.choice(list(customer_map.keys()))
        amount = random.uniform(30000, 1500000)
        payment_date = random_date(120, 5)
        status = random.choice(["pending", "completed", "completed", "completed"])
        approval_status = "approved" if status == "completed" else "pending"
        finance_user = random.choice(finance_users)
        payment = Payment(
            code=generate_code("REC", i + 1),
            type="receive",
            amount=round(amount, 2),
            payment_method=random.choice(["transfer", "transfer", "online"]),
            payment_date=payment_date if status == "completed" else None,
            reference_type="sale",
            customer_id=customer_map[customer_code],
            bank_account=account_map["ACC001"],
            status=status,
            approval_status=approval_status,
            approved_by=user_map.get("wuyafang") if approval_status == "approved" else None,
            approved_at=payment_date - timedelta(hours=random.randint(1, 48)) if approval_status == "approved" else None,
            operator_id=user_map.get(finance_user["username"]),
            remark=f"销售收款，客户：{customer_code}"
        )
        db.add(payment)
        payment_count += 1
    for i in range(40):
        supplier_code = random.choice(list(supplier_map.keys()))
        amount = random.uniform(100000, 3000000)
        bill_date = random_date(90, 10)
        due_date = bill_date + timedelta(days=random.randint(30, 90))
        paid_amount = amount * random.uniform(0, 1.0)
        remaining_amount = amount - paid_amount
        status = "paid" if remaining_amount < 100 else ("partial" if paid_amount > 0 else "unpaid")
        if status == "unpaid" and datetime.now() > due_date:
            status = "overdue"
        bill = Bill(
            code=generate_code("AP", i + 1),
            type="payable",
            amount=round(amount, 2),
            bill_date=bill_date,
            due_date=due_date,
            reference_type="purchase",
            supplier_id=supplier_map[supplier_code],
            paid_amount=round(paid_amount, 2),
            remaining_amount=round(remaining_amount, 2),
            status=status,
            remark=f"应付账款，供应商：{supplier_code}"
        )
        db.add(bill)
        bill_count += 1
    for i in range(35):
        customer_code = random.choice(list(customer_map.keys()))
        amount = random.uniform(80000, 2500000)
        bill_date = random_date(90, 10)
        due_date = bill_date + timedelta(days=random.randint(15, 60))
        paid_amount = amount * random.uniform(0, 1.0)
        remaining_amount = amount - paid_amount
        status = "paid" if remaining_amount < 100 else ("partial" if paid_amount > 0 else "unpaid")
        if status == "unpaid" and datetime.now() > due_date:
            status = "overdue"
        bill = Bill(
            code=generate_code("AR", i + 1),
            type="receivable",
            amount=round(amount, 2),
            bill_date=bill_date,
            due_date=due_date,
            reference_type="sale",
            customer_id=customer_map[customer_code],
            paid_amount=round(paid_amount, 2),
            remaining_amount=round(remaining_amount, 2),
            status=status,
            remark=f"应收账款，客户：{customer_code}"
        )
        db.add(bill)
        bill_count += 1
    db.commit()
    print(f"成功创建 {payment_count} 条付款记录，{bill_count} 条账单记录")

def create_workflow_instances(db: Session, wf_map: dict, user_map: dict):
    print("创建工作流实例数据...")
    instance_count = 0
    log_count = 0
    for i in range(20):
        wf_code = random.choice(list(wf_map.keys()))
        initiator = random.choice(list(user_map.keys()))
        status = random.choice(["pending", "approved", "approved", "approved", "rejected"])
        instance = WorkflowInstance(
            code=generate_code("WF", i + 1),
            definition_id=wf_map[wf_code],
            business_type="purchase" if wf_code == "WF_PURCHASE" else ("sale" if wf_code == "WF_SALES" else "payment"),
            business_id=random.randint(1, 50),
            current_step="已完成" if status == "approved" else ("已拒绝" if status == "rejected" else "待审批"),
            status=status,
            initiator_id=user_map[initiator],
            remark=f"工作流实例，流程：{wf_code}"
        )
        db.add(instance)
        db.flush()
        instance_count += 1
        log = WorkflowLog(
            instance_id=instance.id,
            step_name="提交申请",
            action="submit",
            handler_id=user_map[initiator],
            comment="提交审批申请"
        )
        db.add(log)
        log_count += 1
        if status in ["approved", "rejected"]:
            approver = random.choice(["zhengguohua", "wuyafang", "huangwenzhou"])
            log = WorkflowLog(
                instance_id=instance.id,
                step_name="审批",
                action=status,
                handler_id=user_map.get(approver),
                comment="同意" if status == "approved" else "拒绝"
            )
            db.add(log)
            log_count += 1
    db.commit()
    print(f"成功创建 {instance_count} 个工作流实例，{log_count} 条工作流日志")

def create_menus(db: Session):
    print("创建菜单数据...")
    menus = [
        {"name": "仪表盘", "code": "DASHBOARD", "path": "/dashboard", "component": None, "icon": "DataAnalysis", "parent_id": None, "sort_order": 1, "status": True},
        {"name": "系统管理", "code": "SYSTEM", "path": "/system", "component": None, "icon": "Setting", "parent_id": None, "sort_order": 2, "status": True},
        {"name": "用户管理", "code": "SYSTEM_USERS", "path": "users", "component": "Users", "icon": "User", "parent_id": None, "sort_order": 1, "status": True},
        {"name": "角色管理", "code": "SYSTEM_ROLES", "path": "roles", "component": "Roles", "icon": "UserFilled", "parent_id": None, "sort_order": 2, "status": True},
        {"name": "部门管理", "code": "SYSTEM_DEPTS", "path": "departments", "component": "Departments", "icon": "OfficeBuilding", "parent_id": None, "sort_order": 3, "status": True},
        {"name": "菜单管理", "code": "SYSTEM_MENUS", "path": "menus", "component": "Menus", "icon": "Menu", "parent_id": None, "sort_order": 4, "status": True},
        {"name": "供应链管理", "code": "SUPPLY", "path": "/supply", "component": None, "icon": "Goods", "parent_id": None, "sort_order": 3, "status": True},
        {"name": "供应商管理", "code": "SUPPLY_SUPPLIERS", "path": "suppliers", "component": "Suppliers", "icon": "Shop", "parent_id": None, "sort_order": 1, "status": True},
        {"name": "采购管理", "code": "SUPPLY_PURCHASE", "path": "purchase", "component": "Purchase", "icon": "ShoppingCart", "parent_id": None, "sort_order": 2, "status": True},
        {"name": "库存管理", "code": "SUPPLY_INVENTORY", "path": "inventory", "component": "Inventory", "icon": "Box", "parent_id": None, "sort_order": 3, "status": True},
        {"name": "销售管理", "code": "SUPPLY_SALES", "path": "sales", "component": "Sales", "icon": "Sell", "parent_id": None, "sort_order": 4, "status": True},
        {"name": "财务管理", "code": "FINANCE", "path": "/finance", "component": None, "icon": "Money", "parent_id": None, "sort_order": 4, "status": True},
        {"name": "付款管理", "code": "FINANCE_PAYMENTS", "path": "payments", "component": "Payments", "icon": "Wallet", "parent_id": None, "sort_order": 1, "status": True},
        {"name": "账单管理", "code": "FINANCE_BILLS", "path": "bills", "component": "Bills", "icon": "Document", "parent_id": None, "sort_order": 2, "status": True},
        {"name": "账户管理", "code": "FINANCE_ACCOUNTS", "path": "accounts", "component": "Accounts", "icon": "CreditCard", "parent_id": None, "sort_order": 3, "status": True},
        {"name": "报表分析", "code": "FINANCE_REPORTS", "path": "reports", "component": "Reports", "icon": "DataLine", "parent_id": None, "sort_order": 4, "status": True},
        {"name": "数据分析", "code": "ANALYSIS", "path": "/analysis", "component": None, "icon": "TrendCharts", "parent_id": None, "sort_order": 5, "status": True},
        {"name": "供应商分析", "code": "ANALYSIS_SUPPLIER", "path": "supplier", "component": "SupplierAnalysis", "icon": "Shop", "parent_id": None, "sort_order": 1, "status": True},
        {"name": "采购分析", "code": "ANALYSIS_PURCHASE", "path": "purchase", "component": "PurchaseAnalysis", "icon": "ShoppingCart", "parent_id": None, "sort_order": 2, "status": True},
        {"name": "库存分析", "code": "ANALYSIS_INVENTORY", "path": "inventory", "component": "InventoryAnalysis", "icon": "Box", "parent_id": None, "sort_order": 3, "status": True},
        {"name": "销售分析", "code": "ANALYSIS_SALES", "path": "sales", "component": "SalesAnalysis", "icon": "Sell", "parent_id": None, "sort_order": 4, "status": True},
        {"name": "付款分析", "code": "ANALYSIS_PAYMENT", "path": "payment", "component": "PaymentAnalysis", "icon": "Wallet", "parent_id": None, "sort_order": 5, "status": True},
        {"name": "账单分析", "code": "ANALYSIS_BILL", "path": "bill", "component": "BillAnalysis", "icon": "Document", "parent_id": None, "sort_order": 6, "status": True},
        {"name": "账户分析", "code": "ANALYSIS_ACCOUNT", "path": "account", "component": "AccountAnalysis", "icon": "CreditCard", "parent_id": None, "sort_order": 7, "status": True},
    ]
    
    menu_map = {}
    created_count = 0
    
    for menu_data in menus:
        existing = db.query(Menu).filter(Menu.code == menu_data["code"]).first()
        if existing:
            menu_map[menu_data["code"]] = existing.id
            continue
        menu = Menu(**menu_data)
        db.add(menu)
        db.flush()
        menu_map[menu.code] = menu.id
        created_count += 1
    
    db.commit()
    
    parent_map = {
        "SYSTEM": 2,
        "SYSTEM_USERS": 2, "SYSTEM_ROLES": 2, "SYSTEM_DEPTS": 2, "SYSTEM_MENUS": 2,
        "SUPPLY": 7,
        "SUPPLY_SUPPLIERS": 7, "SUPPLY_PURCHASE": 7, "SUPPLY_INVENTORY": 7, "SUPPLY_SALES": 7,
        "FINANCE": 12,
        "FINANCE_PAYMENTS": 12, "FINANCE_BILLS": 12, "FINANCE_ACCOUNTS": 12, "FINANCE_REPORTS": 12,
        "ANALYSIS": 17,
        "ANALYSIS_SUPPLIER": 17, "ANALYSIS_PURCHASE": 17, "ANALYSIS_INVENTORY": 17,
        "ANALYSIS_SALES": 17, "ANALYSIS_PAYMENT": 17, "ANALYSIS_BILL": 17, "ANALYSIS_ACCOUNT": 17,
    }
    
    for menu_data in menus:
        if menu_data["parent_id"] is None and menu_data["code"] in parent_map:
            menu = db.query(Menu).filter(Menu.code == menu_data["code"]).first()
            if menu:
                menu.parent_id = parent_map[menu_data["code"]]
    
    db.commit()
    print(f"成功创建 {created_count} 个菜单（已存在 {len(menus) - created_count} 个）")
    return menu_map

def main():
    print("=" * 60)
    print("厦门建发集团供应链管理系统 - 测试数据初始化")
    print("=" * 60)
    db = SessionLocal()
    try:
        print("\n开始初始化测试数据...\n")
        dept_map = create_departments(db)
        role_map = create_roles(db)
        perm_map = create_permissions(db)
        user_map = create_users(db, dept_map, role_map)
        create_menus(db)
        supplier_map = create_suppliers(db)
        customer_map = create_customers(db)
        cat_map = create_product_categories(db)
        product_map = create_products(db, cat_map)
        warehouse_map = create_warehouses(db)
        account_map = create_accounts(db)
        cc_map = create_cost_centers(db)
        wf_map = create_workflow_definitions(db)
        create_purchase_orders(db, supplier_map, product_map, user_map, warehouse_map)
        create_sales_orders(db, customer_map, product_map, user_map, warehouse_map)
        create_payments_and_bills(db, supplier_map, customer_map, user_map, account_map)
        create_workflow_instances(db, wf_map, user_map)
        print("\n" + "=" * 60)
        print("测试数据初始化完成！")
        print("=" * 60)
        print("\n默认用户密码：123456")
        print("管理员账号：admin")
        print("\n数据统计：")
        print(f"  - 部门：{len(DEPARTMENTS)} 个")
        print(f"  - 用户：{len(USERS)} 个")
        print(f"  - 角色：{len(ROLES)} 个")
        print(f"  - 供应商：{len(SUPPLIERS)} 个")
        print(f"  - 客户：{len(CUSTOMERS)} 个")
        print(f"  - 产品分类：{len(PRODUCT_CATEGORIES)} 个")
        print(f"  - 产品：{len(PRODUCTS)} 个")
        print(f"  - 仓库：{len(WAREHOUSES)} 个")
        print(f"  - 账户：{len(ACCOUNTS)} 个")
        print(f"  - 成本中心：{len(COST_CENTERS)} 个")
        print(f"  - 工作流定义：{len(WORKFLOW_DEFINITIONS)} 个")
    except Exception as e:
        print(f"\n初始化失败：{e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
