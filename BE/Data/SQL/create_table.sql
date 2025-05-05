-- 目前一共6种不同的response
-- (1) login
-- (2) findMy
-- (3) type
-- (4) typeProducts
-- (5) productDetail
-- (6) searchguess

-- 先创建5张表

-----------------------------------
-- (1) login
-- (2) findMy
-- 用户表（users）
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,  -- 登录账号
  password VARCHAR(255) NOT NULL,        -- 加密后的密码
  nickName VARCHAR(50) DEFAULT '',       -- 昵称
  phoneNum INT,                          -- 手机号码
  userImg VARCHAR(255) DEFAULT 'http://newcoffee.wwp666.cn:10006/assets/default.png',
  userBg VARCHAR(255) DEFAULT 'http://newcoffee.wwp666.cn:10006/assets/default_bg.jpg',
  `desc` TEXT,                           -- 用户描述
  vip TINYINT DEFAULT 0,                 -- VIP等级 0-非会员
  token VARCHAR(255),                    -- JWT令牌
  token_expire DATETIME,                 -- 令牌过期时间
  createdAt DATETIME NOT NULL,
  updatedAt DATETIME NOT NULL
);


-----------------------
-- (3) type
-- 商品分类表（product_types）
CREATE TABLE product_types (
  id INT PRIMARY KEY AUTO_INCREMENT,
  type VARCHAR(20) NOT NULL UNIQUE,     -- 类型标识（latte/coffee等） e.g. coffee
  typeDesc VARCHAR(20) NOT NULL,        -- 类型描述
  createdAt DATETIME NOT NULL,
  updatedAt DATETIME NOT NULL
);

-------------------------
-- (4) typeProducts
-- (5) productDetail
-- 商品表（products）
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  pid VARCHAR(20) NOT NULL UNIQUE,      -- 商品唯一编号
  type VARCHAR(20) NOT NULL,            -- 关联product_types.type  e.g. coffee
  name VARCHAR(100) NOT NULL,
  enname VARCHAR(100) NOT NULL,         -- 英文名称
  price DECIMAL(10,2) NOT NULL,
  `desc` TEXT NOT NULL,
  smallImg VARCHAR(255) NOT NULL,
  largeImg VARCHAR(255) NOT NULL,
  isHot TINYINT DEFAULT 0,              -- 是否热卖 0/1
  tem VARCHAR(50),                      -- 温度选项
  tem_desc VARCHAR(50),
  sugar VARCHAR(50),                    -- 糖分选项
  sugar_desc VARCHAR(50),
  milk VARCHAR(50),                     -- 奶选项
  milk_desc VARCHAR(50),
  cream VARCHAR(50),                    -- 奶油选项
  cream_desc VARCHAR(50),
  createdAt DATETIME NOT NULL,
  updatedAt DATETIME NOT NULL,
  FOREIGN KEY (type) REFERENCES product_types(type)
);

--------------------------
-- (6) searchguess
-- 推广内容表（promotions）
CREATE TABLE promotions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  imgUrl VARCHAR(255) NOT NULL,         -- 推广图片
  `desc` VARCHAR(255) NOT NULL,         -- 推广描述
  sort_order INT DEFAULT 0,             -- 排序顺序
  createdAt DATETIME NOT NULL,
  updatedAt DATETIME NOT NULL
);


-----------------
--商品规格（温度/糖分）可单独建表实现更灵活配置
CREATE TABLE product_specs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  pid VARCHAR(20) NOT NULL,
  spec_type ENUM('tem','sugar','milk','cream') NOT NULL,
  spec_value VARCHAR(50) NOT NULL,
  spec_desc VARCHAR(50),
  FOREIGN KEY (pid) REFERENCES products(pid)
);
